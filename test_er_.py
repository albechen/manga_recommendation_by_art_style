import asyncio
from playwright.async_api import async_playwright


async def get_first_link():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(
            "https://www.google.com/search?q=Sakamichi+no+Apollon:+Bonus+Track+site:https://mangadex.org/title"
        )
        await page.wait_for_selector("div.g a")
        first_link = await page.get_attribute("div.g a", "href")
        print(first_link)
        await browser.close()


asyncio.get_event_loop().run_until_complete(get_first_link())
