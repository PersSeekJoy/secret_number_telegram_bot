import json


def users_read() -> dict:
    with open('users.json', 'r') as file:
        users = json.load(file)
    users = dict(zip(map(int, users.keys()), users.values()))
    return users


def users_write(users: dict):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4, ensure_ascii=False)
