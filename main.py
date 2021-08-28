from flask import Flask
from flask import render_template, redirect, abort
from flask import request
from models import User, MultipleChoice, TermQuestion, Lesson, Course, Question
from tools import next_id
import urllib
import json

app = Flask(__name__, template_folder="./templates", static_folder="./static")

users = {}  # { username: User }
lessons = {}  # { lesson_id: Lesson }
courses = {}  # { course_id: Course }


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/instructions")
def instructions():
  return render_template("instructions.html")

@app.route("/login")
def login():
    if "message" in request.args:
        return render_template("login.html", message=request.args["message"])
    return render_template("login.html")


@app.route("/register")
def register():
    if "message" in request.args:
        return render_template("register.html",
                               message=request.args["message"])
    return render_template("register.html")


@app.route("/account")
def practice():
    return render_template("account.html")


@app.route("/search")
def search():
    query = request.args.get("query")
    if query is None or query == "":
        return render_template("error.html", message=f"Please enter a search term")
    # do some searching, probably accepting GET/POST params
    results = [
        Lesson("Addition", "User 2", [], 0),
        Course("Grade 9 Biology", "User 5", [], 1),
        Course("Grade 2 Math", "User 9", [], 2),
        Lesson("Logarithms", "User 10", [], 3)
    ]  # example results
    return render_template("search.html",
                           query=query,
                           results=results,
                           type_=type)


@app.route("/lesson/<id>")
def lesson_details(id=None):
  if id in lessons:
    lesson = lessons[id]
    return render_template("lesson_details", name=lesson.name, author=lesson.made_by.username, questions=lesson.questions)
  abort(404)
  

@app.route("/api/lesson_details")
def get_lesson():
    id = request.args.get("id")
    if id in lessons:
        lesson = lessons[id]
        return json.dumps({
            "name":
            lesson.name,
            "author":
            lesson.made_by.username,
            "questions":
            json.dumps(lesson.questions)
        })
    return ""


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
            questions_parsed.append(
                Question(question["type"], question["args"]))
        create_new_lesson(name, users[username], questions_parsed)


def create_new_lesson(name, user: User, questions: list):
    id = next_id(Lesson, lessons)
    lessons[id] = Lesson(name, user, questions, id)


@app.route("/api/create/user", methods=["POST"])
def add_user():
    username = request.form["username"]
    password = request.form["password"]
    if username in users:
        return redirect("/register?message=" +
                        urllib.parse.quote_plus("The username is taken"),
                        code=302)
    else:
        users[username] = User(username, password)
        return redirect("/login?message=" +
                        urllib.parse.quote_plus("You can now log in"),
                        code=302)


@app.route("/checkuser", methods=["POST"])
def check_user():
    username = request.form["username"]
    password = request.form["password"]
    if username not in users or users[username].password != password:
        return redirect(
            "/login?message=" +
            urllib.parse.quote_plus("The username or password is invalid"),
            code=302)
    return render_template("shorts/login_success.html",
                           username=username,
                           password=password)


@app.route("/api/checkuser", methods=["POST"])
def api_check_user():
    username = request.form["username"]
    password = request.form["password"]
    if username not in users or users[username].password != password:
        return "false"
    return "true"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
