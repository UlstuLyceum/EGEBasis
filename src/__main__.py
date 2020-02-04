from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login")
def login():
    return render_template("login.html", title="Войти")


@app.route("/signup")
def signup():
    return render_template("signup.html", title="Зарегистрироваться")


app.run(port=8000)
