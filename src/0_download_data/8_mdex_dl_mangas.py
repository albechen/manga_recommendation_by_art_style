# %%
import os
import pandas as pd
import datetime
import time

# %%
mdex_link_df = pd.read_csv("data/raw/mdex_link.csv")[["rank", "updated_mdex_link"]]
mdex_data_df = pd.read_csv("data/raw/mdex_data.csv")[["rank", "mdex_mal_id"]]
mal_top_df = pd.read_csv("data/raw/mal_top_manga.csv")[["rank", "mal_id"]]

# %%
df = mal_top_df.merge(mdex_data_df, on="rank", how="left").merge(
    mdex_link_df, on="rank", how="left"
)
df["match_mal_id"] = df["mal_id"] == df["mdex_mal_id"]
matching_mal_mdex_links = df.loc[df["match_mal_id"] == True]
mdex_links = matching_mal_mdex_links["updated_mdex_link"].to_list()
ranks = matching_mal_mdex_links["rank"].to_list()


# %%
start_time = datetime.datetime.now()
start_n = 7261
end_n = len(ranks)
sleep_time = 30

for link, rank in zip(mdex_links[start_n:end_n], ranks[start_n:end_n]):
    total_seconds = (datetime.datetime.now() - start_time).total_seconds()
    time_formatted = str(datetime.timedelta(seconds=total_seconds))
    print(rank, time_formatted, link)

    path = '"data/images/{:05d}"'.format(rank)
    mdex_cmd = 'mangadex-dl {} --start-chapter 1 --end-chapter 5 --cover "512px" --start-page 6 --end-page 10 --path "{}"'.format(
        link, path
    )
    os.system(mdex_cmd)

    time.sleep(sleep_time)


# %%
