from flask_sqlalchemy import SQLAlchemy

from resources import app

db = SQLAlchemy(app)


def commit():
    db.session.commit()


def add(obj, do_commit=True):
    db.session.add(obj)
    if do_commit:
        commit()


def remove(obj, do_commit=True):
    db.session.remove(obj)
    if do_commit:
        commit()


def create_all():
    db.create_all()
