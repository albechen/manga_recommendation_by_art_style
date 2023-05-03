# %%
import random
import time
from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def download_mal_top_mangas(num_manga):
    count = 0
    links_list = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        while count <= num_manga:
            url = "https://myanimelist.net/topmanga.php?type=manga&limit={}".format(
                count
            )
            page.goto(url)
            page.wait_for_selector("[class='hoverinfo_trigger fs14 fw-b']")
            html = page.inner_html(".top-ranking-table")
            soup = BeautifulSoup(html, "html.parser")
            manga_list = soup.find_all("a", class_="hoverinfo_trigger fs14 fw-b")

            links_list.extend(
                [
                    [manga.text, manga["href"], manga["href"].split("/")[-2]]
                    for manga in manga_list
                ]
            )

            sleep_time = random.randint(5, 10) / 2
            print(count, sleep_time)
            time.sleep(sleep_time)
            count += 50

        mal_top_mangas = pd.DataFrame(
            links_list, columns=["title", "mal_link", "mal_id"]
        )
        mal_top_mangas.to_csv("data/key_tables/mal_top_manga.csv")
        browser.close()


download_mal_top_mangas(num_manga=15000)

# %%
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd


# def download_mal_top_mangas(num_manga):
#     count = 0
#     links_list = []

#     while count <= num_manga:
#         url = "https://myanimelist.net/topmanga.php?type=manga&limit={}".format(count)
#         response = requests.get(url)
#         soup = BeautifulSoup(response.content, "html.parser")
#         print(soup)
#         manga_list = soup.find_all("a", class_="hoverinfo_trigger fs14 fw-b")

#         links_list.extend(
#             [
#                 [manga.text, manga["href"], manga["href"].split("/")[-2]]
#                 for manga in manga_list
#             ]
#         )

#         print(count)
#         count += 50

#     mal_top_mangas = pd.DataFrame(links_list, columns=["title", "mal_link", "mal_id"])
#     print(links_list)
#     # mal_top_mangas.to_csv("data/mal_top__manga.csv")


# download_mal_top_mangas(num_manga=100)

# %%
# import requests
# from bs4 import BeautifulSoup

# # URL of the manga page
# url = "https://myanimelist.net/topmanga.php?type=manga&limit=10050"

# # Send a request to the URL and get the response
# response = requests.get(url)

# # Parse the HTML content of the response using BeautifulSoup
# soup = BeautifulSoup(response.content, "html.parser")
# # print(soup)
# manga_list = soup.find_all("a", class_="hoverinfo_trigger fs14 fw-b")

# links_list = [manga["href"] for manga in manga_list]
# title_list = [manga["text"] for manga in manga_list]
# title_list
