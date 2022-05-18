import mysql.connector
import yfinance as yf
import csv
import sqlalchemy
from config import host, user, passwd, database_name

# Q for Query

try:
    db = mysql.connector.connect(
        host=host,
        port=3306,
        user=user,
        passwd=passwd
    )
    print("Successfully connected")
except Exception as e:
    print("Connection refused. Make sure that the config file stores the correct information")
    print(e)
else:
    Q1 = "CREATE DATABASE " + database_name
    try:
        db.cursor().execute(Q1)
    except Exception as e:
        print("database is already existed")
        print(e)
        print("Are you sure you want to delete existing dataBase and create new one? (y/n)")
        txt = input()
        while txt != "y" and txt != "yes" and txt != "n" and txt != "no":
            print("Unexpected value. Are you sure you want to delete existing dataBase and create new one? (y/n)")
            txt = input()
        if txt == "y" or txt == "yes":
            Q1 = "DROP DATABASE " + database_name
            db.cursor().execute(Q1)
            Q1 = "CREATE DATABASE " + database_name
            db.cursor().execute(Q1)


try:
    db = mysql.connector.connect(
        host=host,
        port=3306,
        user=user,
        passwd=passwd,
        database=database_name
    )
    print("Successfully connected to database")
except Exception as e:
    print("Unable to connect to the database. Make sure that the config file stores the correct information")
    print(e)
else:
    Q2 = "CREATE TABLE IF NOT EXISTS `{name}`.`news` (" \
         "`idnews` INT NOT NULL AUTO_INCREMENT,"\
         "`datetime` DATETIME NOT NULL,"\
         "`title` VARCHAR(100) NULL," \
         "`body` VARCHAR(1000) NULL," \
         "`ticker_symbol` VARCHAR(10) NULL,"\
         "PRIMARY KEY (`idnews`))" \
         "ENGINE = InnoDB".format(name=database_name)

    Q4 = "CREATE TABLE IF NOT EXISTS `{name}`.`predictions` (" \
         "`newsId` INT NOT NULL," \
         "`polarity` ENUM('positive', 'neutral', 'negative') NULL," \
         "`importance` ENUM('imorant', 'slightly', 'unimportant') NULL," \
         "`ticker` VARCHAR(10) NULL," \
         "PRIMARY KEY (`newsId`)," \
         "UNIQUE INDEX `newsId_UNIQUE` (`newsId` ASC) VISIBLE," \
         "CONSTRAINT `newsID`" \
         "FOREIGN KEY (`newsId`)" \
         "REFERENCES `news_analyse_robot_data_base`.`news` (`idnews`))" \
         "ENGINE = InnoDB".format(name=database_name)

    Q5 = "CREATE TABLE IF NOT EXISTS `{name}`.`dictionary` (" \
         "`ticker` VARCHAR(10) NOT NULL," \
         "`company_name` VARCHAR(45) NULL," \
         "PRIMARY KEY (`ticker`)," \
         "UNIQUE INDEX `ticker_UNIQUE` (`ticker` ASC) VISIBLE)" \
         "ENGINE = InnoDB".format(name=database_name)

    try:
        db.cursor().execute(Q2)
    except Exception as e:
        print("Table 'news' is already existed")
        print(e)

    try:
        db.cursor().execute(Q4)
    except Exception as e:
        print("Table stockMarketPrices is already existed")
        print(e)
    try:
        db.cursor().execute(Q5)
    except Exception as e:
        print("Table stockMarketPrices is already existed")
        print(e)

print("started loading stock market databases")

path = "ticker_list"


def get_ticker_list(p):
    with open(p, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            return row


try:
    ticker_list = get_ticker_list(path)
except Exception as e:
    print(e)
    print("check if the ticker_list file is located in the directory from where this program is launched")
else:
    try:
        engine = sqlalchemy.create_engine('mysql+mysqlconnector://{user}:{passwd}@{host}:{port}/{dbname}'.format(
            host=host,
            port=3306,
            user=user,
            passwd=passwd,
            dbname=database_name))
        data = yf.download(
            tickers=ticker_list,
            threads=True,
            period='59d',
            interval='15m',
            group_by='ticker'
        )
        data = data.loc[:, (slice(None), 'Close')]
        data = data.droplevel(1, axis=1)
        data.dropna(axis=1, how="all")
        data.to_sql(
            name="stockMarketPrices",
            con=engine,
            if_exists="replace"
        )
    except Exception as e:
        print("Connection error in sqlalchemy engine")
        print(e)

from automatic_update_for_stockMarketPrices_database import *
