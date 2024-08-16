from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)


# Database connection helper
def get_db_connection():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    return conn


# Route to display homepage
@app.route("/")
def index():
    return render_template("index.html")


# Route to add a new book
@app.route("/add-book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        isbn = request.form["isbn"]
        published_year = request.form["published_year"]
        genre = request.form["genre"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO Books (title, author, isbn, published_year, genre) VALUES (?, ?, ?, ?, ?)",
            (title, author, isbn, published_year, genre),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("add_book.html")


# Route to add a new member
@app.route("/add-member", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO Members (first_name, last_name, email, phone_number) VALUES (?, ?, ?, ?)",
            (first_name, last_name, email, phone_number),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("add_member.html")


# Route to add a new loan
@app.route("/add-loan", methods=["GET", "POST"])
def add_loan():
    if request.method == "POST":
        book_id = request.form["book_id"]
        member_id = request.form["member_id"]
        loan_date = datetime.now()
        due_date = datetime.now() + timedelta(days=10)

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO Loans (book_id, member_id, loan_date, due_date) VALUES (?, ?, ?, ?)",
            (book_id, member_id, loan_date, due_date),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    conn = get_db_connection()
    books = conn.execute("SELECT * FROM Books").fetchall()
    members = conn.execute("SELECT * FROM Members").fetchall()
    conn.close()

    return render_template("add_loan.html", books=books, members=members)


if __name__ == "__main__":
    app.run(debug=True)
