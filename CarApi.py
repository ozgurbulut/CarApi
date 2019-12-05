url = 'https://www.cars.com/for-sale/searchresults.action/?dealerType=localOnly&page=1&perPage=20&searchSource=GN_BREADCRUMB&sort=relevance&zc=90006'
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"
    
@app.route("/cars/list/extcolor=black")
def salvador():
    return "Hello, siyah araba"
    
if __name__ == "__main__":
    app.run(debug=True)

    
    
    //denemeli
    @app.route("/login?provider=<provider>")
def login(provider):
    if provider == 'google':
        return "Hello, Google!"
    return render_template('login.html')
https://uniwebsidad.com/libros/explore-flask/chapter-6/url-converters
    https://stackoverflow.com/questions/50426137/flask-get-clicked-link-info-and-display-on-rendered-page
        https://gist.github.com/Jaza/61f879f577bc9d06029e
#Onemli ? isaretini buldum
https://pythonise.com/series/learning-flask/flask-query-strings
