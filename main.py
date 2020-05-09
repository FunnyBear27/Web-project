from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from data.register import LoginForm
from data import db_session
from data.users import User

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')