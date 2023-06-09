from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/ai-chat-db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)


# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     book = db.Column(db.String(120), nullable=False)
#     characters = db.Column(db.String(200), nullable=False)
#     description = db.Column(db.String(120), nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False,
#                            default=datetime.utcnow)

#     def __repr__(self):
#         return f'Book: {self.description}'

#     def __init__(self, description):
#         self.description = description


# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     email = db.Column(db.String, unique=True)

#     def __repr__(self):
#         return f'<User(name={self.name}, email={self.email})>'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(120), nullable=False)
    characters = db.Column(db.String(200), nullable=False)
    handle = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return f'Book: {self.book}'

    def __init__(self, book, characters, handle):
        self.book = book
        self.characters = characters
        self.handle = handle


def format_book(book):
    return {
        'book': book.book,
        'characters': book.characters,
        'handle': book.handle,
        'id': book.id,
        'created_at': book.created_at
    }


@app.route('/books', methods=['POST'])
def create_book():
    book = request.json['book']
    characters = request.json['characters']
    newBook = Book(book, characters)
    db.session.add(newBook)
    db.session.commit()
    return format_book(newBook)

# get all books


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.order_by(Book.id.desc()).all()
    book_list = []
    for book in books:
        book_list.append(format_book(book))
    return {'book': book_list}

# get a single book


@app.route('/books/<handle>', methods=['GET'])
def get_book(handle):
    book = Book.query.filter_by(handle=handle).first()
    return {'book': format_book(book)}


# delete an book
@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    return f'Book (id: {id}) deleted'

# update an book


@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.filter_by(id=id).first()
    book.book = request.json['book']
    book.characters = request.json['characters']
    db.session.commit()
    return format_book(book)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run()
