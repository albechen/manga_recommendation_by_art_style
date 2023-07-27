# %%
import pandas as pd
import numpy as np
import ast
import re

df = pd.read_csv("data/interim/manga_site_features_combined.csv")

# %%
df_cols = df.columns.tolist()


def get_cols_start_with(cols, start_str):
    start_str_len = len(start_str)
    start_with_cols = [x for x in cols if x[:start_str_len] == start_str]
    return start_with_cols


df[["ani_genres", "ani_description"]]


# %%
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


tags_df = get_tag_metrics(df)


# %%
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


scores_df = get_score_metrics(df)

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Apply PCA
pca = PCA()
pca.fit(get_tag_metrics(df).drop(["rank"], axis=1))

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
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

# Assuming 'df' is your DataFrame containing numerical data.

# Apply t-SNE
tsne = TSNE(n_components=2, random_state=42)
tsne_result = tsne.fit_transform(tags_df.drop(["rank"], axis=1))

# Create a new DataFrame with the t-SNE results
tsne_df = pd.DataFrame(tsne_result, columns=["t-SNE1", "t-SNE2"])

# %%
# Plot t-SNE
plt.figure(figsize=(8, 6))
plt.scatter(tsne_df["t-SNE1"], tsne_df["t-SNE2"], s=10, alpha=0.05)
plt.xlabel("t-SNE Component 1")
plt.ylabel("t-SNE Component 2")
plt.title("t-SNE Visualization")
plt.grid(True)
plt.show()
