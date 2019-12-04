url = 'https://www.cars.com/for-sale/searchresults.action/?dealerType=localOnly&page=1&perPage=20&searchSource=GN_BREADCRUMB&sort=relevance&zc=90006'
import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

app.run()
