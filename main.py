from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from data.register import LoginForm, RegisterForm
from data.finding_zodiac_aura import finding_aura, finding_zodiac
from data import db_session
from data.users import User

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init('db/blogs.sqlite')


@app.route('/')
@app.route('/profile')
@login_required
def profile():
    return render_template('index.html')


@app.route('/horoscope')
def horoscope():
    return render_template('horoscope.html')


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
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            birthday=form.birthday.data,
            aura=finding_aura(form.birthday.data),
            zodiac=finding_zodiac(form.birthday.data)
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')