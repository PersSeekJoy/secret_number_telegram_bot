from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError

from users_updates import users_read, users_write

ATTEMPTS = 5


async def process_start_command(message: Message):
    users = users_read()
    try:
        await message.answer(
            '''Привет👋
Давайте сыграем в игру "Угадай чилсо"?
Чтобы получить правила игры
и список доступных команд отправьте команду /help'''
        )
        if message.from_user.id not in users:
            users[message.from_user.id] = {
                'in_game': False,
                'secret_number': None,
                'attempts': None,
                'total_games': 0,
                'wins': 0
            }
            users_write(users)
    except TelegramForbiddenError:
        pass


async def process_help_command(message: Message):
    users = users_read()
    try:
        await message.answer(
            f'''Правила игры📜
Я загадываю число от 1 до 100, а вам нужно его угадать
У вас есть {ATTEMPTS} попыток

Доступные команды:
/help - правила игры и список команд
/cancel - выйти из игры
/stat - посмотреть статистику

Чтобы начать игру напишите любое из этих сообщений
(без кавычек, в любом регистре):
"Да", "Давай", "Сыграем", "Игра", "Играть", "Хочу играть", "Ехала"

Давай сыграем?'''
        )
    except TelegramForbiddenError:
        users[message.from_user.id]['in_game'] = False
        users[message.from_user.id]['secret_number'] = None
        users[message.from_user.id]['attempts'] = None
        users_write(users)


async def process_stat_command(message: Message):
    users = users_read()
    try:
        await message.answer(
            f'''Всего игр сыграно: {users[message.from_user.id]["total_games"]}
Игр выйграно: {users[message.from_user.id]["wins"]}'''
        )
    except TelegramForbiddenError:
        users[message.from_user.id]['in_game'] = False
        users[message.from_user.id]['secret_number'] = None
        users[message.from_user.id]['attempts'] = None
        users_write(users)


async def process_cancel_command(message: Message):
    users = users_read()
    try:
        if users[message.from_user.id]['in_game']:
            users[message.from_user.id]['in_game'] = False
            await message.answer(
                '''Вы вышли из игры
Если захотите сыграть снова - напишите об этом'''
            )
            users_write(users)
        else:
            await message.answer(
                '''А мы с вами и так не играем.
Может сыграем разок?'''
            )
    except TelegramForbiddenError:
        users[message.from_user.id]['in_game'] = False
        users[message.from_user.id]['secret_number'] = None
        users[message.from_user.id]['attempts'] = None
        users_write(users)
