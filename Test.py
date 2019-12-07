#import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq  # Web client

#page_url ='https://www.cars.com/for-sale/searchresults.action/?&mkId=20005'
page_url ='https://www.cars.com/for-sale/searchresults.action/?dealerType=localOnly&mkId=20005&page=1&perPage=50&searchSource=GN_REFINEMENT&sort=relevance&zc=90006'
uClient = uReq(page_url)
page_soup = BeautifulSoup(uClient.read(), "html.parser")
uClient.close()
print(page_soup)
