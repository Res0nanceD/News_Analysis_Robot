# import yfinance as yf
# # from displayfunction import display
# import pandas as pd
# import time
# import sqlalchemy
# import csv
# from config import host, user, passwd, database_name
#
# path = "ticker_list"
#
#
# def get_ticker_list(p):
#     with open(p, "r") as file:
#         reader = csv.reader(file, delimiter=",")
#         for row in reader:
#             return row
#
#
# ticker_list = get_ticker_list(path)
# try:
#     engine = sqlalchemy.create_engine('mysql+mysqlconnector://{user}:{passwd}@{host}:{port}/{dbname}'.format(
#         host=host,
#         port=3306,
#         user=user,
#         passwd=passwd,
#         dbname=database_name))
#     data = yf.download(
#         tickers=ticker_list,
#         threads=True,
#         period='59d',
#         interval='15m',
#         group_by='ticker'
#     )
#     data = data.loc[:, (slice(None), 'Close')]
#     data = data.droplevel(1, axis=1)
#     data.dropna(axis=1, how="all")
#     # temp = yf.Ticker("MMM")
#     # df = temp.history(period='1mo', interval='30m')
#     # stockMarketPrices_df = df.loc[:, ['Open']]
#     # stockMarketPrices_df.rename(columns={"Open": ticker_list[0]}, inplace=True)
#     # print(stockMarketPrices_df.shape)
#     # for i in range(len(ticker_list[1:])):
#     #     ticker = ticker_list[i + 1]
#     #     temp = yf.Ticker(ticker)
#     #     df = temp.history(period='1mo', interval='30m')
#     #     if df.shape[0] != stockMarketPrices_df.shape[0]:
#     #         print(str(df.shape) + " " + str(i))
#     #         continue
#     #     if i % 50 == 0 and i != 0:
#     #         time.sleep(10)
#     #     new_df = df.loc[:, ['Open']]
#     #     new_df.rename(columns={"Open": ticker}, inplace=True)
#     #     stockMarketPrices_df = pd.merge(stockMarketPrices_df, new_df, left_index=True, right_index=True)
#     #     print(ticker + str(stockMarketPrices_df.shape) + " " + str(i))
#     data.to_sql(
#         name="stockMarketPrices",
#         con=engine,
#         if_exists="replace"
#         # append or fail
#     )
#     # 341,
# except Exception as e:
#     print("Connection error in sqlalchemy engine")
#     print(e)