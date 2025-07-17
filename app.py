from flask import Flask, request, render_template
import sqlite3
import authentication

user = authentication.user
passkey = authentication.passkey

app = Flask(__name__)

#this is the root to serve registration form
@app.route("/")
def home():
    return render_template("registration.html")

#this is the root to collect the data from users
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    place = request.form["place"]
    age = request.form['age']
    mobile = request.form['mobile']
    course = request.form['course']
    email = request.form['email']
    gender = request.form['gender']
#hear writing collected data into students.db file
    con = sqlite3.connect("students.db")
    cursor = con.cursor()
    cursor.execute("""
        create table if not exists students (
            id integer primary key,
            name text not null,
            place text not null,
            age integer not null,
            mobile_number text not null,
            course text not null,
            email text not null,
            gender text not null
        )
    """)
    cursor.execute("""
        insert into students (name, place, age, mobile_number, course, email, gender)
        values (?, ?, ?, ?, ?, ?, ?)
    """, (name, place, age, mobile, course, email, gender))
    con.commit()
    con.close()
    return f"Thank you for registering {name}, your form is successful!"

#rendering verification page
@app.route("/verification", methods=["get"])
def verification_form():
    return render_template("admin_verification.html")

#root for user verification for   admin rights
@app.route("/verification", methods=["POST"])
def verification():
    user_id = request.form["userid"]
    password = request.form["password"]
    if user_id == user and password == passkey:
        return render_template("chat.html")
    else:
        return "Wrong credentials! Please provide a valid user ID and password."

#run the app
if __name__ == "__main__":
    app.run(debug=True)
