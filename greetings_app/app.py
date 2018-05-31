import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']

db = SQLAlchemy(app)
db.create_all()


class Stranger(db.Model):
    name = db.Column(db.String(80), unique=True,
                     nullable=False, primary_key=True)
    counter = db.Column(db.Integer, nullable=False)


def get_max(all_strangers):
    max_stranger = Stranger(name='', counter=0)
    for stranger in all_strangers:
        if max_stranger.counter < stranger.counter:
            max_stranger = stranger
    return max_stranger


def get_stranger(name):
    stranger = Stranger.query.filter_by(name=name).first()
    return stranger if stranger else Stranger(name=name, counter=0)


def get_all_strangers():
    return Stranger.query.all()


def update_stranger(stranger, db):
    stranger.counter += 1
    db.session.add(stranger)
    db.session.commit()


@app.route('/', methods=["GET", "POST"])
def greetings():
    if request.method == 'POST':
        new_greeting_from = request.form['name']
        stranger = get_stranger(new_greeting_from)
        update_stranger(stranger, db)

    strangers = get_all_strangers()
    return render_template('index.j2', strangers=strangers,
                           max_stranger=get_max(strangers))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
