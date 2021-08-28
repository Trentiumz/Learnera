from flask import Flask
from flask import render_template, redirect, abort
from flask import request
from models import User, Package, Page
from tools import next_id
import urllib
import json

app = Flask(__name__, template_folder="./templates", static_folder="./static")

users = {}  # { username: User }
packages = {}  # { package_id: Package }


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


@app.route("/review", methods=["GET"])
def review():
    if "package" in request.args and int(request.args["package"]) in packages:
        return render_template("review.html", id=int(request.args["package"]))
    else:
        abort(404)


@app.route("/account/<username>")
def account(username):
    if username in users:
      return render_template("account.html", packages=users[username].packages)
    abort(404)


@app.route("/search")
def search():
    query = request.args.get("query")
    if query is None or query == "":
        return render_template("error.html",
                               message=f"Please enter a search term")
    # do some searching, probably accepting GET/POST params
    results = [
        Package("Addition", User("User 3", "qwerty"), [], 0),
        Package("Logarithms", User("User 10", "qwertyuiop"), [], 3)
    ]  # example results
    return render_template("search.html",
                           query=query,
                           results=results,
                           type_=type)


# TEMPORARY, JUST FOR MAKING FRONT END
@app.route("/editpackage")
def edit_package():
    return render_template("edit_package.html")


@app.route("/package/<id>")
def package_details(id=None):
    id = int(id)
    if id in packages:
        package = packages[id]
        return render_template("package_details.html",
                               name=package.name,
                               author=package.made_by.username,
                               pages=package.pages,
                               id=id)
    abort(404)


@app.route("/api/package_details")
def get_package():
    id = request.args.get("id")
    if id in packages:
        package = packages[id]
        return json.dumps({
            "name": package.name,
            "author": package.made_by.username,
            "pages": json.dumps(package.pages)
        })
    return ""


@app.route("/api/content_list", methods=["POST"])
def get_content_list():
    id = int(request.form["id"])
    page_list = []
    if id in packages:
        package = packages[id]
        for page in package.pages:
            page_list.append(page)
    return json.dumps([{
        "type": page.type,
        "args": page.args
    } for page in page_list])


@app.route("/api/create/package", methods=["POST"])
def create_package():
    username = request.form["username"]
    password = request.form["password"]
    if username in users and users[username].password == password:
        name = request.form["name"]
        pages = json.loads(request.form["pages"])
        pages_parsed = []
        for page in pages:
            # page = { type: ..., args: ...}
            pages_parsed.append(Page(page["type"], page["args"]))
        create_new_package(name, users[username], pages_parsed)


def create_new_package(name, user: User, pages: list):
    id = next_id(Package, packages)
    packages[id] = Package(name, user, pages, id)
    user.add_package(packages[id])


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


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


if __name__ == "__main__":
    users["tester"] = User("tester", "password")
    create_new_package("sample", users["tester"], [
        Page("content",
             {"file": "http://www.africau.edu/images/default/sample.pdf"}),
        Page(
            "questions", {
                "questions": [{
                    "type": "mc",
                    "question_text":
                    "Who is my favourite food eating guinea pig",
                    "choices": ["bobby", "tommy", "alex"],
                    "correct_choice": "bobby"
                }, {
                    "type": "term",
                    "question_text":
                    "There once was a giant big bird called: ",
                    "answer": "fred"
                }]
            }),
        Page(
            "content", {
                "file":
                "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
            })
    ])
    print(packages)
    app.run(host="0.0.0.0", port=3000)
