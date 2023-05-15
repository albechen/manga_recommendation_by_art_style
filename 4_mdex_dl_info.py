# %%
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import random
import datetime
import time


# %%
def extract_mdex_genres(page):
    try:
        html_genre = page.inner_html(".flex.flex-wrap.gap-1.tags-row")
        soup = BeautifulSoup(html_genre, "html.parser")
        tagged_names = [a_tag.text for a_tag in soup.find_all("a")]
    except:
        tagged_names = []
    return tagged_names


def extract_mdex_description(page):
    try:
        html_desc = page.query_selector(".md-md-container")
        paragraph = html_desc.query_selector("p")
        description = paragraph.text_content() if paragraph else None
    except:
        description = ""
    return description


def extract_mdex_mal_link(page):
    raw_link = page.query_selector('a[href^="https://myanimelist.net/manga/"]')
    mal_link = raw_link.get_attribute("href") if raw_link else None
    return mal_link


def extract_mdex_genre_desc_malLink(page):
    genre_lists = extract_mdex_genres(page)
    description = extract_mdex_description(page)
    mal_link = extract_mdex_mal_link(page)

    mdex_dict = {
        "mdex_genre": genre_lists,
        "mdex_description": description,
        "mdex_mal_link": mal_link,
    }
    return mdex_dict


def extract_mdex_dict_from_url(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_viewport_size({"width": 2048, "height": 1002})
        page.goto(url)
        page.wait_for_selector(".flex.flex-wrap.gap-1.tags-row", timeout=5000)
        mdex_dict = extract_mdex_genre_desc_malLink(page)
        browser.close()
    return mdex_dict


# %%
def download_mdex_data(mdex_links, ranks, start, end):
    s_mdex_links = mdex_links[start:end]
    s_ranks = ranks[start:end]
    mdex_data_list = []
    error_count = 0

    for link, rank in zip(s_mdex_links, s_ranks):
        try:
            mdex_dict = extract_mdex_dict_from_url(link)
            mdex_dict["rank"] = rank
            mdex_data_list.append(mdex_dict)

            sleep_time = random.randint(6, 8) / 2
            time.sleep(sleep_time)
            print(rank)

        except:
            print("FAIL", link, rank)
            error_count += 1

    manga_df = pd.DataFrame(mdex_data_list)
    manga_df.to_csv(
        "data/raw/mdex_data_tables/mdex_data_{}_to_{}.csv".format(start, end),
        index=False,
    )

    return error_count


# %%
mdex_links_df = pd.read_csv("data/raw/mdex_link.csv")
mdex_links = mdex_links_df["updated_mdex_link"].to_list()
ranks = mdex_links_df["rank"].to_list()

# %%
start_time = datetime.datetime.now()
start_n = 5650  # 5650 updated code to try accept desc
end_n = len(mdex_links)
inc_size = 50
sleep_time = 60

error_count = 0
while start_n < end_n and error_count < 50:
    error_count = download_mdex_data(
        mdex_links,
        ranks,
        start_n,
        start_n + inc_size,
    )

    total_seconds = (datetime.datetime.now() - start_time).total_seconds()
    time_formatted = str(datetime.timedelta(seconds=total_seconds))

    print(start_n, time_formatted, error_count)
    start_n += inc_size

    time.sleep(sleep_time)
