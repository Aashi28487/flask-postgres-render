from flask import Flask, render_template, request, redirect
from db import get_connection
from db import create_students_table
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.before_request
def init_db():
    try:
        create_students_table()
    except Exception as e:
        print(f"Database initialization error: {e}")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (name, email) VALUES (%s, %s)",
            (name, email)
        )
        conn.commit()
        cur.close()
        conn.close()

        return redirect("/students")

    return render_template("add_student.html")

@app.route("/students")
def students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, email FROM students")
    data = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("students.html", students=data)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_ENV") == "development")

