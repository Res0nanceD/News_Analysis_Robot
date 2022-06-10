import pandas as pd
import requests
import csv
import mysql.connector
from bs4 import BeautifulSoup as soup
from requests.exceptions import HTTPError
from datetime import datetime
from config import host, user, passwd, database_name, path_to_tickers_set


new_tickers = ["^TNX", "NQ=F"]
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
        my_cursor.execute('ALTER TABLE stockMarketPrices ADD COLUMN `{ticker}` FLOAT'.format(ticker=ticker))
    my_cursor.close()
