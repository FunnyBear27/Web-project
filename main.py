from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from data.register import LoginForm, RegisterForm
from data.finding_zodiac_aura import finding_aura, finding_zodiac
from data import db_session
from data.users import User

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init('db/blogs.sqlite')

    @app.route('/')
    @app.route('/profile')
    def profile():
        return

    @app.route('/ether')
    def ether():
        pass

    @app.route('/horoscope')
    def horoscope():
        return render_template('horoscope.html')

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

    @login_manager.user_loader
    def load_user(user_id):
        session = db_session.create_session()
        return session.query(User).get(user_id)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            user = session.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect('/')
            return render_template('login.html', message='Неправильный пароль или логин', form=form)
        return render_template('login.html', title='Авторизация', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
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