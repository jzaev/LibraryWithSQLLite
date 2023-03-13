from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
all_books = []


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", library=all_books)


@app.route("/add", methods=['POST', "GET"])
def add():
    if request.method == "POST":
        book_name = request.form['book_name']
        book_author = request.form['book_author']
        book_rating = request.form['book_rating']
        # all_books.append({"title": book_name, "author": book_author, "rating": book_rating})
        new_book = Book(name=book_name, author=book_author, rating=book_rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect("/")
    return render_template("add.html")


@app.route("/edit", methods=['POST', "GET"])
def edit():
    if request.method == "POST":
        book_rating = request.form['book_rating']
        current_book = Book.query.get(request.args["book_id"])
        current_book.rating = book_rating
        db.session.commit()
        return redirect("/")
    if request.method == "GET":
        if request.args["action"] == 'del':
            current_book = Book.query.get(request.args["book_id"])
            db.session.delete(current_book)
            db.session.commit()
            return redirect("/")
        elif request.args["action"] == "edit":
            return render_template("edit.html")


if __name__ == "__main__":
    app.run(debug=True)
