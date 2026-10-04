from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "feedback.db"


def init_db():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        return "All fields are required.", 400

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO feedback (name, email, message)
        VALUES (?, ?, ?)
    """, (name, email, message))

    connection.commit()
    connection.close()

    return redirect(url_for("success"))


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/responses")
def responses():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email, message
        FROM feedback
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return render_template(
        "responses.html",
        responses=data
    )

@app.route("/health")
def health():
    return {
        "status": "healthy",
        "application": "Student Feedback Management System"
    }


if __name__ == "__main__":
    init_db()
    app.run(debug=True)