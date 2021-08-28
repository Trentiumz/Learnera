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


@app.route("/practice", methods=["GET"])
def practice():
    if "lesson" in request.args and int(request.args["lesson"]) in lessons:
        return render_template("practice.html",
                               ids=json.dumps([int(request.args["lesson"])]))
    elif "course" in request.args and int(lessons["course"]) in courses:
        return render_template(
            "practice.html",
            ids=json.dumps([
                lesson.id for lesson in courses[int(lessons["course"]).lessons]
            ]))
    else:
        abort(404)


@app.route("/account")
def account():
    return render_template("account.html")


@app.route("/search")
def search():
    query = request.args.get("query")
    if query is None or query == "":
        return render_template("error.html",
                               message=f"Please enter a search term")
    # do some searching, probably accepting GET/POST params
    results = [
        Lesson("Addition", User("User 3", "qwerty"), [], 0),
        Course("Grade 9 Biology", User("User 5", "password123"), [], 1),
        Course("Grade 2 Math", User("User 9", "agoodpassword"), [], 2),
        Lesson("Logarithms", User("User 10", "qwertyuiop"), [], 3)
    ]  # example results
    return render_template("search.html",
                           query=query,
                           results=results,
                           type_=type)


# TEMPORARY, JUST FOR MAKING FRONT END
@app.route("/editlesson")
def edit_lesson():
    return render_template("edit_lesson.html")


@app.route("/lesson/<id>")
def lesson_details(id=None):
    if id in lessons:
        lesson = lessons[id]
        return render_template("lesson_details",
                               name=lesson.name,
                               author=lesson.made_by.username,
                               questions=lesson.questions,
                               id=id)
    abort(404)


@app.route("/api/lesson_details")
def get_lesson():
    id = request.args.get("id")
    if id in lessons:
        lesson = lessons[id]
        return json.dumps({
            "name": lesson.name,
            "author": lesson.made_by.username,
            "questions": json.dumps(lesson.questions)
        })
    return ""


@app.route("/api/question_list", methods=["POST"])
def get_question_list():
    print(request.form["ids"])
    ids = json.loads(request.form["ids"])
    question_list = []
    for id in ids:
        if id in lessons:
            lesson = lessons[id]
            for question in lesson.questions:
                question_list.append(question)
    return json.dumps([{
      "question_type": question.question_type,
      "args": question.args
    } for question in question_list])


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
    users["tester"] = User("tester", "password")
    create_new_lesson(
        "sample", users["tester"],
        [Question("term", {
            "question_text": "who is I",
            "answer": "myself"
        })])
    print(lessons)
    app.run(host="0.0.0.0", port=3000)
