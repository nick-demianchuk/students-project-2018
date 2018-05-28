import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']

db = SQLAlchemy(app)

class Stranger(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    counter =db.Column(db.Integer, nullable=False)

db.create_all()

@app.route('/', methods=["GET", "POST"])
def greetings():
    if request.method == 'POST':
        new_greeting_from = request.form['name']
        
        stranger = Stranger.query.filter_by(name=new_greeting_from).first()

        if not stranger:
            stranger = Stranger(name=new_greeting_from, counter=0)
        stranger.counter += 1

        db.session.add(stranger)
        db.session.commit()

    strangers = Stranger.query.all()
    return render_template('index.j2', strangers=strangers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
