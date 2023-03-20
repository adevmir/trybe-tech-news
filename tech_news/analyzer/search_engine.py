from tech_news.database import search_news
import datetime


# Requisito 7
def search_by_title(title):
    query = {"title": {"$regex": title, "$options": "i"}}
    news_list = search_news(query)
    result = []
    for news in news_list:
        result.append((news["title"], news["url"]))
    return result


# Requisito 8
def search_by_date(date):
    print(date)
    try:
        bd_date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
        print(bd_date)
        news_list = search_news({"timestamp": bd_date})
        result = []
        for news in news_list:
            result.append((news["title"], news["url"]))
        return result
    except ValueError:
         raise ValueError("Data inválida")


# Requisito 9
def search_by_category(category):
    query = {"category": {"$regex": category, "$options": "i"}}
    news_list = search_news(query)
    result = []
    for news in news_list:
        result.append((news["title"], news["url"]))
    return result
