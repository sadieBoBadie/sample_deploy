from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask_app.models.user import User
from flask import flash

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    if "user_id" not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect("/")
    
    user = User.get_by_id(session["user_id"])

    return render_template("home.html", user=user)

@app.route("/register", methods=["POST"])
def register():
    valid_user = User.create_valid_user(request.form)

    if not valid_user:
        return redirect("/")
    
    session["user_id"] = valid_user.id
    
    return redirect("/home")

@app.route("/login", methods=["POST"])
def login():
    valid_user = User.authenticated_user_by_input(request.form)
    if not valid_user:
        return redirect("/")

    session["user_id"] = valid_user.id
    return redirect("/home")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")