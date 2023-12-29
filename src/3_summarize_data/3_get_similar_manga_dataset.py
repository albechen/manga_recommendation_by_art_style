# %%
import pandas as pd

# %%
df = pd.read_csv("data/processed/similarity_image_feature.csv")

# %%
rank_summary = pd.read_csv("data/processed/final_tsne_and_descriptions.csv")
rank_summary = rank_summary[["rank", "mal_title", "mal_demographic", "starting_decade"]]
rank_summary["rank_copy"] = rank_summary["rank"]
rank_summary.set_index("rank_copy", inplace=True)
rank_dict = rank_summary.to_dict(orient="index")


# %%
def gather_top_image_similarity(df, rank_num, top_n):
    rank_str = str(rank_num)
    similarities = df[
        ["rank", rank_str, "mal_title", "mal_demographic", "starting_decade"]
    ]
    similarities = similarities.sort_values(rank_str, ascending=False)
    top_similar = similarities.head(top_n)
    top_similar = top_similar.rename(
        columns={
            rank_str: "similarity_score",
            "mal_title": "place_title",
            "mal_demographic": "place_demographic",
            "starting_decade": "place_decade",
            "rank": "place_rank",
        }
    )
    top_similar["place"] = top_similar["similarity_score"].rank(
        ascending=False, method="dense"
    )

    top_similar["source_rank"] = rank_num
    top_similar["source_title"] = rank_dict[rank_num]["mal_title"]
    top_similar["source_demographic"] = rank_dict[rank_num]["mal_demographic"]
    top_similar["source_decade"] = rank_dict[rank_num]["starting_decade"]

    top_similar = top_similar[
        [
            "source_rank",
            "source_title",
            "source_demographic",
            "source_decade",
            "place",
            "similarity_score",
            "place_rank",
            "place_title",
            "place_demographic",
            "place_decade",
        ]
    ]
    top_similar = top_similar.reset_index(drop=True)
    return top_similar


# %%
full_df = df.merge(rank_summary, on="rank", how="inner")
sorted_ranks = sorted(set(list(full_df["rank"])))
top_n = 10
first_df = True

for rank in sorted_ranks:
    print(rank)
    top_similar = gather_top_image_similarity(full_df, rank, top_n)
    if first_df == False:
        top_similar_full = pd.concat([top_similar_full, top_similar], ignore_index=True)
    else:
        top_similar_full = top_similar
        first_df = False

# %%
top_similar_full.to_csv("data/processed/top_similarties_image_feature.csv", index=False)
