import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def get_page_html(url):
    try:
        driver = webdriver.Chrome(service=Service("/Users/denis/Desktop/вкр/Implementation Of A News Analysis Robot/chromedriver"))
        driver.get(url)
        # last_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(10)
        scroll_pause_time = 5
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                print("break")
                break
            last_height = new_height
        with open("finance_yahoo3.html", "w") as file:
            file.write(driver.page_source)
    except Exception as e:
        print(e)
        return 1
    finally:
        driver.close()
        driver.quit()
        return 0


url_link = "https://finance.yahoo.com/topic/stock-market-news/"
get_page_html(url_link)
