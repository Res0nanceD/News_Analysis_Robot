import requests
from bs4 import BeautifulSoup as soup

page = requests.get('https://finance.yahoo.com/m/f710f90d-e5c3-332f-8270-7999df4de439/investment-strategies-for.html')
page_soup = soup(page, "lxml")
print(page_soup)
