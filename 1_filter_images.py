#%%
import pandas as pd

pic_summary = pd.read_csv("data/images/pic_summary.csv")

# %%
PCT_WHITE_CUTOFF = 84.56
PCT_BLACK_CUTOFF = 50

initial_filter = pic_summary[
    (pic_summary["pct_white"] <= PCT_WHITE_CUTOFF)
    & (pic_summary["pct_black"] <= PCT_BLACK_CUTOFF)
    & (pic_summary["is_grayscale"] == True)
]

#%%
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
    (median_filtered["hw_ratio_diff"] > 0.5) & (median_filtered["hw_ratio_diff"] < 0.5)
]

#%%
grouped_ranks = (
    median_filtered.groupby("rank")
    .agg({"pic_path": "size"})
    .rename(columns={"pic_path": "pic_count"})
)

len(grouped_ranks[grouped_ranks["pic_count"] >= 5])
#%%
final_filter = initial_filter.merge(grouped_ranks, on="rank")
final_filter = final_filter[final_filter["pic_count"] >= 20]

final_filter
# %%

import matplotlib.pyplot as plt

plt.hist(final_filter["pic_count"].to_list(), bins=60)

plt.xlabel("Values")
plt.ylabel("Frequency")
plt.title("Histogram")

plt.show()
