# %%
import random
import datetime
import time
import pandas as pd


# %%
def download_mal_user_list(stats_links, ranks, start, end):
    full_user_df = pd.DataFrame(columns=["Member", "Score", "Status", "rank"])
    s_links = stats_links[start:end]
    s_ranks = ranks[start:end]

    error_count = 0

    for link, rank in zip(s_links, s_ranks):
        try:
            user_df = pd.read_html(link, header=0)[3]
            user_df["rank"] = rank
            user_df = user_df[["Member", "Score", "Status", "rank"]]
            full_user_df = pd.concat([full_user_df, user_df], ignore_index=True)

            sleep_time = random.randint(6, 8) / 2
            time.sleep(sleep_time)
            print(rank)
        except:
            print("FAIL", link, rank)
            error_count += 1

    full_user_df.to_csv(
        "data/raw/mal_user_list_tables/mal_users_{}_to_{}.csv".format(start, end),
        index=False,
    )

    return error_count


# %%
mal_top_mangas = pd.read_csv("data/raw/mal_top_manga.csv")
ranks = mal_top_mangas["rank"].to_list()
stats_links = [
    link + "/stats?m=all#members" for link in mal_top_mangas["mal_link"].to_list()
]


start_time = datetime.datetime.now()
start_n = 11300  # 4150
end_n = len(ranks)
inc_size = 50
sleep_time = 60
error_count = 0

while start_n < end_n and error_count < 10:
    error_count = download_mal_user_list(
        stats_links, ranks, start_n, start_n + inc_size
    )

    total_seconds = (datetime.datetime.now() - start_time).total_seconds()
    time_formatted = str(datetime.timedelta(seconds=total_seconds))

    print(start_n, time_formatted, error_count)
    start_n += inc_size

    time.sleep(sleep_time)
# %%
