from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart

from BOT_TOKEN import BOT_TOKEN
import command_messages
import text_messages

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.message.register(command_messages.process_start_command,
                    CommandStart())
dp.message.register(command_messages.process_help_command,
                    Command(commands='help'))
dp.message.register(command_messages.process_stat_command,
                    Command(commands='stat'))
dp.message.register(command_messages.process_cancel_command,
                    Command(commands='cancel'))
dp.message.register(text_messages.process_positive_answer,
                    F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                        'играть', 'хочу играть', 'ехала']))
dp.message.register(text_messages.process_negative_answer,
                    F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
dp.message.register(text_messages.process_number_answer,
                    lambda x: x.text and x.text.isdigit()
                    and 1 <= int(x.text) <= 100)
dp.message.register(text_messages.process_other_answers)

if __name__ == '__main__':
    dp.run_polling(bot)
