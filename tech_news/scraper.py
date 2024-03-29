from parsel import Selector
from tech_news.database import create_news
import requests
import time


# Requisito 1
def fetch(url):
    try:
        time.sleep(1)
        response = requests.get(
            url,
            headers={"user-agent": "Fake user-agent"},
            timeout=3
        )
        if response.status_code == 200:
            return response.text
        return None
    except requests.exceptions.Timeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(html_content)
    return selector.css(".entry-title > a::attr(href)").getall()


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    next_page_url = selector.css(".next.page-numbers::attr(href)").get()
    return next_page_url


# Requisito 4
def scrape_news(html_content):
    selector = Selector(html_content)
    url = selector.css("link[rel='canonical']::attr(href)").get()
    title = selector.css(".entry-title::text").get().strip()
    timestamp = selector.css(".meta-date::text").extract_first()
    writer = selector.css(".author > a::text").get()
    reading_time = selector.css(".meta-reading-time::text").get()
    summary = "".join(
            selector.css(".entry-content > p:first-of-type *::text").getall()
        ).strip()
    category = selector.css(".category-style > .label::text").get()
    return ({
                "url": url,
                "title": title,
                "timestamp": timestamp,
                "writer": writer,
                "reading_time": int(reading_time[0] + reading_time[1]),
                "summary": summary.strip(),
                "category": category,
            })


# Requisito 5
def get_tech_news(amount):
    html_content = fetch('https://blog.betrybe.com/')
    news_list = []
    i = 0
    while i < amount:
        i += 1
        if (i % 12) == 1:
            updates = scrape_updates(html_content)
        if (i % 12) == 0:
            next_page = scrape_next_page_link(html_content)
            html_content = fetch(next_page)
        current_news = fetch(updates[i % 12 - 1])
        news = scrape_news(current_news)
        news_list.append(news)
    create_news(news_list)
    return news_list
