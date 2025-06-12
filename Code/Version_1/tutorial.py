from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from doctest import debug
from datetime import timedelta


Troubleshooting = True


app = Flask(__name__)
app.secret_key = "Mera7aba Dawle"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=10)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id",db.Integer, primary_key= True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email



@app.route("/")
def origin():
    return render_template("base.html")

@app.route("/<name>")
def home(name):
    return render_template("index.html", name=name)

@app.route("/login", methods= ["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        session ["user"] = user
        found_users = users.query.filter_by(name=user).first()
        if found_users:
            session["email"] = found_users.email
        else:
            if Troubleshooting:
                print(f"Adding a user {user}")
            usr = users(user, None)
            db.session.add(usr)
            db.session.commit()
        flash("Logged In Successful")
        return render_template("user.html", user= user)
    else:
        if "user" in session:
            return redirect(url_for("user"))
        flash("You are already Login In")
        return render_template("login.html")

@app.route("/user", methods= ["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_users = users.query.filter_by(name=user).first()
            found_users.email = email
            db.session.commit()
            flash("Email was saved")

        if request.method == "GET":
            if "email" in session:
                email = session["email"]
        return render_template("user.html", user = user,email= email)
    else:
        return(redirect(url_for("login")))

@app.route("/view")
def view():
    Users = users.query.all()
    if Troubleshooting:
        print(f" We have {len(Users)} users in the database")
        for user in Users:
            print(f"User  : {user.name}  , with email {user.email}")
    return render_template("view.html", values = Users)



@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You Logged Out {user}", "info")
    session.pop("user",None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__=="__main__":
    with app.app_context(): db.create_all()
    app.run(debug= True)
