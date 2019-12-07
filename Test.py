#import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq  # Web client
import mysql.connector

myconn = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="qeweqw123",
  database="sam"
)

def insert_cars(carName,carYear,carModel,carExtColor):

    cur = myconn.cursor()
    sql = '''INSERT INTO sam.cars (car_name, car_year,car_model,car_ext_color,car_int_color,transmission,price,number)
            VALUES (%s, %s, %s, %s,%s, %s, %s, %s)
            '''
    val = (carName,carYear,carModel,carExtColor,carName,carYear,carModel,carExtColor)
    try:
        cur.execute(sql,val)
        myconn.commit()
    except:
        myconn.rollback()

    print(cur.rowcount,"Sutun eklendi")





#page_url ='https://www.cars.com/for-sale/searchresults.action/?&mkId=20005'
page_url ='https://www.cars.com/for-sale/searchresults.action/?dealerType=localOnly&mkId=20005&page=1&perPage=50&searchSource=GN_REFINEMENT&sort=relevance&zc=90006'
uClient = uReq(page_url)
page_soup = BeautifulSoup(uClient.read(), "html.parser")
uClient.close()

bmw_araclar = page_soup.findAll("h2", {"class": "listing-row__title"})
bmw_color = page_soup.findAll("ul",{"class": "listing-row__meta"})
'''
for i in range(50):
    print(bmw_araclar[i].getText())
    print(bmw_color[i].getText())
insert_cars(str(bmw_araclar[0]),str(bmw_araclar[0]),str(bmw_araclar[0]),str(bmw_araclar[0]))
'''
clean_car=str(bmw_araclar[0].getText)

for i in range(len(clean_car)):
    clean_car =clean_car.replace('<bound method Tag.get_text of ',"")
    clean_car =clean_car.replace('<h2 class="listing-row__title">',"")
    clean_car =clean_car.replace("</h2>>","")
    clean_car=clean_car.replace("\n","")
t = clean_car[33:len(clean_car)]
x='2'+t
print(x)
insert_cars(x,x,x,x)
