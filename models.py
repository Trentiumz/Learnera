class Question:
    def __init__(self, question_type: str, args):
        self.question_type = question_type
        self.args = args


# MIGHT ACTUALLY BE KINDA USELESS
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
# END USELESS CODE


class Lesson:
    new_index = 1

    def __init__(self, name, made_by, questions, id):
        self.name = name
        self.made_by = made_by
        self.questions = questions
        self.id = id

    def add_question(self, question: Question):
        self.questions.append(question)


class Course:
    new_index = 1

    def __init__(self, name, made_by, lessons, id):
        self.name = name
        self.made_by = made_by
        self.lessons = lessons
        self.id = id

    def add_lesson(self, lesson: Lesson):
        self.lessons.append(lesson)


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.courses = []
        self.lessons = []

    def add_lesson(self, lesson: Lesson):
        self.lessons.append(lesson)

    def add_course(self, course: Course):
        self.courses.append(course)
