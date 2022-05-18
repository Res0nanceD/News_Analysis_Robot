import time
import pandas as pd
import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


# NASDAQ, NYSE and AMEX
def get_content(page_soup):
    # print("downloading news to database...")
    # page = requests.get(url)
    # page_soup = soup(page.content, "html.parser")
    containers = page_soup.find_all("h3", {"class": "Mb(5px)"})
    links = []

    for container in containers:
        for element in container:
            news_url = "https://finance.yahoo.com" + element.get("href")
            news_title = str(element).split("/")[-2]
            news_title = news_title[2:-1]
            links.append([news_title, news_url])
    result = []
    for elem in links:
        url = elem[1]
        print(url)
        page = requests.get(url)
        page_soup = soup(page.content, "html.parser")
        containers = page_soup.find_all('button', {"aria-haspopup": "dialog"})
        tickers = []
        try:
            for container in containers:
                tickers.append(container.get("aria-label"))
        except Exception:
            tickers = [None]
        tickers = ",".join(tickers)

        body = str()
        try:
            page_data = page_soup.find('div', class_='caas-body')
            for data in page_data:
                body = data.text
        except Exception:
            print("no data")
        date = ""
        try:
            date = page_soup.find('time', class_="caas-attr-meta-time").get("datetime")
            date = date[:-1]
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
        except Exception:
            print("no data")
        result.append([date, elem[0], body, tickers, elem[1]])
    result = pd.DataFrame(result, columns=['datetime', 'title', 'body', 'tickers', 'url'])
    return result

# дописать алгоритм, который при виде нового тикера находит данные о нем (или просто добавляет в тиккер лист)


def get_data_with_selenium(url):
    try:
        driver = webdriver.Chrome(service=Service("/Users/denis/Desktop/вкр/Project/chromedriver"))
        driver.get(url)
        last_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(5)
        SCROLL_PAUSE_TIME = 1

        # Get scroll height
        """last_height = driver.execute_script("return document.body.scrollHeight")

        this dowsnt work due to floating web elements on youtube
        """

        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                print("break")
                break
            last_height = new_height
        with open("finance_yahoo.html", "w") as file:
            file.write(driver.page_source)
        page_soup = soup(driver.page_source, "html.parser")
        result = get_content(page_soup)
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()
        return result


with open("finance_yahoo.html", "r") as file:
    page_soup = soup(file, "html.parser")
    df = get_content(page_soup)
    df.to_csv('out.csv', index=False)
url_link = 'https://finance.yahoo.com/topic/stock-market-news/'



