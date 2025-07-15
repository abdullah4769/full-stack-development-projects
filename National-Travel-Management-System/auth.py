from flask import Flask,Blueprint, render_template, request, redirect, session, url_for, flash
# from flask_bcrypt import Bcrypt
# from flask_pymongo import PyMongo
# from flask_session import Session
from datetime import datetime 
import re
from pymongo import MongoClient
import bcrypt

auth_routes = Blueprint('auth', __name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["Abdullah(12)_travel_db"]
users_collection = db["users"]

form_collection =db["form_submissions"] 

@auth_routes.route("/signup", methods=["GET"])
def show_signup():
    return render_template("signup.html")

@auth_routes.route('/')
def home():
    return render_template('index.html')

# auth.py

@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = users_collection.find_one({"email": email})

        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
                session["username"] = user["username"]
                session["user_id"] = str(user["_id"])  # User ID سیشن میں محفوظ کریں
                flash("Login successful!", "success")
                return redirect(url_for("auth.welcome"))
            else:
                flash("Incorrect password.", "danger")
        else:
            flash("Email not found.", "danger")
    return render_template("login.html")


@auth_routes.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        username = request.form["username"].strip()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # 1. Check if email already exists
        if users_collection.find_one({"email": email}):
            flash("Email already exists. Please login or use another.", "danger")
            return redirect(url_for("signup"))

        # 2. Validate password strength
        import re
        pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,}$")
        if not pattern.match(password):
            flash("Password must be 8 characters, with upper, lower & special char.", "warning")
            return redirect(url_for("signup"))

        # 3. Check passwords match
        if password != confirm_password:
            flash("Passwords do not match.", "warning")
            return redirect(url_for("signup"))

        # 4. Hash password securely
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
         
        # 5. Save to MongoDB
        users_collection.insert_one({
            "email": email,
            "username": username,
            "password": hashed_password
        })

        flash("Account created successfully! Please login.", "success")
        return redirect(url_for("auth.login"))
    
    return render_template("signup.html")



@auth_routes.route('/welcome')
def welcome():
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login'))

    logged_in_username = session['username'] # Get username from session
    print(f"Welcome Page: Session mein username hai: '{logged_in_username}' (Type: {type(logged_in_username)})")

    # Fetch only bookings made by the specific logged-in user using 'booked_by_username'
    bookings = list(form_collection.find({'booked_by_username': logged_in_username}).sort("created_at", -1))

    print(f"Database Query: Is user '{logged_in_username}' ke liye {len(bookings)} bookings mili hain.")

    for booking in bookings:
        if '_id' in booking:
            booking['_id'] = str(booking['_id']) # Convert ObjectId to string

    return render_template('welcome.html', username=logged_in_username, bookings=bookings)

@auth_routes.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None) # Also remove user_id from session
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))