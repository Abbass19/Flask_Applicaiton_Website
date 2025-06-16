from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from doctest import debug
from datetime import timedelta

from sqlalchemy.orm import backref

Troubleshooting = True

app = Flask(__name__)
app.secret_key = "Mera7aba Dawle"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=10)


db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column("id",db.Integer, primary_key= True)
    first_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    Notes = db.relationship('Note', backref='user', lazy=True)

    def __init__(self, first_name, email, password):
        self.first_name = first_name
        self.email = email
        self.password = password


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id


@app.route("/Signup/" , methods = ["POST", "GET"])
@app.route("/signup", methods = ["POST", "GET"])
def SignUp():
    if request.method== "POST":

        input_email = request.form["email"]
        input_first_name = request.form["first_name"]
        input_password = request.form["password"]
        input_confirm = request.form["confirm_password"]

        if input_password== input_confirm:
            #Also check if the user email is present before
            new_user = Users(email=input_email, first_name=input_first_name, password= input_password)
            db.session.add(new_user)
            db.session.commit()
            session["email"] = input_email
            session["first_Name"] = input_first_name
            flash("Signed In Successfully !! ")
            #Troubleshooting
            if Troubleshooting:
                print(f"Account created by mail :{input_email}, Password{input_password}")
            return render_template("login.html")

    if request.method == "GET":
        return render_template("signup.html")



@app.route("/Login/" , methods = ["POST", "GET"])
@app.route("/login/" , methods = ["POST", "GET"])
@app.route("/Login" , methods = ["POST", "GET"])
@app.route("/login" , methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        input_email = request.form.get("email", "").strip()
        input_password = request.form.get("password", "").strip()

        #Dealing With Empty Credentials
        if input_email.strip() == "" or input_password.strip() == "":
            if Troubleshooting:
                print(f"The email or password is empty : Sign in failed")
            flash("Email or Password cannot be empty", "error")
            return render_template("login.html")


        targeted_user = db.session.query(Users).filter_by(email= input_email).first()
        if targeted_user:
            if Troubleshooting:
                print(f"The email entered was found in the database (email :{input_email})")

            if targeted_user.password == input_password:
                if Troubleshooting:
                    print("Correct Password. Now we have to Navigate to Home.")

                session["email"] = input_email
                flash("Logged In Successfully")
                return redirect(url_for("Home"))
            else:
                if Troubleshooting:
                    print("Wrong Password. You need to go again to the Login Page and Try")
                flash("Wrong Password", "error")
                return render_template("login.html")
        else:
            if Troubleshooting:
                print("This email doesn't exist, You can Sign up!")
                print("Here are the emails that exist")
                for user in db.session.query(Users).all():
                    print(f" user Name : {user.first_name} email:{user.email}")
            flash("This email doesn't exist, You should Sign up! ", "error")
            return render_template("login.html")


    if request.method == "GET":
        if Troubleshooting:
            print(f"We are Troubleshooting Here !! ")

        if session.get("email"):
            print(f"The session email is {session.get("email")}")
            flash("You are already Singed In")
            return redirect(url_for("Home"))
        else:
            return render_template("login.html")


@app.route("/Logout/" , methods = ["GET"])
@app.route("/logout/" , methods = ["GET"])
def logout():
    print("Here is the Logout procedure")
    print(f"Session email before logout :{session.get("email")}")
    if session.get("email"):
        session.pop("email")

    print(f"Session email after logout :{session.get("email")}")

    return render_template("login.html")


@app.route("/Home/", methods=["POST", "GET"])
@app.route("/home/" , methods = ["POST", "GET"])
@app.route("/Home" , methods = ["POST", "GET"])
@app.route("/home" , methods = ["POST", "GET"])
def Home():
    if request.method == "POST":
        our_user = db.session.query(Users).filter_by(email=session.get("email")).first()
        user_id =  our_user.id
        input_note_String = request.form["User_Note"]
        input_Note = Note(input_note_String, user_id = user_id)
        db.session.add(input_Note)
        db.session.commit()
        notes = db.session.query(Note).filter_by(user_id=our_user.id).all()

        if Troubleshooting:
            print(f"The Message being added to the Database is {input_note_String}")
            print(f"Printing All Notes for {session.get("email")}")
            for note in notes:
                print(f"{note.content}")


        return render_template("Home.html", Notes=notes)

    if request.method == "GET":
        print("This is a GET Request")
        if  session.get("email"):
            our_user = db.session.query(Users).filter_by(email=session.get("email")).first()
            notes = db.session.query(Note).filter_by(user_id = our_user.id).all()
            return render_template("Home.html", Notes=notes)
        else:
            return render_template("login.html")


if __name__=="__main__":
    with app.app_context(): db.create_all()
    app.run(debug= True)


