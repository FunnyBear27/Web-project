from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from data.finding_zodiac_aura import finding_aura, finding_zodiac, leap_year
from data import db_session
from data.users import User
import sqlite3
from datetime import datetime

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

# подключение к БД
con = sqlite3.connect("db/zodiac.db", timeout=10, isolation_level=None)
cur = con.cursor()

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init('db/blogs.sqlite')


@app.route('/')
@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('index.html', email=current_user.email, birth_date=current_user.birthday,
                               aura_color=current_user.aura, zodiak_sign=current_user.zodiac)
    else:
        return render_template('index.html')


@app.route('/horoscope')
def horoscope():
    return render_template('horoscope.html')


@app.route('/horoscope/aries')
def aries():
    return render_template('sign.html', zodiac_sign='Овен',
                           sign_info=(cur.execute(f"""SELECT info
                                                      FROM zodiac_text
                                                      WHERE name = 'Овен'""").fetchall())[0][0])


@app.route('/horoscope/taurus')
def taurus():
    return render_template('sign.html', zodiac_sign='Телец',
                           sign_info=(cur.execute(f"""SELECT info
                                                      FROM zodiac_text
                                                      WHERE name = 'Телец'""").fetchall())[0][0])


@app.route('/horoscope/gemini')
def gemini():
    return render_template('sign.html', zodiac_sign='Близнецы',
                           sign_info=(cur.execute(f"""SELECT info
                                                      FROM zodiac_text
                                                      WHERE name = 'Близнецы'""").fetchall())[0][0])


@app.route('/horoscope/cancer')
def cancer():
    return render_template('sign.html', zodiac_sign='Рак',
                           sign_info=(cur.execute(f"""SELECT info
                                                      FROM zodiac_text
                                                      WHERE name = 'Рак'""").fetchall())[0][0])


@app.route('/horoscope/leo')
def leo():
    return render_template('sign.html', zodiac_sign='Лев',
                           sign_info=(cur.execute(f"""SELECT info
                                                      FROM zodiac_text
                                                      WHERE name = 'Лев'""").fetchall())[0][0])


@app.route('/horoscope/virgo')
def virgo():
    return render_template('sign.html', zodiac_sign='Дева',
                           sign_info=(cur.execute(f"""SELECT info
                                                      FROM zodiac_text
                                                      WHERE name = 'Дева'""").fetchall())[0][0])


@app.route('/horoscope/libra')
def libra():
    return render_template('sign.html', zodiac_sign='Весы',
                           sign_info=(cur.execute(f"""SELECT info
                                                      FROM zodiac_text
                                                      WHERE name = 'Весы'""").fetchall())[0][0])


@app.route('/horoscope/scorpio')
def scorpio():
    return render_template('sign.html', zodiac_sign='Скорпион',
                           sign_info=(cur.execute(f"""SELECT info
                                                      FROM zodiac_text
                                                      WHERE name = 'Скорпион'""").fetchall())[0][0])


@app.route('/horoscope/sagittarius')
def sagittarius():
    return render_template('sign.html', zodiac_sign='Стрелец',
                           sign_info=(cur.execute(f"""SELECT info
                                                      FROM zodiac_text
                                                      WHERE name = 'Стрелец'""").fetchall())[0][0])


@app.route('/horoscope/capricorn')
def capricorn():
    return render_template('sign.html', zodiac_sign='Козерог',
                           sign_info=(cur.execute(f"""SELECT info
                                                      FROM zodiac_text
                                                      WHERE name = 'Козерог'""").fetchall())[0][0])


@app.route('/horoscope/aquarius')
def aquarius():
    return render_template('sign.html', zodiac_sign='Водолей',
                           sign_info=(cur.execute(f"""SELECT info
                                                      FROM zodiac_text
                                                      WHERE name = 'Водолей'""").fetchall())[0][0])


@app.route('/horoscope/pisces')
def pisces():
    return render_template('sign.html', zodiac_sign='Рыбы',
                           sign_info=(cur.execute(f"""SELECT info
                                                      FROM zodiac_text
                                                      WHERE name = 'Рыбы'""").fetchall())[0][0])


@app.route('/aura')
def aura():
    return render_template('aura.html')


@app.route('/tea')
def tea():
    return render_template('tea.html')


@app.route('/numero')
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
        if ((month > 12 or month < 1) or day < 1 or (day > 31 and month in [1, 3, 5, 7, 8, 10, 12]) or
            (day > 30 and month in [4, 6, 9, 11]) or (month == 2 and leap_year(year) and day > 29) or
            (month == 2 and not leap_year(year) and day > 28)):
            return render_template("number.html", error='Неверная дата')
        while True:
            if res not in range(1, 10) and res != 11 and res != 22:
                res = sum([int(item) for item in list(str(res))])
            else:
                return render_template("number.html",
                                       information=(cur.execute(f"""SELECT info
                                                                    FROM numero_text
                                                                    WHERE name = {res}""").fetchall())[0][0])
    else:
        return render_template('number.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


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
        return redirect("/profile")
    else:
        return render_template('author.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_repeat = request.form.get('password_repeat')
        name = request.form.get('name')
        birth_day = int(request.form.get('day'))
        birth_month = int(request.form.get('month'))
        birth_year = int(request.form.get('year'))
        if password != password_repeat:
            return render_template('register.html', title='Регистрация',
                                   error="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == email).first():
            return render_template('register.html', title='Регистрация',
                                   error="Такой пользователь уже есть")
        if ((birth_year > (datetime.now().year - 14) or (birth_month > 12 or birth_month < 1) or birth_day < 1 or
           (birth_day > 31 and birth_month in [1, 3, 5, 7, 8, 10, 12]) or
           (birth_day > 30 and birth_month in [4, 6, 9, 11]) or
           (birth_month == 2 and leap_year(birth_year) and birth_day > 29) or
           (birth_month == 2 and not leap_year(birth_year) and birth_day > 28))):
            return render_template('register.html', title='Регистрация',
                                   error="Неверная дата рождения")
        user = User(
            username=name,
            email=email,
            birthday=f'{str(birth_day)}/{str(birth_month)}/{str(birth_year)}',
            aura=finding_aura(birth_year, birth_month, birth_day),
            zodiac=finding_zodiac(birth_month, birth_day)
        )
        user.set_password(password)
        session.add(user)
        session.commit()
        return redirect('/profile')
    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')