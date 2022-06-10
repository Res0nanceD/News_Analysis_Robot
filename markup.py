import mysql.connector
from config import host, user, passwd, database_name, path_to_tickers_set
import pandas as pd

df = pd.read_csv("dataframe_example")
datetimes = df.loc[:, "datetime"]
tickers = df.loc[:, "tickers"]
df["prices"] = datetimes


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
    for i in range(len(datetimes)):
        time = datetimes[i]
        ticker = tickers[i]
        if ticker is not None:
            my_cursor.execute("SELECT (`index`) FROM `stockMarketPrices`")
            for x in my_cursor:
                df[df["datetime"] == time, "prices"] = x
        else:
            continue
    my_cursor.close()

print(df)