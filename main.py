from flask import Flask
from flask import render_template
from flask import request
from models import User, MultipleChoice, TermQuestion, Lesson, Course, Question
from tools import next_id

app = Flask(__name__, template_folder="./templates", static_folder="./static")

users = {}  # { username: User }
lessons = {}  # { lesson_id: Lesson }
courses = {}  # { course_id: Course }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/practice")
def practice():
    return render_template("practice.html")


@app.route("/api/create/lesson")
def create_lesson():
    pass


def create_new_lesson(name, user, questions: list):
    id = next_id(Lesson, lessons)
    lessons[id] = Lesson(name, user, questions, id)


@app.route("/api/create/question")
def create_question():
    pass


@app.route("/api/create/user", methods=["POST"])
def add_user():
    username = request.form["username"]
    password = request.form["password"]
    if username in users:
        return "Username Taken"
    else:
        users[username] = User(username, password)

@app.route("/api/checkuser", methods=["POST"])
def check_user():
    username = request.form["username"]
    password = request.form["password"]
    if username not in users or users[username].password != password:
      return "Username or Password is invalid"
    return "successfully logged in"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
