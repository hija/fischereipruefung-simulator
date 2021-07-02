from typing import Optional
from fastapi import FastAPI
import json
import random
import contextlib

app = FastAPI()
questions = json.load(open('res/state3.json'))

CATEGORIES = ['Allgemeine Fischkunde', 'Spezielle Fischkunde', 'Gewässerkunde', 'Gerätekunde', 'Gesetzeskunde']

@contextlib.contextmanager
def local_seed(seed):
    state = random.getstate()
    random.seed(seed)
    try:
        yield
    finally:
        random.setstate(state)

def prepare_question(question):
    print(question)
    # There are always 3 possible answers --> we shuffle them
    answer_order = random.sample([0,1,2], k=3)
    solution = [int(i)-1 for i in question['solution']] #-1 bc fk did not use zero based indices
    solution = [answer_order.index(solutionindex) for solutionindex in solution] 
    
    new_question = {
        'question': question['question'],
        'answers': [
            question[f'answer{answer_order[0]+1}'],
            question[f'answer{answer_order[1]+1}'],
            question[f'answer{answer_order[2]+1}']
        ],        
        'solution': solution
    }

    if question['fishpic']:
        new_question['image'] = question['fishpic'].replace('png', 'jpg')

    return new_question

@app.get('/quiz/{seed}')
async def get_quiz(seed: int):
    # Get questions per category

    _questions = {}
    with local_seed(seed):
        for category in range(5):
            all_questions_of_category = questions['questions'][f'c0{category+1}']
            # Sample random questions
            category_keys = all_questions_of_category.keys()

            sample_questions = list(map(questions['questions'][f'c0{category+1}'].get, random.sample(category_keys, k=12)))
            sample_questions_prepared = list(map(prepare_question, sample_questions))
            _questions[f'c{category}'] = {
                'name': CATEGORIES[category],
                'questions': sample_questions_prepared
            }

    return _questions