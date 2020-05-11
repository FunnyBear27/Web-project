from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from data.finding_zodiac_aura import finding_aura, finding_zodiac
from data import db_session
from data.users import User
import  sqlite3

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
        while True:
            if res not in range(1, 10) and res != 11 and res != 22:
                res = sum([int(item) for item in list(str(res))])
            else:
                return render_template("number.html", information=res)
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
        print(email)
        remember_me = request.form.get('remember_me')
        session = db_session.create_session()
        user = session.query(User).filter(User.email == email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember_me)
            return redirect("/profile")
        else:
            return render_template('author.html', error="Неправильный логин или пароль")
    else:
        return render_template('author.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_repeat = request.form.get('password_repeat')
        name = request.form.get('name')
        birth_day = request.form.get('day')
        birth_month = request.form.get('month')
        birth_year = request.form.get('year')
        if password != password_repeat:
            return render_template('register.html', title='Регистрация',
                                   error="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == email).first():
            return render_template('register.html', title='Регистрация',
                                   error="Такой пользователь уже есть")
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
        return redirect('/')
    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')