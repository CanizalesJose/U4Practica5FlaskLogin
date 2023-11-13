from flask import Flask, render_template, redirect, request, url_for, flash, get_flashed_messages
from flask_mysqldb import MySQL
from models.ModelUsers import ModelUsers
from models.entities.users import User
from config import config

app = Flask(__name__)
db = MySQL(app)

@app.route("/")
def index():
    return redirect("login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User(0, request.form['username'], request.form['password'],0)
        logged_user = ModelUsers.login(db, user)

        if logged_user != None:
            return redirect(url_for("home"))
        else:
            flash("Acceso rechazado...")
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")

@app.route("/home")
def home():
    return render_template("auth/home.html")
if __name__ == '__main__':
    app.config.from_object(config['development'])

    app.run()