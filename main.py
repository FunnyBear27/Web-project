from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from data.finding_zodiac_aura import finding_aura, finding_zodiac, leap_year
from data import db_session
from data.users import User
from data.teas import Teas
import sqlite3
from datetime import datetime

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

# подключение к БД
con = sqlite3.connect("db/zodiac.db", check_same_thread=False)
cur = con.cursor()

app.config['SECRET_KEY'] = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'

db_session.global_init('db/info.sqlite')


@app.route('/')
@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('index.html', email=current_user.email, birth_date=current_user.birthday,
                               aura_color=current_user.aura, zodiak_sign=current_user.zodiac)
    else:
        return render_template('index.html')


@app.route('/profile/my_tea')
def my_tea():
    session = db_session.create_session()
    teas = session.query(Teas).filter(Teas.user_id == current_user.id)
    if teas.count() == 0:
        return render_template('my_teas.html', title='Мои рецепты', recipes=teas, error='Рецептов нет')
    else:
        return render_template('my_teas.html', title='Мои рецепты', recipes=teas)

@app.route('/editing/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        session = db_session.create_session()
        recipe = session.query(Teas).filter(current_user.id == id).first()

        title = request.form.get('title')
        text = request.form.get('text')
        private = request.form.get('private')
        if private == 'True':
            private = True
        else:
            private = False

        tea = Teas(
            title=title,
            content=text,
            created_date=datetime.now(),
            is_private=private,
            user_id=current_user.id,
            username=current_user.username
        )
        session.add(tea)
        session.commit()
        return redirect('/profile/my_tea')
    else:
        return render_template('tea_form.html')


@app.route('/news_delete/<id>')
def delete(id):
    session = db_session.create_session()
    recipe = session.query(Teas).filter(current_user.id == id).first()
    session.delete(recipe)
    session.commit()
    return redirect('/profile/my_tea')


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
    if current_user.is_authenticated:
        return render_template('aura.html',
                               aura_info=(cur.execute(f"""SELECT info
                                                          FROM aura_text
                                                          WHERE color = '{current_user.aura}'""").fetchall())[0][0])
    else:
        return render_template('aura.html',
                               aura_info='Вы не авторизованы, поэтому выберите цвет вручную')


@app.route('/aura/red')
def red():
    return render_template('aura.html', color='Красный',
                           aura_info=(cur.execute(f"""SELECT info
                                                      FROM aura_text
                                                      WHERE color = 'Красный'""").fetchall())[0][0])


@app.route('/aura/yellow')
def yellow():
    return render_template('aura.html', color='Желтый',
                           aura_info=(cur.execute(f"""SELECT info
                                                      FROM aura_text
                                                      WHERE color = 'Желтый'""").fetchall())[0][0])


@app.route('/aura/orange')
def orange():
    return render_template('aura.html', color='Оранжевый',
                           aura_info=(cur.execute(f"""SELECT info
                                                      FROM aura_text
                                                      WHERE color = 'Оранжевый'""").fetchall())[0][0])


@app.route('/aura/green')
def green():
    return render_template('aura.html', color='Зеленый',
                           aura_info=(cur.execute(f"""SELECT info
                                                      FROM aura_text
                                                      WHERE color = 'Зеленый'""").fetchall())[0][0])


@app.route('/aura/blue')
def blue():
    return render_template('aura.html', color='Голубой',
                           aura_info=(cur.execute(f"""SELECT info
                                                      FROM aura_text
                                                      WHERE color = 'Голубой'""").fetchall())[0][0])


@app.route('/aura/darkblue')
def darkblue():
    return render_template('aura.html', color='Синий',
                           aura_info=(cur.execute(f"""SELECT info
                                                      FROM aura_text
                                                      WHERE color = 'Синий'""").fetchall())[0][0])


@app.route('/aura/violet')
def violet():
    return render_template('aura.html', color='Фиолетовый',
                           aura_info=(cur.execute(f"""SELECT info
                                                      FROM aura_text
                                                      WHERE color = 'Фиолетовый'""").fetchall())[0][0])


@app.route('/aura/pink')
def pink():
    return render_template('aura.html', color='Розовый',
                           aura_info=(cur.execute(f"""SELECT info
                                                      FROM aura_text
                                                      WHERE color = 'Розовый'""").fetchall())[0][0])


@app.route('/aura/bronze')
def bronze():
    return render_template('aura.html', color='Бронзовый',
                           aura_info=(cur.execute(f"""SELECT info
                                                      FROM aura_text
                                                      WHERE color = 'Бронзовый'""").fetchall())[0][0])


@app.route('/aura/silver')
def silver():
    return render_template('aura.html', color='Серебряный',
                           aura_info=(cur.execute(f"""SELECT info
                                                      FROM aura_text
                                                      WHERE color = 'Серебряный'""").fetchall())[0][0])


@app.route('/aura/gold')
def gold():
    return render_template('aura.html', color='Золотой',
                           aura_info=(cur.execute(f"""SELECT info
                                                      FROM aura_text
                                                      WHERE color = 'Золотой'""").fetchall())[0][0])


@app.route('/tea')
def tea():
    session = db_session.create_session()
    teas = session.query(Teas).filter(Teas.is_private != True)
    if teas.count() == 0:
        return render_template('teas.html', title='Рецепты', recipes=teas, error='Рецептов нет')
    else:
        return render_template('teas.html', title='Рецепты', recipes=teas)


@app.route('/tea/make', methods=['GET', 'POST'])
def make_tea():
    if request.method == 'POST':
        session = db_session.create_session()
        title = request.form.get('title')
        text = request.form.get('text')
        private = request.form.get('private')
        if private == 'True':
            private = True
        else:
            private = False
        tea = Teas(
            title=title,
            content=text,
            created_date=datetime.now(),
            is_private=private,
            user_id=current_user.id,
            username=current_user.username
        )
        session.add(tea)
        session.commit()
        return redirect('/tea')
    else:
        return render_template('tea_form.html')


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
        return render_template('author.html',
                               error="Неправильный логин или пароль")
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