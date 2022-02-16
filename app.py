from crypt import methods
from email.policy import default
from turtle import title
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/shopping'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow()


class ShoppingNotes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    date = db.Column(db.DateTime, default = datetime.datetime.now)


    def __init__(self, title, body):
        self.title = title
        self.body = body


class ShoppingNoteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')


shopping_note_schema = ShoppingNoteSchema()
shopping_notes_schema = ShoppingNoteSchema(many = True)


@app.route('/getShoppingNotes', methods = ['GET'])
def get_shopping_list():
    return jsonify(
        {
            "Hello" : "World"
        }
    )

@app.route('/addShoppingNotes', methods = ['POST'])
def add_shopping_notes():
    title = request.json['title']
    body = request.json['body']

    notes = ShoppingNotes(title, body)
    db.session.add(notes)
    db.session.commit()
    return shopping_note_schema.jsonify()

if __name__ == "__main__":
    app.run(debug = True)
