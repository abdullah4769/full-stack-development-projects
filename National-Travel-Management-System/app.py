from flask import Flask,redirect,url_for,render_template
from auth import auth_routes
from form_routes import form_routes

app = Flask(__name__)
app.secret_key = 'secret123'

@app.route("/")
def home():
    return redirect(url_for('auth.home'))  # ya auth.signup, ya koi homepage


app.register_blueprint(auth_routes, url_prefix="/auth")
app.register_blueprint(form_routes, url_prefix="/form")

@app.route('/about')
def about():
    return render_template('about.html')



if __name__ == '__main__':
    app.run(debug=True)
