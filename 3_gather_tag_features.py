# %%
import pandas as pd
import numpy as np
import ast
import re
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("data/interim/manga_site_features_combined.csv")
df_cols = df.columns.tolist()


# %%
def get_cols_start_with(cols, start_str):
    start_str_len = len(start_str)
    start_with_cols = [x for x in cols if x[:start_str_len] == start_str]
    return start_with_cols


def get_mal_tags(df):
    mal_tag_cols = [
        "mal_genre",
        "mal_theme",
        "mal_demographic",
    ]

    mal_tags = df.copy()[["rank"] + mal_tag_cols]
    long_tag_list = []

    def replace_space_remove_non_char(x):
        x = x.replace(" ", "_")
        x = re.sub(r"[^a-zA-Z]", "", x)
        return x

    rank_list = mal_tags["rank"].tolist()
    for col in mal_tag_cols:
        tags = mal_tags[col].tolist()
        for rank, tag in zip(rank_list, tags):
            tag_list = ast.literal_eval(tag)
            tag_list = [replace_space_remove_non_char(x) for x in tag_list]
            tagged_tags = [[rank, col + "_" + tag, 1] for tag in tag_list]
            long_tag_list.extend(tagged_tags)

    long_tag_df = pd.DataFrame(long_tag_list, columns=["rank", "tag", "value"])
    wide_tag_df = long_tag_df.pivot_table(index="rank", columns="tag", values="value")
    wide_tag_df = wide_tag_df.reset_index()
    return wide_tag_df


def get_ani_tags(df):
    ani_tag_list = get_cols_start_with(df_cols, "ani_tag")
    ani_tag_df = df.copy()[["rank"] + ani_tag_list]
    return ani_tag_df


def get_tag_metrics(df):
    mal_tags = get_mal_tags(df)
    ani_tags = get_ani_tags(df)

    tags_df = pd.merge(mal_tags, ani_tags, on="rank", how="outer")
    tags_df.fillna(0, inplace=True)
    tags_df = tags_df.astype(int)

    return tags_df


def determine_svd_components(df):
    X = df.drop(["rank"], axis=1)
    X = csr_matrix(X)

    max_components = X.shape[1]
    svd = TruncatedSVD(n_components=max_components)

    svd.fit(X)
    explained_variances = np.cumsum(svd.explained_variance_ratio_)

    # Plot the explained variance ratio
    plt.plot(range(1, max_components + 1), explained_variances, marker="o")
    plt.xlabel("Number of Components")
    plt.ylabel("Cumulative Explained Variance")
    plt.title("Elbow Method to Find Optimal Number of Components")
    plt.grid(True)
    plt.show()


# %%
tags_df = get_tag_metrics(df)
determine_svd_components(tags_df)


# %%
def scale_and_svd(df, num_comp):
    X = df.drop(["rank"], axis=1)
    X = csr_matrix(X)

    svd = TruncatedSVD(n_components=num_comp)
    svd_df = svd.fit_transform(X)
    return svd_df


def get_svd_dataset(df, num_comp):
    tags_df = get_tag_metrics(df)
    svd_array = scale_and_svd(tags_df, num_comp)

    svd_cols = ["tag_svd_" + str(i) for i in range(svd_array.shape[1])]
    svd_pd = pd.DataFrame(svd_array, columns=svd_cols)
    svd_df = df[["rank"]].merge(svd_pd, left_index=True, right_index=True)
    return svd_df


def calculate_similarities_each_doc(doc_vectors):
    doc_vectors = [np.array(vec).reshape(1, -1) for vec in doc_vectors]
    total_ranks = len(doc_vectors)

    similarities = np.zeros((total_ranks, total_ranks))
    for i in range(total_ranks):
        print(i)
        similarities[i, i] = 1
        for j in range(i + 1, total_ranks):
            doc1 = doc_vectors[i]
            doc2 = doc_vectors[j]
            similarity_value = cosine_similarity(doc1, doc2)
            similarities[i, j] = similarity_value
            similarities[j, i] = similarity_value

    return similarities


def get_score_similarities(df, num_comp):
    tags_df = get_tag_metrics(df)
    svd_df = scale_and_svd(tags_df, num_comp)
    similarities = calculate_similarities_each_doc(svd_df)

    rank_list = df["rank"].tolist()
    similarities_df = pd.DataFrame(similarities, columns=rank_list, index=rank_list)
    similarities_df.reset_index(inplace=True)
    similarities_df.rename(columns={"index": "rank"}, inplace=True)
    return similarities_df


# %%
num_comp = 75
svd_df = get_svd_dataset(df, num_comp)
svd_df.to_csv("data/processed/processed_features_tag_svd.csv", index=False)

# %%
# score_similarities = get_score_similarities(df, num_comp)
# score_similarities.to_csv("data/processed/similarities_tags.csv", index=False)

# %%
