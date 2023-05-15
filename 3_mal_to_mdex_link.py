# %%
import random
import datetime
import time
import pandas as pd
from playwright.sync_api import sync_playwright


# %%
def download_mdex_links(mdex_search, ggl_search, ranks, start, end):
    with sync_playwright() as p:
        mdex_dict_links = []

        s_mdex_search = mdex_search[start:end]
        s_ggl_search = ggl_search[start:end]
        s_ranks = ranks[start:end]

        error_count = 0

        for mdex_search, ggl_search, rank in zip(s_mdex_search, s_ggl_search, s_ranks):
            browser = p.chromium.launch()
            page = browser.new_page()

            try:
                page.goto(mdex_search)
                page.wait_for_selector(".manga-card-dense a", timeout=5000)
                mdex_link = page.get_attribute(
                    ".manga-card-dense a", "href", timeout=5000
                )

                link_dict = {
                    "rank": rank,
                    "search_term": mdex_search,
                    "mdex_link": mdex_link,
                    "link_method": "mdex",
                }
                mdex_dict_links.append(link_dict)

            except:
                browser.close()
                browser = p.chromium.launch()
                page = browser.new_page()
                print("FAIL-MDEX", mdex_search, rank)
                try:
                    page.goto(ggl_search)
                    page.wait_for_selector("div.g a", timeout=5000)
                    mdex_link = page.get_attribute("div.g a", "href", timeout=5000)

                    link_dict = {
                        "rank": rank,
                        "search_term": ggl_search,
                        "mdex_link": mdex_link,
                        "link_method": "google",
                    }
                    mdex_dict_links.append(link_dict)
                    print("PASS-GGL_1", ggl_search, mdex_link)

                except:
                    print("FAIL-GGL_1", ggl_search, rank)
                    error_count += 1

            sleep_time = random.randint(6, 8) / 2
            time.sleep(sleep_time)
            print(rank)
            browser.close()

        manga_df = pd.DataFrame(mdex_dict_links)
        manga_df.to_csv(
            "data/raw/mdex_link_tables/mdex_{}_to_{}.csv".format(start, end),
            index=False,
        )

        return error_count


# %%
mal_top_mangas = pd.read_csv("data/raw/mal_top_manga.csv")
ranks = mal_top_mangas["rank"].to_list()
titles = mal_top_mangas["title"].to_list()

titles = [
    title.replace('"', "").replace("'", "").replace("&", "%26") for title in titles
]

mdex_search_urls = [
    "https://mangadex.org/search?q={}&tab=titles".format(title).replace(" ", "+")
    for title in titles
]
ggl_search_urls = [
    "https://www.google.com/search?q={}+site:https://mangadex.org/title".format(
        title
    ).replace(" ", "+")
    for title in titles
]

# %%
start_time = datetime.datetime.now()
start_n = 13800
end_n = 15050
inc_size = 50
sleep_time = 60

error_count = 0
while start_n < end_n and error_count < 50:
    error_count = download_mdex_links(
        mdex_search_urls,
        ggl_search_urls,
        ranks,
        start_n,
        start_n + inc_size,
    )
    total_seconds = (datetime.datetime.now() - start_time).total_seconds()
    time_formatted = str(datetime.timedelta(seconds=total_seconds))

    print(start_n, time_formatted, error_count)
    start_n += inc_size

    time.sleep(sleep_time)

# %%
