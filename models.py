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
args: {question_text: text for the question, 
      choices: [list of strings for each choice],
      correct_choice: string of correct choice}

type: term
args: {question_text: text for the question,
      answer: the correct term/word to input}

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
  def __init__(self, name: str, owner, users):
    self.name = name
    self.owner = owner
    self.users = users
  def add_user(self, user: int):
    self.packages.append(user)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.packages = []

    def add_package(self, lesson: int):
        self.packages.append(lesson)

    def __str__(self):
        return self.username
