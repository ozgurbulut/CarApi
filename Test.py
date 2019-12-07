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

def insert_cars(carName,carYear,carModel,carExtColor,carInf):
    cur = myconn.cursor()
    sql = '''INSERT INTO sam.cars (car_name, car_year,car_model,car_ext_color,car_int_color,transmission,price,number)
            VALUES (%s, %s, %s, %s,%s,%s,%s,%s)
            '''
    val = (carName,carYear,carModel,carExtColor,carInf,carYear,carModel,carExtColor)
    try:
        cur.execute(sql,val)
        myconn.commit()
    except:
        myconn.rollback()
    print(cur.rowcount,"Sutun eklendi")

page_url ='https://www.cars.com/for-sale/searchresults.action/?dealerType=localOnly&mkId=20005&page=1&perPage=50&searchSource=GN_REFINEMENT&sort=relevance&zc=90006'
uClient = uReq(page_url)
page_soup = BeautifulSoup(uClient.read(), "html.parser")
uClient.close()

bmw_names = page_soup.findAll("h2", {"class": "listing-row__title"})
bmw_color = page_soup.findAll("ul",{"class": "listing-row__meta"})
#Gereksiz karakterleri temizliyoruz
car_name_list=[]
for i in range(len(bmw_names)):
    clean_car=str(bmw_names[i].getText)
    clean_car =clean_car.replace('<bound method Tag.get_text of ',"")
    clean_car =clean_car.replace('<h2 class="listing-row__title">',"")
    clean_car =clean_car.replace("</h2>>","")
    clean_car=clean_car.replace("\n","")
    clean_car=clean_car.replace("","")
    clean_car = clean_car[33:len(clean_car)]
    clean_car='2'+clean_car
    car_name_list.append(clean_car)

extColor=[]
intColor=[]
transmission=[]
driveTrain=[]
for i in range(len(bmw_color)):
    clean_car=str(bmw_names[i].getText)
    clean_car =clean_car.replace('<bound method Tag.get_text of ',"")
    clean_car =clean_car.replace('<h2 class="listing-row__title">',"")
    clean_car =clean_car.replace("</h2>>","")
    clean_car=clean_car.replace("\n","")
    clean_car=clean_car.replace("","")
    clean_car = clean_car[33:len(clean_car)]
    clean_car='2'+clean_car

    clean_bmw_color = str(bmw_color[i].getText)
    clean_bmw_color =clean_bmw_color.replace('<bound method Tag.get_text of ',"")
    clean_bmw_color=clean_bmw_color.replace("\n","")
    clean_bmw_color=clean_bmw_color.replace('<ul class="listing-row__meta ">',"")
    clean_bmw_color=clean_bmw_color.replace('</li><li>">',"")
    clean_bmw_color=clean_bmw_color.replace('<ul class="listing-row__meta cpcTest--hide"><li><strong>',"")
    clean_bmw_color=clean_bmw_color.replace('<li><strong>',"")
    clean_bmw_color=clean_bmw_color.replace(':</strong>',"")
    clean_bmw_color=clean_bmw_color.replace('</li>',"")
    clean_bmw_color=clean_bmw_color.replace('</ul>>',"")
    clean_bmw_color=clean_bmw_color.replace('           ',"")
    clean_bmw_color=clean_bmw_color.replace('. ',"")
    clean_bmw_color = clean_bmw_color.split()
    for i in range(len(clean_bmw_color) // 8):
        extColor.append(clean_bmw_color[i+1])
        intColor.append(clean_bmw_color[i+3])
        transmission.append(clean_bmw_color[i+5])
        driveTrain.append(clean_bmw_color[i+7])
    insert_cars(car_name_list[i],extColor[i],intColor[i],transmission[i],driveTrain[i])

'''print(len(car_name_list))
print(len(extColor))
print(len(intColor))
print(len(transmission))
print(len(driveTrain))
#print(clean_bmw_color)
'''

#for dongusu koy

#print(extColor)


#print(clean_bmw_color)
