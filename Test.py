import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq  # Web client
import mysql.connector

myconn = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="qeweqw123",
  database="sam"
)

def insert_cars(carName,carYear,extColor,intColor,transmission,price,driveTrain,number):
    cur = myconn.cursor()
    sql = '''INSERT INTO sam.cars (car_name, car_year,car_model,car_ext_color,car_int_color,transmission,price,number,drivetrain)
            VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s)
            '''
    val = (carName,carYear,'---',extColor,intColor,transmission,price,number,driveTrain)
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

car_name_list=[]
extColor=[]
intColor=[]
transmission=[]
driveTrain=[]
year=[]
price=[]
number=[]
model=[]

bmw_names = page_soup.findAll("h2", {"class": "listing-row__title"})
bmw_color = page_soup.findAll("ul",{"class": "listing-row__meta"})
bmw_price = page_soup.findAll("span",{"class": "listing-row__price "})
bmw_number = page_soup.findAll("div",{"class": "listing-row__phone obscure"})


for o in range(len(bmw_number)):
    clean_bmw_number = str(bmw_number[o].getText)
    clean_bmw_number =clean_bmw_number.replace('<bound method Tag.get_text of <div class="listing-row__phone obscure">',"")
    clean_bmw_number =clean_bmw_number.replace('<span>',"")
    clean_bmw_number =clean_bmw_number.replace('</span>',"")
    clean_bmw_number =clean_bmw_number.replace('</div>>',"")
    clean_bmw_number =clean_bmw_number.replace('()',"")
    clean_bmw_number =clean_bmw_number.replace('<span class="dni-replace-',"")
    clean_bmw_number =clean_bmw_number.replace('</div>>',"")
    clean_bmw_number =clean_bmw_number.replace('<div class="obscured-placeholder">',"")
    clean_bmw_number =clean_bmw_number.replace('-</div>',"")
    clean_bmw_number =clean_bmw_number.replace('">(',"")
    clean_bmw_number =clean_bmw_number.replace(') ',"")
    clean_bmw_number =clean_bmw_number.replace('-',"")
    clean_bmw_number = clean_bmw_number.split()
    number.append(clean_bmw_number)


number.append('0')
#print(number)



#Gereksiz karakterleri temizliyoruz


for i in range(len(bmw_price)):
    clean_bmw_price = str(bmw_price[i].getText)
    clean_bmw_price =clean_bmw_price.replace('<bound method Tag.get_text of ',"")
    clean_bmw_price =clean_bmw_price.replace('<span class="listing-row__price-msrp">' ,"")
    clean_bmw_price =clean_bmw_price.replace('<span class="listing-row__mileage">' ,"")
    clean_bmw_price =clean_bmw_price.replace('<span class="listing-row__price ">' ,"")
    clean_bmw_price =clean_bmw_price.replace('</span>',"")
    clean_bmw_price =clean_bmw_price.replace('</div>>',"")
    clean_bmw_price =clean_bmw_price.replace('MSRP',"")
    clean_bmw_price =clean_bmw_price.replace('>',"")
    clean_bmw_price =clean_bmw_price.replace("['","")

    clean_bmw_price = clean_bmw_price.split()
    price.append(clean_bmw_price)

#Sitede son 3 price degeri yok eksik değerleri 0 olarak giriyorum
for x in range(47,50):
    price.append('0')








        #bmw_price =bmw_price.replace('<span class="listing-row__price">',"")

for i in range(len(bmw_color)):
    clean_car=str(bmw_names[i].getText)
    clean_car =clean_car.replace('<bound method Tag.get_text of ',"")
    clean_car =clean_car.replace('<h2 class="listing-row__title">',"")
    clean_car =clean_car.replace("</h2>>","")
    clean_car=clean_car.replace("\n","")
    clean_car=clean_car.replace("","")
    clean_car = clean_car[33:len(clean_car)]
    clean_car='2'+clean_car
    #print(clean_car)
    car_name_list.append(clean_car)

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


    for j in range(len(clean_bmw_color) // 8):
        extColor.append(clean_bmw_color[j+1])
        intColor.append(clean_bmw_color[j+3])
        transmission.append(clean_bmw_color[j+5])
        driveTrain.append(clean_bmw_color[j+7])
        year.append(clean_car[0:4])
    insert_cars(car_name_list[i],year[i],extColor[i],intColor[i],transmission[i],str(price[i]),str(number[i]),driveTrain[i])



#for dongusu koy

#print(extColor)


#print(clean_bmw_color)
