import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq  # Web client
import mysql.connector
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
myconn = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="qeweqw123",
  database="sam"
)
#extcolor,intColor,price,brand,trans,name,year,name,drivetrain='','','','','','','','',''
def select_all():
    mycursor = myconn.cursor()
    sql = '''SELECT * FROM sam.cars'''
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    liste = []
    for x in myresult:
        liste.append(x)
    return(liste)
carName,carYear,carModel,extColor,intColor,transmission,price,driveTrain,number='','','','','','','','',''
carYear='2019'
extColor='Gray'
def like_cars(carName,carYear,carModel,extColor,intColor,transmission,price,driveTrain,number):
    mycursor = myconn.cursor()
    sql = "SELECT * FROM sam.cars WHERE car_name LIKE '%%"+carName+"%' and car_year LIKE '%%"+carYear+"%' and car_model LIKE '%%"+carModel+"%'  and car_ext_color LIKE '%%"+extColor+"%' and car_int_color LIKE '%%"+intColor+"%' and transmission LIKE '%%"+transmission+"%' and price LIKE '%%"+price+"%' and number LIKE '%%"+number+"%' and drivetrain LIKE '%%"+driveTrain+"%' "
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    return(myresult)
print(like_cars(carName,carYear,carModel,extColor,intColor,transmission,price,driveTrain,number))
#like_cars(extcolor,intColor,price,brand,trans,name,year,name,drivetrain)
def insert_cars(carName,carYear,carModel,extColor,intColor,transmission,price,driveTrain,number):
    cur = myconn.cursor()
    sql = '''INSERT INTO sam.cars (car_name, car_year,car_model,car_ext_color,car_int_color,transmission,price,number,drivetrain)
            VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s)
            '''
    val = (carName,carYear,carModel,extColor,intColor,transmission,price,number,driveTrain)
    try:
        cur.execute(sql,val)
        myconn.commit()
    except:
        myconn.rollback()
    print(cur.rowcount,"Sutun eklendi")
#Burada hangi sayfalardan veri cekeceksek onları listeliyoruz
page_url =['https://www.cars.com/for-sale/searchresults.action/?dealerType=localOnly&mkId=20005&page=1&perPage=50&searchSource=GN_REFINEMENT&sort=relevance&zc=90006','https://www.cars.com/for-sale/searchresults.action/?dealerType=localOnly&mkId=20015&page=1&perPage=50&searchSource=GN_REFINEMENT&sort=relevance&zc=90006']

for pages in range(len(page_url)):
    uClient = uReq(page_url[pages])
    page_soup = BeautifulSoup(uClient.read(), "html.parser")
    uClient.close()
    #Temizlenmis hallerini bu listelere atacagiz
    car_name_list=[]
    extColor=[]
    intColor=[]
    transmission=[]
    driveTrain=[]
    year=[]
    price=[]
    number=[]
    model=[]

    #aradiğimiz tagları cekiyoruz
    bmw_names = page_soup.findAll("h2", {"class": "listing-row__title"})
    bmw_color = page_soup.findAll("ul",{"class": "listing-row__meta"})
    bmw_price = page_soup.findAll("span",{"class": "listing-row__price "})
    bmw_number = page_soup.findAll("div",{"class": "listing-row__phone obscure"})

    #İstenmeyen karakter dizilerini her tag bolumune gore inspect edip cekiyoruz
    bmw_number_black_list=['<bound method Tag.get_text of <div class="listing-row__phone obscure">','<span>','</span>','</div>>','()','<span class="dni-replace-','<div class="obscured-placeholder">','-</div>','">(',') ','-']
    bmw_price_black_list=['<bound method Tag.get_text of ','<span class="listing-row__price-msrp">','<span class="listing-row__mileage">','<span class="listing-row__price ">','</span>','</div>>','MSRP','>',"['"]
    bmw_color_black_list=['<bound method Tag.get_text of ','<h2 class="listing-row__title">','</h2>>','\n','']
    bmw_price_black_list_s=['<bound method Tag.get_text of ',"\n",'<ul class="listing-row__meta ">','</li><li>">','<ul class="listing-row__meta cpcTest--hide"><li><strong>','<li><strong>',':</strong>','</li>','</ul>>','           ','. ']

    #Gereksiz karakterleri split ile temizliyoruz
    for o in range(len(bmw_number)):
        clean_bmw_number = str(bmw_number[o].getText)
        for ı in range(len(bmw_number_black_list)):
                clean_bmw_number =clean_bmw_number.replace(bmw_number_black_list[ı],"")
        clean_bmw_number = clean_bmw_number.split()
        number.append(clean_bmw_number)
    number.append('0')


    for i in range(len(bmw_price)):
        clean_bmw_price = str(bmw_price[i].getText)
        for pbl in range(len(bmw_price_black_list)):
            clean_bmw_price =clean_bmw_price.replace(bmw_price_black_list[pbl],"")
        clean_bmw_price = clean_bmw_price.split()
        price.append(clean_bmw_price)

    #Sitede son 3 price degeri yok eksik değerleri 0 olarak giriyorum
    for x in range(47,52):
        price.append('0')

            #bmw_price =bmw_price.replace('<span class="listing-row__price">',"")
    for i in range(len(bmw_color)):
        clean_car=str(bmw_names[i].getText)
        for bcbl in range(len(bmw_color_black_list)):
            clean_car =clean_car.replace(bmw_color_black_list[bcbl],"")
        clean_car = clean_car[33:len(clean_car)]
        clean_car='2'+clean_car
        #print(clean_car)
        car_name_list.append(clean_car)
        model.append(clean_car[5:len(clean_car)])
        clean_bmw_color = str(bmw_color[i].getText)
        for bccl in range(len(bmw_price_black_list_s)):
                clean_bmw_color =clean_bmw_color.replace(bmw_price_black_list_s[bccl],"")
        clean_bmw_color = clean_bmw_color.split()
        #Deger asimi olmamasi icin her sutun degeri için 1 dongu yapılacak
        for j in range(len(clean_bmw_color) // 8):
            extColor.append(clean_bmw_color[j+1])
            intColor.append(clean_bmw_color[j+3])
            transmission.append(clean_bmw_color[j+5])
            driveTrain.append(clean_bmw_color[j+7])
            year.append(clean_car[0:4])
        insert_cars(car_name_list[i],year[i],str(model[i]),extColor[i],intColor[i],transmission[i],str(price[i]),driveTrain[i],str(number[i]))

app = Flask(__name__)


@app.route("/query")
def query():
    #Varsayılan degerleri null veriyoruz sql sorgusunda hata donmesin diye
    args = request.args
    if 'extcolor' in args:
                extcolor = args.get("extcolor")
    if 'intcolor' in args:
                intColor = args.get("intcolor")
    if 'price' in args:
                price = args.get("price")
    if 'brand' in args:
                brand = args.get("brand")
    if 'trans' in args:
                trans = args.get("trans")
    if 'name' in args:
                name = args.get("name")
    if 'year' in args:
                year = args.get("year")
    if 'name' in args:
                name = args.get("name")
    if 'drivetrain' in args:
                drivetrain = args.get("drivetrain")
    carName,carYear,carModel,extColor,intColor,transmission,price,driveTrain,number='','','','','','','','',''
    query_like = like_cars(carName,carYear,carModel,extColor,intColor,transmission,price,driveTrain,number)
    #return render_template('like.html',list=query_like)
    return render_template('like.html',list=query_like)

@app.route("/cars/list")
def cars():
    all=select_all()
    return render_template('list.html',list=all)


if __name__ == "__main__":
    app.run()
