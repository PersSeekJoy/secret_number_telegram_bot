import requests
from random import randint

CAT_URL = 'https://api.thecatapi.com/v1/images/search'


def get_cat_photo() -> str:
    return requests.get(CAT_URL).json()[0]['url']


def get_random_number() -> int:
    return randint(1, 100)
