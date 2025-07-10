# 🔐 Flask Auth System with MongoDB

A simple yet secure user authentication system built using **Flask**, **MongoDB**, and **bcrypt**. It includes user **signup**, **login**, **password validation**, **CAPTCHA**, and **session-based welcome page**.

## 📁 Folder Structure

auth-system/
│
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
│
├── templates/ # HTML Templates
│ ├── index.html
│ ├── login.html
│ ├── signup.html
│ └── welcome.html
│
├── static/
│ ├── css/
│ │ └── style.css # Styling for signup/login forms
│ └── js/
│ └── script.js # Password toggle & CAPTCHA logic



## 🚀 Features

- User Registration with:
  - Email uniqueness check
  - Strong password validation
  - CAPTCHA security
  - Password hashing with bcrypt
- User Login with secure session
- Flash messages for user feedback
- Welcome screen after login
- Logout functionality

## 🔧 Technologies Used

- **Python 3**
- **Flask**
- **MongoDB**
- **Jinja2**
- **bcrypt**
- **Flask-Session**
- **HTML, CSS, JavaScript**

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/auth-system.git
cd auth-system
2. Create a Virtual Environment (optional but recommended)
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
3. Install the Dependencies
pip install -r requirements.txt
4. Start MongoDB Locally
Make sure you have MongoDB installed and running:

mongod
The app connects to MongoDB at mongodb://localhost:27017/user_auth_project

5. Run the Application
python app.py
Now open your browser and visit:

http://localhost:5000
🔐 Password Rules
During signup, the password must:

Be at least 8 characters long

Contain 1 uppercase, 1 lowercase, and 1 special character

CAPTCHA is also required to protect against bots.

✍️ Author
Abdullah Abid
A 4th-semester Computer Science student building real-world full-stack projects.
Connect on LinkedIn