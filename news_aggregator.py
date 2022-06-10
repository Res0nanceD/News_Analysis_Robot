import pandas as pd
import requests
import csv
import mysql.connector
from bs4 import BeautifulSoup as soup
from requests.exceptions import HTTPError
from datetime import datetime
from config import host, user, passwd, database_name, path_to_tickers_set


# ___________________
# function to get tickers_set

def get_tickers_set(path):
    with open(path, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            return row


def update_tickers_set(path, input_variable):
    with open(path, "w") as file:
        my_writer = csv.writer(file, delimiter=',')
        my_writer.writerow(input_variable)


def get_content(page_html):
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.find_all("h3", {"class": "Mb(5px)"})
    links = []

    # ___________________
    # getting all link from yahoo latest stock market news

    for container in containers:
        for element in container:
            news_url = "https://finance.yahoo.com" + element.get("href")
            news_title = str(element).split("/")[-2]
            news_title = news_title[2:-1]
            links.append([news_title, news_url])

    result = []
    mentioned_tickers = set()

    for link in links:
        try:
            response = requests.get(link[1], headers={'User-Agent': 'Custom'})
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        else:
            page_soup = soup(response.text, "html.parser")

            # ___________________
            # getting tickers

            tickers = set()
            containers = page_soup.find_all('button', {"aria-haspopup": "dialog"})
            try:
                for container in containers:
                    tickers.add(container.get("aria-label"))
            except Exception as e:
                print("no tickers found, and exception accrued")
                print(e)
            mentioned_tickers = mentioned_tickers.union(tickers)
            tickers = ",".join(tickers)

            # ___________________
            # getting news body

            body = str()
            try:
                body = page_soup.find('div', class_='caas-body').text
            except Exception as e:
                print(f'error occurred while trying to get news body: {e}')

            # ___________________
            # getting news date

            date = ""
            try:
                date = page_soup.find('time', class_="caas-attr-meta-time").get("datetime")
                date = date[:-1]
                date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
            except Exception as e:
                print(f"error occurred while trying to get news date: {e}")

            # ___________________
            # forming the result [date, title, body, ticker, url_link]
            result.append([date, link[0], body, tickers, link[1]])

    # ___________________
    # checking if new tickers appeared in recent news and updating ticker_set if so

    try:
        tickers_list = get_tickers_set(path_to_tickers_set)
    except Exception as e:
        print(f"error occurred while trying to get tickers_set: {e}")
    else:
        tickers_set = set(tickers_list)

        # ___________________
        # updating SQL table to keep new tickers

        new_tickers = mentioned_tickers.difference(tickers_set)
        print(new_tickers)
        if len(new_tickers) != 0:
            try:
                db = mysql.connector.connect(
                    host=host,
                    port=3306,
                    user=user,
                    passwd=passwd,
                    database=database_name
                )
                my_cursor = db.cursor()
            except Exception as e:
                print(e)
            else:
                for ticker in new_tickers:
                    my_cursor.execute("ALTER TABLE stockMarketPrices ADD COLUMN `{ticker}` FLOAT".format(ticker=ticker))
                my_cursor.close()
                tickers_set = tickers_set.union(mentioned_tickers)
                try:
                    update_tickers_set(path_to_tickers_set, tickers_set)
                except Exception as e:
                    print(f"error occurred while trying to update tickers_set: {e}")

    # ___________________
    # converting result to pandas dataframe

    result = pd.DataFrame(result, columns=['datetime', 'title', 'body', 'tickers', 'url'])
    return result


if __name__ == '__main__':
    with open("finance_yahoo.html", "r") as file:
        df = get_content(file)
        df.to_csv("dataframe_example", index=False)
