# %%
import pandas as pd

mal_top = pd.read_csv("data/key_tables/mal_top_manga.csv")
mal_data = pd.read_csv("data/key_tables/mal_data_tables/mal_0_to_100.csv")

# %%
mal_join = mal_data.merge(mal_top, on="rank", how="left")
mal_join["title_author"] = mal_join["title"] + " " + mal_join["Authors"]


mal_join["Authors"]

# %%
duplicates = mal_top.duplicated(subset=["title"], keep=False)
mal_top[duplicates].sort_values("title")
