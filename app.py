from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from models import db
from models import User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'devopsdiggersecret'

app.config['SQLALCHEMY_DATABASE_URI'] = \
'sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        password_hash = generate_password_hash(
            request.form["password"]
        )

        user = User(
            firstname=request.form["firstname"],
            lastname=request.form["lastname"],
            mobile=request.form["mobile"],
            age=request.form["age"],
            gender=request.form["gender"],
            education=request.form["education"],
            email=request.form["email"],
            username=request.form["username"],
            password=password_hash
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful")

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):
            login_user(user)

            return redirect(
                url_for("dashboard")
            )

        flash("Invalid Credentials")

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html"
    )

@app.route("/calculator")
@login_required
def calculator():
    return render_template(
        "calculator.html"
    )

@app.route("/calculate", methods=["POST"])
@login_required
def calculate():

    score = 0

    os_choice = request.form["os"]
    cloud = request.form["cloud"]
    admin = request.form["admin"]

    if os_choice == "Linux":
        score += 5
    elif os_choice == "Windows":
        score += 3
    else:
        score += 2

    if cloud == "AWS":
        score += 15
    elif cloud == "Azure":
        score += 12
    elif cloud == "GCP":
        score += 12

    if admin == "Linux":
        score += 5
    else:
        score += 3

    skill_fields = [
        "jenkins",
        "git",
        "ansible",
        "docker",
        "prometheus",
        "terraform"
    ]

    values = {
        "jenkins":10,
        "git":5,
        "ansible":10,
        "docker":25,
        "prometheus":10,
        "terraform":15
    }

    for skill in skill_fields:

        if request.form.get(skill) == "Yes":
            score += values[skill]

    experience = int(
        request.form["experience"]
    )

    multiplier = 1

    if experience <= 2:
        multiplier = 1

    elif experience <= 5:
        multiplier = 1.5

    elif experience <= 8:
        multiplier = 2.5

    elif experience <= 12:
        multiplier = 4

    elif experience <= 15:
        multiplier = 6

    elif experience <= 20:
        multiplier = 8

    else:
        multiplier = 10

    salary = (
        300000 +
        (score * 50000)
    ) * multiplier

    salary = min(
        max(salary,300000),
        7000000
    )

    return render_template(
        "result.html",
        salary=salary,
        score=score,
        experience=experience
    )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
