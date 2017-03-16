from flask import Flask, render_template, url_for, request

from ranking.vsm import search

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', info=[])

@app.route('/search_me')
def search_me():
    query = request.args.get('query')
    info = search(query)
    print [result['url'] for result in info]
    return render_template('index.html', info=info, query=query)


if __name__ == '__main__':
    app.run()