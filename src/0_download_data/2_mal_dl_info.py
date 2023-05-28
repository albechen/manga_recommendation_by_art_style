# %%
import random
import datetime
import time
import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re


# %%
def extract_dict_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    list_output = soup.find_all("div", class_="spaceit_pad")

    info_dict = {}
    vote_count = 10
    for x in list_output:
        list_test = re.sub("\s+", " ", x.text).split(sep=":")
        first_str = list_test[0].strip()

        if len(list_test) == 1:
            score_str = "score_{}".format(vote_count)
            votes = re.findall("\((.*?)\)", first_str)
            info_dict[score_str] = re.sub("[^0-9]", "", votes[0])
            vote_count -= 1
        else:
            info_dict[first_str] = " ".join([x.strip() for x in list_test[1:]])

    return info_dict


# %%
def download_mal_manga_info(stats_links, ranks, start, end):
    with sync_playwright() as p:
        manga_dict_list = []
        browser = p.chromium.launch()
        page = browser.new_page()

        s_links = stats_links[start:end]
        s_ranks = ranks[start:end]

        error_count = 0

        for link, rank in zip(s_links, s_ranks):
            try:
                page.goto(link)
                try:
                    page.wait_for_selector(".score-stats")
                    html = page.inner_html("#content")

                    manga_dict = extract_dict_from_html(html)
                    manga_dict["rank"] = rank
                    manga_dict_list.append(manga_dict)

                    sleep_time = random.randint(4, 8) / 2
                    time.sleep(sleep_time)
                    print(rank)
                except:
                    print("FAIL", link, rank)
                    error_count += 1
            except:
                try:
                    page.goto(link)
                    page.wait_for_selector(".score-stats")
                    html = page.inner_html("#content")

                    manga_dict = extract_dict_from_html(html)
                    manga_dict["rank"] = rank
                    manga_dict_list.append(manga_dict)

                    sleep_time = random.randint(4, 8) / 2
                    time.sleep(sleep_time)
                    print(rank)
                except:
                    print("FAIL", link, rank)
                    error_count += 1

        browser.close()
        manga_df = pd.DataFrame(manga_dict_list)
        manga_df.to_csv(
            "data/raw/mal_data_tables/mal_{}_to_{}.csv".format(start, end),
            index=False,
        )

        return error_count


# %%
mal_top_mangas = pd.read_csv("data/raw/mal_top_manga.csv")
ranks = mal_top_mangas["rank"].to_list()
stats_links = [link + "/stats" for link in mal_top_mangas["mal_link"].to_list()]


start_time = datetime.datetime.now()
start_n = 9750
inc_size = 100
sleep_time = 60

error_count = 0
while start_n < 15050 and error_count < 10:
    error_count += download_mal_manga_info(
        stats_links, ranks, start_n, start_n + inc_size
    )
    duration = datetime.datetime.now() - start_time
    total_seconds = int(duration.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    time_difference_string = f"{minutes:02}:{seconds:02}"
    print(start_n, time_difference_string, error_count)
    start_n += inc_size

    time.sleep(sleep_time)

# download_mal_manga_info(stats_links, ranks, 0, 2)
# %%
