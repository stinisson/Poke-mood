import requests
import base64

ENDPOINT = 'https://opentdb.com/api.php?amount=4&category=18&difficulty=easy&type=multiple&encode=base64'


class QuizAPI:

    def __init__(self):
        self.url = ENDPOINT

    def get_all_questions(self):
        r = requests.get(self.url)
        ls = r.json()['results']
        return ls

def quiz():
    quizapi = QuizAPI()
    results = quizapi.get_all_questions()
    for idx, result in enumerate(results):
        question = base64.b64decode(results[idx]['question']).decode('utf-8')
        correct_answer = base64.b64decode(results[idx]['correct_answer']).decode('utf-8')
        print(question)
        print(correct_answer)
        for in_ans in results[idx]['incorrect_answers']:
            incorrect_answer = base64.b64decode(in_ans).decode('utf-8')
            print(incorrect_answer)
        quit()
quiz()