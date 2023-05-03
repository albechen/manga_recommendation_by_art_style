# %%
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = "https://mangadex.org/title/bcfa196d-d162-45f5-a224-61d26b04a077"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    page.wait_for_selector("[class='tag bg-accent']")
    html = page.inner_html(".flex.flex-wrap.gap-1.tags-row")
    soup = BeautifulSoup(html, "html.parser")
    print(soup)
    tagged_names = [a_tag.text for a_tag in soup.find_all("a")]
    print(tagged_names)
    browser.close()

# %%
# from selenium import webdriver
# import time

# from bs4 import BeautifulSoup


# # Define the URL of the manga page you want to scrape the genres from
# url = "https://mangadex.org/title/bcfa196d-d162-45f5-a224-61d26b04a077"

# # Start a new Chrome browser session
# # options = webdriver.ChromeOptions()
# # options.add_argument('start-maximized')
# # options.add_experimental_option('excludedSwitches', ['enable-automation'])
# # options.add_experimental_option('detach', True)
# # options.add_experimental_option('useAutomationExtension', False)

# driver = webdriver.Chrome()
# driver.get(url)
# time.sleep(5)

# page_source = driver.page_source
# soup = BeautifulSoup(page_source, "html.parser")
# print(soup)

# driver.quit()

# %%

# %%
# import requests
# from bs4 import BeautifulSoup

# # URL of the manga page
# url = "https://mangadex.org/title/bcfa196d-d162-45f5-a224-61d26b04a077"

# # Send a request to the URL and get the response
# response = requests.get(url)

# # Parse the HTML content of the response using BeautifulSoup
# soup = BeautifulSoup(response.content, 'html.parser')
# soup
