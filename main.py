from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_user
import sqlite3
from datetime import date
from data.for_database import Films, Genres, Sessions, User
from data import db_session
from forms.user import RegisterForm, LoginForm
from PIL import Image, ImageDraw
from flask_login import login_user, login_required, logout_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()


@app.route('/delete_film', methods=['POST', 'GET'])
def delete_film():
    global db_sess
    params = dict()
    params['Page_title'] = 'Управление фильмами'
    if request.method == 'GET':
        film_titles = []
        for film in db_sess.query(Films):
            film_titles.append(film.title)
        film_titles.sort()
        params['titles'] = film_titles
        return render_template('delete_film.html', **params)
    elif request.method == 'POST':
        db_sess = db_session.create_session()
        for film in db_sess.query(Films).filter(Films.title == request.form['title']):
            db_sess.delete(film)
        db_sess.commit()
        return show_films()


@app.route('/delete_session', methods=['POST', 'GET'])
def delete_session():
    global db_sess
    params = dict()
    params['Page_title'] = 'Управление сеансами'
    if request.method == 'GET':
        film_titles = []
        for film in db_sess.query(Films):
            film_titles.append(film.title)
        film_titles.sort()
        params['titles'] = film_titles
        return render_template('delete_session.html', **params)
    elif request.method == 'POST':
        for film in db_sess.query(Films).filter(Films.title == request.form['film']):
            id_film = int(film.id)
        db_sess = db_session.create_session()
        for session in db_sess.query(Sessions).filter(
                Sessions.id_film == id_film and Sessions.date == request.form['date'] and Sessions.time ==
                request.form['time']):
            db_sess.delete(session)
        db_sess.commit()
        return show_films()


@app.route('/add_session', methods=['POST', 'GET'])
def add_session():
    global db_sess
    params = dict()
    params['Page_title'] = 'Управление сеансами'
    if request.method == 'GET':
        film_titles = []
        for film in db_sess.query(Films):
            film_titles.append(film.title)
        film_titles.sort()
        params['titles'] = film_titles
        return render_template('add_session.html', **params)
    elif request.method == 'POST':
        print(request.form)
        session = Sessions()
        for film in db_sess.query(Films).filter(Films.title == request.form['film']):
            session.id_film = int(film.id)
        session.date, session.time = request.form['date'], request.form['time']
        session.amount, session.cost = int(request.form['amount']), int(request.form['cost'])
        session.id = int(request.form['id'])
        db_sess = db_session.create_session()
        db_sess.add(session)
        db_sess.commit()
        return show_films()


@app.route('/add_film', methods=['POST', 'GET'])
def add_film():
    params = dict()
    params['Page_title'] = 'Управление фильмами'
    if request.method == 'GET':
        return render_template('add_film.html', **params)
    elif request.method == 'POST':
        film = Films()
        genres = {'комедия': 0, 'мультфильм': 1, 'ужасы': 2, 'фантастика': 3, 'триллер': 4, 'боевик': 5, 'мелодрама': 6,
                  'детектив': 7, 'приключения': 8, 'фентези': 9, 'военный': 10, 'семейный': 11, 'аниме': 12,
                  'исторические': 13, 'драма': 14, 'документальные': 15, 'детские': 16, 'криминал': 17, 'биографии': 18,
                  'вестерны': 19, 'фильмы-нуар': 20, 'спортивные': 21, 'реальное ТВ': 22, 'короткометражки': 23,
                  'концерт': 24, 'музыкальные': 25, 'мюзиклы': 26, 'ток-шоу': 27, 'новости': 28, 'игры': 29,
                  'церемонии': 30}
        film.id, film.title, film.genre_id = int(request.form['id']), request.form['title'], genres[request.form['genre'].lower()]
        film.description, film.duration = request.form['description'], int(request.form['duration'])
        film.img, film.year = request.form['img'], int(request.form['year'])
        db_sess = db_session.create_session()
        db_sess.add(film)
        db_sess.commit()
        return show_films()


@app.route('/test_page')
def test():
    params = dict()
    params['Page_title'] = 'test'
    return render_template('base.html', **params)


@app.route('/')
@app.route('/all_films')
def show_films():
    global db_sess
    params = dict()
    params['Page_title'] = 'Все доступные сеансы'
    params['Sessions'] = dict()
    params['Dates'] = []

    today = str(date.today())
    for session in db_sess.query(Sessions).filter(Sessions.date >= today):
        id = session.id_film
        for film in db_sess.query(Films).filter(Films.id == id):
            res = [session.time, session.cost, session.amount]
            if not session.date in params['Sessions']:
                params['Sessions'][session.date] = {}
                params['Dates'].append(session.date)
            if not session.id_film in params['Sessions'][session.date]:
                params['Sessions'][session.date][session.id_film] = [film.img, film.title, film.description, []]
            params['Sessions'][session.date][session.id_film][3].append(res)
            params['Sessions'][session.date][session.id_film][3].sort(key=lambda x: x[0])
    params['Dates'].sort()
    print(params['Sessions'])
    return render_template('show_films.html', **params)


@app.route('/sessions/<id>')
def sessions_for_one_film(id):
    global db_sess
    params = dict()
    params['Page_title'] = 'Сеансы для фильма'
    for film in db_sess.query(Films).filter(Films.id == id):
        for genre in db_sess.query(Genres).filter(Genres.id == film.genre_id):
            params['film_data'] = [film.img, film.title, film.description, film.duration, film.year, genre.name]
    params['sessions'] = {}
    params['dates'] = []
    for session in db_sess.query(Sessions).filter(Sessions.id_film == id):
        if not session.date in params['dates']:
            params['sessions'][session.date] = []
            params['dates'].append(session.date)
        params['sessions'][session.date].append([session.time, session.cost, session.amount])
        params['sessions'][session.date].sort(key=lambda x: x[0])
    return render_template('sessions.html', **params)


@app.route('/ticket/<time>/<date>/<places>/<price>/')
def ticket(time, date, places, price):
    global db_sess
    params = dict()
    params['Page_title'] = 'Сеансы для фильма'
    params['time'] = time
    params['date'] = date
    params['price'] = price
    params['places'] = places
    im = Image.open(r"static/img/cinema_ticket.png")
    draw_text = ImageDraw.Draw(im)
    draw_text.text(
        (100, 100),
        'Test Text',
        fill=('#1C0606')
    )
    params['img'] = im.show()
    im.show()
    return render_template('ticket.html', **params)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/films_database")
    db_sess = db_session.create_session()
    db_sess.commit()
    login_manager.init_app(app)
    app.run(port=8080, host='127.0.0.1')
