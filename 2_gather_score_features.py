# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("data/interim/manga_site_features_combined.csv")
df_cols = df.columns.tolist()


# %%
def get_cols_start_with(cols, start_str):
    start_str_len = len(start_str)
    start_with_cols = [x for x in cols if x[:start_str_len] == start_str]
    return start_with_cols


def get_score_metrics(df):
    mal_score_df = get_score_pct_mean_std(df, "mal")
    ani_score_df = get_score_pct_mean_std(df, "ani")
    score_df = pd.merge(mal_score_df, ani_score_df, on="rank", how="inner")
    return score_df


def get_score_pct_mean_std(df, prefix):
    base_df = df.copy()
    prefix = prefix + "_"

    score_list = get_cols_start_with(df_cols, prefix + "score")
    prefix = score_list[0][:4] + "_"

    score_pct_df = calc_pct_score(base_df, score_list)
    score_mean_std_df = calc_mean_std_score(base_df, score_list, prefix)

    score_df = pd.merge(score_pct_df, score_mean_std_df, on="rank", how="inner")

    return score_df


def calc_pct_score(df, score_list):
    rank_df = df.copy()[["rank"]]

    scores_df = df[score_list]
    scores_df = scores_df.fillna(0).astype(int)

    raw_scores = scores_df.copy()
    raw_scores["count"] = raw_scores.sum(axis=1)
    for score in score_list:
        rank_df[score] = raw_scores[score] / raw_scores["count"]

    return rank_df


def calc_mean_std_score(df, score_list, prefix):
    score_int = [int(int(col.split("_")[-1])) for col in score_list]
    scores_df = df[score_list]
    scores_df = scores_df.fillna(0).astype(int)

    raw_scores = scores_df.copy()
    raw_scores["count"] = raw_scores.sum(axis=1)
    for score in score_list:
        raw_scores[score] = raw_scores[score] / raw_scores["count"]

    scores_array = scores_df.values
    std_list = []

    for row in scores_array:
        std_list.append(np.std(np.repeat(score_int, row)))

    rank_df = df.copy()[["rank"]]
    rank_df["count"] = scores_df.sum(axis=1)
    rank_df["std"] = std_list

    for col in score_list:
        score = int(col.split("_")[-1])
        scores_df[col] = score * scores_df[col]

    rank_df["sum"] = scores_df.sum(axis=1)
    rank_df["mean"] = rank_df["sum"] / rank_df["count"]
    rank_df["mean_upper"] = rank_df["mean"] + rank_df["std"]
    rank_df["mean_lower"] = rank_df["mean"] - rank_df["std"]

    rank_df = rank_df[["rank", "mean", "mean_upper", "mean_lower"]]

    name_dict = {}
    for name in ["mean", "mean_upper", "mean_lower"]:
        name_dict[name] = prefix + name

    rank_df.rename(columns=name_dict, inplace=True)
    return rank_df


def determine_pca_components(df):
    scaler = StandardScaler()
    scores_scaled = scaler.fit_transform(df.drop(["rank"], axis=1))
    pca = PCA()
    pca.fit(scores_scaled)

    # Get explained variance ratio for each component
    explained_variance_ratio = pca.explained_variance_ratio_

    # Plot the cumulative explained variance to find the elbow point
    cumulative_variance = np.cumsum(explained_variance_ratio)
    plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker="o")
    plt.xlabel("Number of Components")
    plt.ylabel("Cumulative Explained Variance")
    plt.title("Elbow Method to Find Optimal Number of Components")
    plt.grid(True)
    plt.show()


# %%
scores_df = get_score_metrics(df)
# scores_df.to_csv("data/interim/aggregate_scores.csv", index=False)
determine_pca_components(scores_df)


# %%
def scale_and_pca(df, num_comp):
    scaler = StandardScaler()
    scaled_df = scaler.fit_transform(df.drop(["rank"], axis=1))
    pca = PCA(n_components=num_comp)
    pca_df = pca.fit_transform(scaled_df)
    return pca_df


def get_pca_dataset(df, num_comp):
    score_df = get_score_metrics(df)
    pca_array = scale_and_pca(score_df, num_comp)

    pca_cols = ["score_pca_" + str(i) for i in range(pca_array.shape[1])]
    pca_pd = pd.DataFrame(pca_array, columns=pca_cols)
    pca_df = df[["rank"]].merge(pca_pd, left_index=True, right_index=True)
    return pca_df


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
    scores_df = get_score_metrics(df)
    pca_df = scale_and_pca(scores_df, num_comp)
    similarities = calculate_similarities_each_doc(pca_df)

    rank_list = df["rank"].tolist()
    similarities_df = pd.DataFrame(similarities, columns=rank_list, index=rank_list)
    similarities_df.reset_index(inplace=True)
    similarities_df.rename(columns={"index": "rank"}, inplace=True)
    return similarities_df


# %%
num_comp = 9
pca_df = get_pca_dataset(df, num_comp)
pca_df.to_csv("data/processed/procsessed_features_score_pca.csv", index=False)

# %%
# score_similarities = get_score_similarities(df, num_comp)
# score_similarities.to_csv("data/processed/similarities_score.csv", index=False)

# %%
