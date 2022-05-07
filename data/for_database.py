import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash


class Films(SqlAlchemyBase):
    __tablename__ = 'films'
    id = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    genre_id = sqlalchemy.Column(sqlalchemy.INT, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text)
    duration = sqlalchemy.Column(sqlalchemy.INT)
    img = sqlalchemy.Column(sqlalchemy.String)
    year = sqlalchemy.Column(sqlalchemy.INT)


class Genres(SqlAlchemyBase):
    __tablename__ = 'genres'
    id = sqlalchemy.Column(sqlalchemy.INT, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)


class Sessions(SqlAlchemyBase):
    __tablename__ = 'sessions'
    id = sqlalchemy.Column(sqlalchemy.INT, primary_key=True, autoincrement=True)
    id_film = sqlalchemy.Column(sqlalchemy.INT, nullable=False, unique=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    amount = sqlalchemy.Column(sqlalchemy.INT, nullable=False)
    cost = sqlalchemy.Column(sqlalchemy.INT, nullable=False)


class Sold_tickets(SqlAlchemyBase):
    __tablename__ = 'tickets'
    id = sqlalchemy.Column(sqlalchemy.INT, primary_key=True, autoincrement=True)
    id_film = sqlalchemy.Column(sqlalchemy.INT, nullable=False, unique=True)


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = password

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class LoginForm(FlaskForm):
    name = StringField('ФИО')
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')

