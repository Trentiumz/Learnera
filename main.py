from flask import Flask
from flask import render_template, redirect, abort
from flask import request
from models import User, Package, Page, Room
from tools import next_id
import urllib
import json

app = Flask(__name__, template_folder="./templates", static_folder="./static")

users = {}  # { username: User }
packages = {}  # { package_id: Package }
rooms = {} # { room_id: Room }


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

@app.route("/room/<id>", methods=["GET"])
def room_details(id):
  id = int(id)
  if id in rooms:
    room = rooms[id]
    return render_template("room/room_details.html", id=room.id, name=room.name, owner=users[room.owner], users=[users[username] for username in room.invited if room.id in users[username].rooms], packages=[packages[id] for id in room.packages])
  else:
    abort(404)

@app.route("/account/<username>")
def account(username):
    if username in users:
      print(users[username].invitations)
      return render_template("account.html", packages=[packages[id] for id in users[username].packages], username=username, rooms=[rooms[id] for id in users[username].rooms], invitations=[rooms[id] for id in users[username].invitations])
    abort(404)


@app.route("/search")
def search():
    query = request.args.get("query")
    if query is None or query == "":
        return render_template("error.html",
                               message=f"Please enter a search term")
    words = [word.strip() for word in query.split(" ")]
    results = []
    for id in packages:
      package = packages[id]
      has_all = True
      for word in words:
        has_all = has_all and word in package.name
      if has_all:
        results.append(package)

    for username in users:
      if word in username or username in word:
        results.append(users[username])

    return render_template("search.html",
                           query=query,
                           results=results,
                           type_=type)

@app.route("/create/room")
def room_setup():
  return render_template("room/room_setup.html")

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
                               author=package.made_by,
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
            "author": package.made_by,
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

@app.route("/api/room/<id>/join", methods=["POST"])
def join_room(id):
  id = int(id)
  if id in rooms:
    username = request.form["username"]
    password = request.form["password"]
    if username in users and users[username].password == password and username in rooms[id].invited:
      users[username].join_room(id)
      return "true"
    else:
      return "false"
  abort(404)

@app.route("/api/room/<id>/invite", methods=["POST"])
def invite_to_room(id):
  id = int(id)
  if id in rooms:
    username = request.form["username"]
    password = request.form["password"]
    invite_name = request.form["invite_name"]
    if username in users and users[username].password == password and rooms[id].owner == username and invite_name in users:
      users[invite_name].invite_to_room(id)
      rooms[id].invited.append(invite_name)
      return "done"
    else:
      return "param_fail"
  else:
    abort(404)

@app.route("/api/room/<id>/add_package", methods=["POST"])
def add_package_to_room(id):
  id = int(id)
  username = request.form["username"]
  password = request.form["password"]
  package_id = int(request.form["package"])
  if id in rooms:
    if username in users and users[username].password == password and rooms[id].owner == username and package_id in packages and package_id not in rooms[id].packages:
      rooms[id].add_package(package_id)
      return "done"
    else:
      return "param_fail"
  else:
    abort(404)

@app.route("/api/create/room", methods=["POST"])
def api_create_room():
  owner_user = request.form["username"]
  owner_pass = request.form["password"]
  if owner_user in users and users[owner_user].password == owner_pass:
    packages = json.loads(request.form["packages"])
    room_name = request.form["name"]
    return str(create_new_room(room_name, packages, owner_user))
  else:
    return "Account Details Invalid"

def create_new_room(name, packages: list, owner: str):
  id = next_id(Room, rooms)
  rooms[id] = Room(id, name, owner, packages)
  users[owner].invite_to_room(id)
  users[owner].join_room(id)
  return id

@app.route("/api/create/package", methods=["POST"])
def create_package():
    print(request.form)
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
    return "Package created successfully"


def create_new_package(name, user: User, pages: list):
    id = next_id(Package, packages)
    packages[id] = Package(name, user.username, pages, id)
    user.add_package(id)

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
    users["test"] = User("test", "test")
    print(packages)
    app.run(host="0.0.0.0", port=3000)
