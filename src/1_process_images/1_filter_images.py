# %%
import pandas as pd
import os
import shutil
import matplotlib.pyplot as plt

pic_summary = pd.read_csv("data/images/pic_summary.csv")


# %%
#############################################################
############### FILTER IMAGES TO KEEP #######################
#############################################################

PCT_WHITE_CUTOFF = 84.56
PCT_BLACK_CUTOFF = 50

initial_filter = pic_summary[
    (pic_summary["pct_white"] <= PCT_WHITE_CUTOFF)
    & (pic_summary["pct_black"] <= PCT_BLACK_CUTOFF)
    & (pic_summary["is_grayscale"] == True)
]

# %%
median_ranks = (
    initial_filter.groupby("rank")
    .agg({"width": "median", "height": "median"})
    .rename(columns={"width": "median_width", "height": "median_height"})
)

median_df = initial_filter.merge(median_ranks, on="rank")
median_df["hw_ratio"] = median_df["width"] / median_df["height"]
median_df["median_hw_ratio"] = median_df["median_width"] / median_df["median_height"]
median_df["hw_ratio_diff"] = median_df["median_hw_ratio"] - median_df["hw_ratio"]

median_filtered = median_df[
    (median_df["hw_ratio_diff"] < 0.5) & (median_df["hw_ratio_diff"] > -0.5)
]

# %%
grouped_ranks = (
    median_filtered.groupby("rank")
    .agg({"pic_path": "size"})
    .rename(columns={"pic_path": "pic_count"})
)

len(grouped_ranks[grouped_ranks["pic_count"] >= 5])
# %%
final_filter = initial_filter.merge(grouped_ranks, on="rank")
final_filter = final_filter[final_filter["pic_count"] >= 5]

final_filter

# %%
fig, axs = plt.subplots(1, 4, figsize=(20, 5))

axs[0].hist(median_df["hw_ratio_diff"].to_list(), bins=60)
axs[0].set_xlabel("hw_ratio_diff")
axs[0].set_ylabel("Frequency")
axs[0].set_title("Height / Width Ratio Difference of Image vs Median of Manga")

axs[1].hist(pic_summary["pct_white"].to_list(), bins=60)
axs[1].set_xlabel("pct_white")
axs[1].set_ylabel("Frequency")
axs[1].set_title("Percent Image Contains White Pixels")

axs[2].hist(pic_summary["pct_black"].to_list(), bins=60)
axs[2].set_xlabel("pct_black")
axs[2].set_ylabel("Frequency")
axs[2].set_title("Percent Image Contains Black Pixels")

axs[3].hist(final_filter["pic_count"].to_list(), bins=60)
axs[3].set_xlabel("number of images")
axs[3].set_ylabel("Frequency")
axs[3].set_title("Number of Images per Manga")

plt.tight_layout()
plt.savefig("data/images/results/image_filter_summary.png")
plt.show()

# %%
#############################################################
########## ACTUALLY DELETE IMAGES TO FILTER #################
#############################################################

dont_filter_list = final_filter["pic_path"].to_list()
all_pic_path = pic_summary["pic_path"].to_list()

to_filter_list = list(set(all_pic_path) - set(dont_filter_list))

print(len(all_pic_path) == len(dont_filter_list) + len(to_filter_list))

# %%
for img_path in to_filter_list:
    os.remove(img_path)

# %%
#############################################################
########## MAKE SURE FOLDERS ARE THERE ######################
#############################################################


def list_empty_folders(path):
    rank_path_list = ["/".join([path, rank]) for rank in os.listdir(path)]
    empty_paths = []
    for rank_path in rank_path_list:
        if len(os.listdir(rank_path)) == 0:
            empty_paths.append(rank_path)
    return empty_paths


path = "data/images/manga"
empty_folders = list_empty_folders(path)

# %%
for rank_path in empty_folders:
    shutil.rmtree(rank_path)
