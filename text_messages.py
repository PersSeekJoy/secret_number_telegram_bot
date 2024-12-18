from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError

from users_updates import users_read, users_write
from randoms_functions import get_cat_photo, get_random_number

ATTEMPTS = 5


async def process_positive_answer(message: Message):
    users = users_read()
    try:
        if not users[message.from_user.id]['in_game']:
            users[message.from_user.id]['in_game'] = True
            users[message.from_user.id]['secret_number'] = get_random_number()
            users[message.from_user.id]['attempts'] = ATTEMPTS
            await message.answer(
                '''Ура!
Я загадал число от 1 до 100,
попробуй угадать!'''
            )
            users_write(users)

        else:
            await message.answer(
                'Пока мы играем я могу реагировать только'
                'на числа от 1 до 100 и команды /cancel и /stat'
                )

    except TelegramForbiddenError:
        users[message.from_user.id]['in_game'] = False
        users[message.from_user.id]['secret_number'] = None
        users[message.from_user.id]['attempts'] = None
        users_write(users)


async def process_negative_answer(message: Message):
    users = users_read()
    try:
        if not users[message.from_user.id]['in_game']:
            await message.answer(
                '''Жаль😕
Если захотите играть, всегда можно об этом написать'''
            )
        else:
            await message.answer(
                '''Мы же сейчас с вами играем...
Присылайте, пожалуйста, числа от 1 до 100.'''
                )
    except TelegramForbiddenError:
        users[message.from_user.id]['in_game'] = False
        users[message.from_user.id]['secret_number'] = None
        users[message.from_user.id]['attempts'] = None
        users_write(users)


async def process_number_answer(message: Message):
    users = users_read()
    try:
        if users[message.from_user.id]['in_game']:
            if int(message.text) == users[message.from_user.id]['secret_number']:
                users[message.from_user.id]['in_game'] = False
                users[message.from_user.id]['total_games'] += 1
                users[message.from_user.id]['wins'] += 1

                await message.answer_photo(photo=get_cat_photo(),
                                           caption='''Ура🤩 Ты угадал число😎
Вот тебе котик в награду😻'''
                                           )
                await message.answer('Может сыграем ещё?🥺')

            elif int(message.text) > users[message.from_user.id]['secret_number']:
                users[message.from_user.id]['attempts'] -= 1
                await message.answer('Моё число меньше')
            elif int(message.text) < users[message.from_user.id]['secret_number']:
                users[message.from_user.id]['attempts'] -= 1
                await message.answer('Моё число больше')

            if users[message.from_user.id]['attempts'] == 0:
                users[message.from_user.id]['in_game'] = False
                users[message.from_user.id]['total_games'] += 1
                await message.answer(
                    f'''К сожалению, у вас закончились попытки. Вы проиграли😔
Моё число было {users[message.from_user.id]["secret_number"]}
Давайте сыграем ещё?'''
                )

            users_write(users)

        else:
            await message.answer('''Мы ещё не играем.
Хотите сыграть?''')

    except TelegramForbiddenError:
        users[message.from_user.id]['in_game'] = False
        users[message.from_user.id]['secret_number'] = None
        users[message.from_user.id]['attempts'] = None
        users_write(users)


async def process_other_answers(message: Message):
    users = users_read()
    try:
        if users[message.from_user.id]['in_game']:
            await message.answer(
                '''Мы же с вами сейчас играем...
Присылайте, пожалуйста, числа от 1 до 100'''
            )
        else:
            await message.answer(
                '''Я довольно ограниченный бот😶
Может просто сыграем в игру?'''
            )
    except TelegramForbiddenError:
        users[message.from_user.id]['in_game'] = False
        users[message.from_user.id]['secret_number'] = None
        users[message.from_user.id]['attempts'] = None
        users_write(users)
