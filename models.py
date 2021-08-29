"""
Page: 

type: content
args: {file: [link to pdf file]}

type: questions
args: {questions: [
  list of Questions
]}

Question: stored as a dict

type: mc
question_text: text for the question, 
choices: [list of strings for each choice],
correct_choice: string of correct choice

type: term
question_text: text for the question,
answer: the correct term/word to input

"""


class Page():
    def __init__(self, type: str, args):
        self.type = type
        self.args = args


class Package:
    new_index = 1

    def __init__(self, name, made_by: str, pages, id):
        self.name = name
        self.made_by = made_by
        self.pages = pages
        self.id = id

    def add_page(self, question: Page):
        self.pages.append(question)


class Room:
    new_index = 1

    def __init__(self, id, name: str, owner: str, packages):
        self.id = id
        self.name = name
        self.owner = owner
        self.packages = packages
        self.invited = [owner]

    def add_user(self, user: int):
        self.invited.append(user)

    def add_package(self, package: int):
        self.packages.append(package)


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.packages = []
        self.rooms = []
        self.invitations = []

    def add_package(self, package: int):
        self.packages.append(package)

    def join_room(self, room: int):
        if room in self.invitations:
          self.rooms.append(room)
          self.invitations.remove(room)

    def invite_to_room(self, room: int):
        if room not in self.rooms and room not in self.invitations:
            self.invitations.append(room)

    def __str__(self):
        return self.username
