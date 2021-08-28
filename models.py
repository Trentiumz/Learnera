class Question:
    def __init__(self, question_type: str, args):
        self.question_type = question_type
        self.args = args


class MultipleChoice(Question):
    def __init__(self, question_text: str, options):
        super().__init__("mc", {
            "question_text": question_text,
            "options": options
        })


class TermQuestion(Question):
    def __init__(self, question_text: str, answer: str):
        super().__init__("term", {
            "question_text": question_text,
            "answer": answer
        })


class Lesson:
    new_index = 1

    def __init__(self, name, questions, id):
        self.name = name
        self.questions = questions
        self.id = id

    def add_question(self, question: Question):
        self.questions.append(question)


class Course:
    new_index = 1

    def __init__(self, name, lessons, id):
        self.name = name
        self.lessons = lessons
        self.id = id

    def add_lesson(self, lesson: Lesson):
        self.lessons.append(lesson)


class User:
    def __init__(self, username, password, courses=[], lessons=[]):
        self.username = username
        self.password = password
        self.courses = courses
        self.lessons = lessons

    def add_lesson(self, lesson: Lesson):
        self.lessons.append(lesson)

    def add_course(self, course: Course):
        self.courses.append(course)
