# -*- coding: utf8 -*-
from flask import Flask, render_template
import os, signal, pickle
from kinopoisk.movie import Movie
from bs4 import BeautifulSoup
import requests, json

app = Flask(__name__, template_folder='.')
app.config['TEMPLATES_AUTO_RELOAD'] = True
films_roots = ['d:/VIDEO/', 'h:/VIDEO/']
db = {}


class Film: pass


def getPlot(filmID):
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'})
    r = s.get('https://www.kinopoisk.ru/film/'+str(filmID))
    soup = BeautifulSoup(r.text.encode('cp1251'), 'lxml')
    return soup.select('div.brand_words.film-synopsys')[0].text


@app.route("/jquery.min.js")
def jquery():
    return open('jquery.min.js', 'rb').read()
    
@app.route("/cookies.js")
def cookies():
    return open('cookies.js', 'rb').read()


@app.route("/")
def hello():
    films = []

    # try to load files
    files = json.load(open('files.json', 'r'))
    files = sorted(set(files))
    print 'Loading film list ok!'


    for f in files:
        name = os.path.splitext(f)[0]
        if name == '!service': continue
        if name not in db or not db[name].ok:
            try:
                print 'kinopoisk request:', name,
                m = Movie.objects.search(name)[0]
                db[name] = m
                db[name].ok = True
                print '... ok!'
            except Exception as e:
                db[name] = Film()
                db[name].ok = False
                print '... error: ', str(e)

            db[name].filename = name

        # get plot
        if db[name].ok and hasattr(db[name], 'plot'):
            if db[name].plot == '' or db[name].plot == 'None':
                print 'try to load plot for', db[name].id
                try: db[name].plot = getPlot(db[name].id)
                except: db[name].plot = 'None'


        films.append(db[name])

    return render_template('index.html', films=films)

if __name__ == "__main__":
    def signal_handler(*args):
        print 'Saving DB ...'
        pickle.dump(db, open('films.pickle', 'wb'))
        exit()
    # app terminate signal
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    try:
        db = pickle.load(open('films.pickle','rb'))
        print 'Loading DB ok!'
    except: print("Can't load DB!"); pass

    app.run(debug=False, port=80, host="0.0.0.0", threaded=True)