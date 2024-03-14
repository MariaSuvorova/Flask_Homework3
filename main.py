from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import CSRFProtect
from models import User, db
from forms import RegistrationForm
from werkzeug.security import generate_password_hash
import re


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c56cd00d1a08c65029f644cdba4002dc308eee2506f963bb6c7d88281fc2e229'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)
DB_NAME = 'users.db'


#  Функция для работы с БД из командной строки
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


#  Функция для работы с БД из командной строки
@app.cli.command("clear-db")
def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print(f'Очищена таблица: {table}')
        db.session.execute(table.delete())
    db.session.commit()


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/users/')
def all_users():
    users = User.query.all()
    context = {'users': users}
    return render_template('users.html', **context)


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data

        if User.query.filter_by(firstname=firstname).first() and User.query.filter_by(lastname=lastname).first():
            message = f'Пользователь с таким именем уже существует.'
            flash(message, 'error')
            return redirect(url_for('registration'))
        if User.query.filter_by(email=email).first():
            message = f'Пользователь с таким email адресом уже существует.'
            flash(message, 'error')
            return redirect(url_for('registration'))

        password = form.password.data
        password_hash = generate_password_hash(password)

        user = User(firstname=firstname, lastname=lastname, email=email, password=password_hash)
        db.session.add(user)
        db.session.commit()
        username = f'{firstname} {lastname}'
        message = f'Пользователь {username} успешно зарегистрирован.'
    
        flash(message, 'success')

    return render_template('registration.html', form=form)


# if __name__ == '__main__':
#     if DB_NAME not in os.listdir(os.path.abspath('instance/')):
#         init_db()
#     app.run(debug=True)