# pip install requests
# pip install flask
# pip install sqlalchemy

from requests import get
from pprint import pprint
from data.for_database import Films, Genres, Sessions
from data import db_session
from flask import Flask, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def add_film(id, title, genre, description, duration, year, img):
    genres = {'комедия': 0, 'мультфильм': 1, 'ужасы': 2, 'фантастика': 3, 'триллер': 4, 'боевик': 5, 'мелодрама': 6,
              'детектив': 7, 'приключения': 8, 'фентези': 9, 'военный': 10, 'семейный': 11, 'аниме': 12,
              'исторические': 13, 'драма': 14, 'документальные': 15, 'детские': 16, 'криминал': 17, 'биографии': 18,
              'вестерны': 19, 'фильмы-нуар': 20, 'спортивные': 21, 'реальное ТВ': 22, 'короткометражки': 23,
              'концерт': 24, 'музыкальные': 25, 'мюзиклы': 26, 'ток-шоу': 27, 'новости': 28, 'игры': 29,
              'церемонии': 30}

    film = Films()
    film.id = id
    film.title = title
    film.genre_id = genres[genre]
    film.description = description
    film.duration = duration
    film.year = year
    film.img = img
    return film

# добавить жанры
# def add_genre(id, name):
#     genre = Genres()
#     genre.id = id
#     genre.name = name
#     return genre
#
#
# db_session.global_init("db/films_database")
# db_sess = db_session.create_session()
# w1 = 'Комедии_Мультфильмы_Ужасы_Фантастика_Триллеры_Боевики_Мелодрамы_Детективы_Приключения_Фентези_Военные_Семейные'
# w2 = 'Аниме_Исторические_Драмы_Документальные_Детские_Криминал_Биографии_Вестерны_Фильмы-нуар_Спортивные_Реальное ТВ'
# w3 = 'Короткометражки_Концерты_Музыкальные_Мюзиклы_Ток-шоу_Новости_Игры_Церемонии'
# all_w = w1.split('_') + w2.split('_') + w3.split('_')
# d = dict()
# for i in range(len(all_w)):
#     d[all_w[i]] = i
# print(d)
# for i in range(len(all_w)):
#     db_sess.add(add_genre(i, all_w[i]))
# db_sess.commit()
# app.run()



headers = {
        'X-API-KEY': '',
        'Content-Type': 'application/json',
    }

params = {
    'type': 'TOP_100_POPULAR_FILMS',
    'page': 1
}

result = get('https://kinopoiskapiunofficial.tech/api/v2.2/films/top', headers=headers, params=params).json()

pprint(result)
ids = []
for film in result['films']:
    ids.append(film['filmId'])

db_session.global_init("db/films_database")
db_sess = db_session.create_session()

for id in ids:
    try:
        result = get(f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}', headers=headers).json()
        print('проверка', id, result)
        print(result['kinopoiskId'], result['nameRu'], result['genres'][0]['genre'],
              result['description'].replace(u'\xa0', ' '), result['filmLength'], result['startYear'], result['posterUrl'])
        db_sess.add(add_film(result['kinopoiskId'], result['nameRu'], result['genres'][0]['genre'],
                         result['description'].replace(u'\xa0', ' '), result['filmLength'], result['startYear'], result['posterUrl']))
    except Exception as error:
        print(error)

db_sess.commit()
app.run()
