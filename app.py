from flask import Flask, render_template, request, redirect, session, flash

from database import create_database
from auth import register_user, login_user
from vault import (
    get_dashboard_stats,
    add_credential,
    get_all_credentials,
    delete_credential
)

app = Flask(__name__)
app.secret_key = "vaultiq-secret-key"

create_database()


@app.route("/")
def home():
    return render_template("login.html")


# ---------------- REGISTER ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if register_user(username, password):

            flash("Registration successful. Please login.", "success")

            return redirect("/")

        flash("Username already exists.", "danger")

        return redirect("/register")

    return render_template("register.html")


# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    user_id = login_user(username, password)

    if user_id:

        session["user_id"] = user_id

        flash("Login successful.", "success")

        return redirect("/dashboard")

    flash("Invalid username or password.", "danger")

    return redirect("/")


# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    stats = get_dashboard_stats(session["user_id"])

    return render_template(
        "dashboard.html",
        stats=stats
    )


# ---------------- VAULT ---------------- #

@app.route("/vault")
def vault():

    if "user_id" not in session:
        return redirect("/")

    credentials = get_all_credentials(session["user_id"])

    return render_template(
        "vault.html",
        credentials=credentials
    )


# ---------------- ADD CREDENTIAL ---------------- #

@app.route("/add", methods=["GET", "POST"])
def add():

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        website = request.form["website"]
        email = request.form["email"]
        password = request.form["password"]
        notes = request.form["notes"]

        add_credential(
            session["user_id"],
            website,
            email,
            password,
            notes
        )

        flash("Credential added successfully.", "success")

        return redirect("/vault")

    return render_template("add_password.html")


# ---------------- DELETE ---------------- #

@app.route("/delete/<int:credential_id>")
def delete_credential_route(credential_id):

    if "user_id" not in session:
        return redirect("/")

    delete_credential(credential_id)

    flash("Credential deleted successfully.", "success")

    return redirect("/vault")


# ---------------- EDIT ---------------- #

@app.route("/edit/<int:id>")
def edit(id):

    return "Edit feature coming soon."


# ---------------- PASSWORD GENERATOR ---------------- #

@app.route("/generator")
def generator():

    if "user_id" not in session:
        return redirect("/")

    return render_template("generator.html")


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "info")

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)