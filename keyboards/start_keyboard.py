from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def start_keyboard():
    help_button = KeyboardButton("/help")
    quiz_button = KeyboardButton("/quiz")

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True)

    return keyboard.row(
        help_button,
        quiz_button,
    )