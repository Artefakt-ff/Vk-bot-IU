import random
from re import sub

from fuzzywuzzy import process

from components.answers import ANSWERS


def get_answer(body):
    body = sub(',|\.|\?|!|;|:|', '', body).lower()
    analise = process.extract(body, ANSWERS.keys(), limit=1)[0] # return a tuple with a probably mean and probability
    if analise[1] < 75:
        message = 'Я тебе не понимаю :( Можешь написать help, чтобы узнать что я умею'
    else:
        message = random.choice(ANSWERS[analise[0]])  # return one from answers
    return message




