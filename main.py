from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init('db/blogs.sqlite')

@app.route('/')
@app.route('/profile')
def profile():
    return render_template('index.html')

@app.route('/ether')
def ether():
    pass

@app.route('/horoscope')
def horoscope():
    return render_template('horoscope.html')

@app.route('/aura')
def aura():
    return render_template('aura.html')

@app.route('/tea')
def tea():
    return render_template('tea.html')

@app.route('/numero', methods=['GET', 'POST'])
def numero():
    if request.method == 'POST':  # this block is only entered when the form is submitted
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form.get('year')
        try:
            day = int(day)
            month = int(month)
            year = int(year)
            res = day + month + year
        except ValueError:
            return render_template("number.html", error='Можно использовать только числа')
        while True:
            if res not in range(1, 10) and res != 11 and res != 22:
                res = sum([int(item) for item in list(str(res))])
            else:
                return render_template("number.html", information=res)
    else:
        return render_template('number.html')

@app.route('/dreams')
def dreams():
    return render_template('aura.html')

@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # this block is only entered when the form is submitted
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me')
        session = db_session.create_session()
        user = session.query(User).filter(User.email == email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember_me)
        return render_template("/profile")
    else:
        return render_template('author.html')


# @app.route('/register', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':  # this block is only entered when the form is submitted
#         email = request.form.get('email')
#         password = request.form.get('password')
#         remember_me = request.form.get('remember_me')
#         # session = db_session.create_session()
#         # user = session.query(User).filter(User.email == email).first()
#         # if user and user.check_password(password):
#             # login_user(user, remember=form.remember_me.data)
#         return redirect("/")
#
#     else:
#         return render_template('register.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
