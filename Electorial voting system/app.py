from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Use environment variable in production. Local fallback for beginner usage.
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-for-local-testing")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False  # set to True after you use HTTPS in production
)

# Simple in-memory user store
users = {}  # {username: {"password_hash": "..."}}

@app.route("/")
def index():
    return render_template("index.html", username=session.get("username"))

@app.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        if not username or not password:
            flash("Username and password required.")
            return redirect(url_for("register"))
        if username in users:
            flash("Username already exists.")
            return redirect(url_for("register"))
        users[username] = {"password_hash": generate_password_hash(password)}
        flash("Registered — please log in.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        user = users.get(username)
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["username"] = username
            flash("Logged in.")
            return redirect(url_for("index"))
        flash("Incorrect username or password.")
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
