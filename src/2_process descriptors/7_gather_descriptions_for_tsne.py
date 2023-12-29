# %%
import pandas as pd
import ast
import re


# %%
def replace_space_remove_non_char(x):
    x = x.replace(" ", "_")
    x = re.sub(r"[^a-zA-Z]", "", x)
    return x


def get_mal_tags(df):
    mal_tags = df.copy()[["rank", "mal_demographic"]]
    tags = mal_tags["mal_demographic"].tolist()
    tag_str_list = []

    for tag in tags:
        tag_list = ast.literal_eval(tag)
        tag_list = [replace_space_remove_non_char(x) for x in tag_list]
        if len(tag_list) > 1:
            if "Kids" in tag_list:
                tag_list = ["Kids"]
            if "Seinen" in tag_list:
                tag_list = ["Seinen"]
        elif len(tag_list) == 0:
            tag_list = [""]
        tag_str = tag_list[0]
        tag_str_list.append(tag_str)

    mal_tags["mal_demographic"] = tag_str_list
    return mal_tags


def get_agg_scores():
    agg_scores = pd.read_csv("data/interim/aggregate_scores.csv")
    agg_scores = agg_scores[["rank", "ani__mean", "mal__mean"]]
    agg_scores["mean_score"] = round(
        (agg_scores["ani__mean"] + agg_scores["mal__mean"]) / 2 / 10
    )
    agg_scores = agg_scores[["rank", "mean_score"]].dropna()
    agg_scores["mean_score_int"] = agg_scores["mean_score"].astype(int)
    agg_scores["mean_score"] = "score_" + agg_scores["mean_score"].astype(int).astype(
        str
    )
    return agg_scores


def get_decade(df):
    decade_df = df.copy()[["rank", "mal_start_year"]].dropna()
    decade_df["starting_decade"] = round(df["mal_start_year"] / 10) * 10
    decade_df["starting_decade_int"] = decade_df["starting_decade"].astype(int)
    decade_df["starting_decade"] = "y_" + decade_df["starting_decade"].astype(
        int
    ).astype(str)
    decade_df = decade_df.drop(["mal_start_year"], axis=1)
    return decade_df


# %%
df = pd.read_csv("data/interim/manga_site_features_combined.csv")
mal_demo_sorted = get_mal_tags(df)
agg_scores = get_agg_scores()
decade_df = get_decade(df)

cols = [
    "rank",
    "mal_title",
    "mal_status",
    "mal_completed",
    "ani_description",
]

df = pd.read_csv("data/interim/manga_site_features_combined.csv")
feature_df = pd.merge(df[cols], mal_demo_sorted, on="rank", how="outer")
feature_df = pd.merge(feature_df, agg_scores, on="rank", how="outer")
feature_df = pd.merge(feature_df, decade_df, on="rank", how="outer")

# %%
tsne = pd.read_csv("data/processed/final_tsne_per_manga.csv")
full_df = pd.merge(feature_df, tsne, on="rank", how="inner")

# %%
full_df.to_csv("data/processed/final_tsne_and_descriptions.csv", index=False)

# %%
