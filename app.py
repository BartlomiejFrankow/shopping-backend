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


# Get all notes
@app.route('/getNotes', methods = ['GET'])
def get_shopping_notes():
    all_shopping_notes = ShoppingNotes.query.all()
    return jsonify(shopping_notes_schema.dump(all_shopping_notes))


# Get single note
@app.route('/getNote/<id>/', methods = ['GET'])
def note_detail(id):
    note = ShoppingNotes.query.get(id)
    return shopping_note_schema.jsonify(note)


# Add note
@app.route('/addNote', methods = ['POST'])
def add_shopping_note():
    title = request.json['title']
    body = request.json['body']

    note = ShoppingNotes(title, body)   

    db.session.add(note)
    db.session.commit()
    return shopping_note_schema.jsonify(note)


# Update note
@app.route('/updateNote/<id>/', methods = ['PUT'])
def update_note(id):
    note = ShoppingNotes.query.get(id)

    title = request.json['title']
    body = request.json['body']

    note.title = title
    note.body = body

    db.session.commit()
    return shopping_note_schema.jsonify(note)


# Delete note
@app.route('/delete/<id>/', methods = ['DELETE'])
def delete_note(id):
    note = ShoppingNotes.query.get(id)

    db.session.delete(note)
    db.session.commit()

    return shopping_note_schema.jsonify(note)


if __name__ == "__main__":
    app.run(debug = True)
