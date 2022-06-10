import time
import mysql.connector
import sqlalchemy
import yfinance as yf
import datetime
from datetime import datetime as dt
from config import host, user, passwd, database_name, path_to_tickers_set
from news_aggregator import get_tickers_set


print("automatic_update_for_stockMarketPrices_database is working on background")

if __name__ != '__main__':
    print("we are sleeping")
    time.sleep(800)


# def get_ticker_list(p):
#     with open(p, "r") as file:
#         reader = csv.reader(file, delimiter=",")
#         for row in reader:
#             return row


tickers_set = get_tickers_set(path_to_tickers_set)

while True:

    # signify what data we want to get and check if new data available

    Q = "SELECT MAX(`index`) FROM `stockMarketPrices`"
    db = mysql.connector.connect(
        host=host,
        port=3306,
        user=user,
        passwd=passwd,
        database=database_name
    )
    my_cursor = db.cursor()
    my_cursor.execute(Q)
    last_loaded_time = ()
    for x in my_cursor:
        last_loaded_time = x
    last_loaded_time = last_loaded_time[0]
    last_loaded_time = last_loaded_time + datetime.timedelta(minutes=5)
    print(last_loaded_time)
    now = dt.now()
    if __name__ != '__main__':
        while now.minute % 15 != 0:
            now = dt.now()


    # getting new data

    data = yf.download(
        tickers=tickers_set,
        threads=True,
        start="2022-04-22", #last_loaded_time,
        interval='5m',
        group_by='ticker'
    )
    data = data.loc[:, (slice(None), 'Close')]
    data = data.droplevel(1, axis=1)
    # data.dropna(axis=1, how="all")
    print("data successfully converted")
    if data.empty:
        time.sleep(800)
        continue

    # writing new data to sql

    engine = sqlalchemy.create_engine('mysql+mysqlconnector://{user}:{passwd}@{host}:{port}/{dbname}'.format(
        host=host,
        port=3306,
        user=user,
        passwd=passwd,
        dbname=database_name))
    data.to_sql(
        name="stockMarketPrices",
        con=engine,
        if_exists="append"
    )
    time.sleep(800)
