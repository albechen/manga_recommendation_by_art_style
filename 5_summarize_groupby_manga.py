# %%
import pandas as pd
import numpy as np

df = pd.read_csv("data/interim/image_feature_pca.csv")
# df = pd.read_csv("data/interim/feature_test.csv")

# %%
rank_count = df.groupby("rank").size().reset_index(name="pic_count")

# %%
pca_cols = df.filter(regex="^PCA").columns.to_list()
pca_cols

agg_func = {}
for col in pca_cols:
    agg_func[col] = [
        "median",
        ("pct_40", lambda x: np.percentile(x, 40)),
        ("pct_60", lambda x: np.percentile(x, 60)),
    ]

# %%
percentiles_df = df.groupby("rank").agg(agg_func)
percentiles_df.columns = [
    "_".join(col) if isinstance(col, tuple) else col for col in percentiles_df.columns
]

percentiles_df

# %%
pct_by_rank = rank_count.merge(percentiles_df, on="rank", how="left")
pct_by_rank
# %%
pct_by_rank.to_csv("data/processed/image_features_by_managa.csv")
