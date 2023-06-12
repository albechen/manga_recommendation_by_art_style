# %%
import pandas as pd
import os
import shutil

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

median_filtered = initial_filter.merge(median_ranks, on="rank")
median_filtered["hw_ratio"] = median_filtered["width"] / median_filtered["height"]
median_filtered["median_hw_ratio"] = (
    median_filtered["median_width"] / median_filtered["median_height"]
)
median_filtered["hw_ratio_diff"] = (
    median_filtered["median_hw_ratio"] - median_filtered["hw_ratio"]
)

median_filtered = median_filtered[
    (median_filtered["hw_ratio_diff"] < 0.5) & (median_filtered["hw_ratio_diff"] > -0.5)
]

median_filtered
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


import matplotlib.pyplot as plt

plt.hist(final_filter["pic_count"].to_list(), bins=60)

plt.xlabel("Values")
plt.ylabel("Frequency")
plt.title("Histogram")

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
