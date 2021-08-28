from flask import Flask
from flask import render_template
from flask import request
from models import User, MultipleChoice, TermQuestion, Lesson, Course, Question
from tools import next_id
import json

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

@app.route("/search")
def search():
    # do some searching, probably accepting GET/POST params
    return render_template("search.html")

@app.route("/api/create/lesson", methods=["POST"])
def create_lesson():
    username = request.form["username"]
    password = request.form["password"]
    if username in users and users[username].password == password:
      name = request.form["name"]
      questions = json.loads(request.form["questions"])
      questions_parsed = []
      for question in questions:
        # question = { type: ..., args: ...}
        questions_parsed.append(Question(question["type"], question["args"]))
      create_new_lesson(name, users[username], questions_parsed)

def create_new_lesson(name, user: User, questions: list):
    id = next_id(Lesson, lessons)
    lessons[id] = Lesson(name, user, questions, id)


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
