from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    # do something
    print query
    info = [
        {
            'title': 'salam1',
            'body': '111111111111111jkflsja ffdsf'
        },
        {
            'title': 'salam2',
            'body': '22222222222222fjsdklfs'
        }
    ]

    return render_template('index.html', info=info)


if __name__ == '__main__':
    app.run()