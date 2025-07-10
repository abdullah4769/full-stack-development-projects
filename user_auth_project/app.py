from flask import Flask, render_template, request, redirect, session, url_for, flash
# from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from flask_session import Session
import re
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
# app.secret_key = "your_secret_key_here"  # replace with a strong secret key

app.secret_key = "MyStrongSecretKey123!@#"
app.config["MONGO_URI"] = "mongodb://localhost:27017/userAuthDB"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

mongo = PyMongo(app)

app.secret_key = "supersecretkey"  # For session
client = MongoClient("mongodb://localhost:27017/")
db = client["user_auth_project"]
users_collection = db["users"]

@app.route("/signup", methods=["GET"])
def show_signup():
    return render_template("signup.html")

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = users_collection.find_one({"email": email})

        if user:
            # Check password (hashed)
            if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
                # Save username in session for welcome page
                session["username"] = user["username"]
                flash("Login successful!", "success")
                return redirect(url_for("welcome"))
            else:
                flash("Incorrect password.", "danger")
        else:
            flash("Email not found.", "danger")

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
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
        return redirect(url_for("login"))
    
    return render_template("signup.html")

@app.route("/welcome")
def welcome():
    if "username" in session:
        username = session["username"]
        return render_template("welcome.html", username=username)
    else:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
