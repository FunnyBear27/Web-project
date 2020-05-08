from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/profile')
def profile():
    return


@app.route('/ether')
def ether():
    pass


@app.route('/horoscope')
def horoscope():
    pass


@app.route('/aura')
def aura():
    pass


@app.route('/tea')
def tea():
    pass


@app.route('/numero')
def numero():
    pass


@app.route('/dreams')
def dreams():
    pass


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')