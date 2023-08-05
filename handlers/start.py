from const import HELP_TEXT
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.sql_commands import Database
from config import bot
from keyboards import start_keyboard
from random import randint
from datetime import datetime, timedelta


# Start
async def start(message: types.Message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    Database().sql_insert_user_table_query(telegram_id=telegram_id,
                                           username=username,
                                           first_name=first_name,
                                           last_name=last_name)

    await message.reply(text=f"Привет {message.from_user.username}!",
                        reply_markup=start_keyboard.start_keyboard())


async def help(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=HELP_TEXT)


quiz_id = None


async def quiz_1(message: types.Message):
    global quiz_id
    quiz_id = 'quiz_1'
    question = "в каком году распался СССР?"
    option = [
        "2023",
        "1999",
        "2010",
        "1987"
    ]
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton(
        "Следующая викторина",
        callback_data="button_call_1"
    )
    markup.add(button_call_1)
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=option,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="Правильный ответ 2",
        explanation_parse_mode=types.ParseMode.MARKDOWN_V2,
        reply_markup=markup
    )


async def quiz_2(call: types.PollAnswer):
    global quiz_id
    quiz_id = 'quiz_2'
    question = "кто создал python&"
    option = [
        "Билл Гейтс",
        "Майк Мазовски",
        "Гвидо Ван Россум",
        "Уилл Смит"
    ]
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=option,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation="Правильный ответ 3",
        explanation_parse_mode=types.ParseMode.MARKDOWN_V2
    )


# hw1   # 3.1.
async def handle_poll_answer(poll_answer: types.PollAnswer):
    Database().sql_insert_quiz(telegram_id=poll_answer.user.id,
                               quiz=quiz_id,
                               quiz_option=poll_answer.option_ids[0])


async def random_integer(message: types.Message):
    rand_num = randint(1, 100)
    await message.reply(rand_num)


async def complaint_member(message: types.Message):
    complaint_text = message.text.split()

    if len(complaint_text) > 1:
        username = complaint_text[1]
        t_id = int(message.from_user.id)
        t_id_bad_user = Database().sql_select_id_by_username(username)[0]['username']
        reason = complaint_text[2:] if len(complaint_text) >= 3 else ''
        count = 1
        complaint_check = Database().sql_select_complaint_check(user_id=t_id, bad_user_id=t_id_bad_user).fetchall()

        if complaint_check:
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'Вы уже отправляли жалобу на {username}')
        elif t_id_bad_user == t_id:
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'Не стоит на себя жаловатся! 🙃')
        elif t_id_bad_user:
            Database().sql_insert_complaint(telegram_id=t_id,
                                            telegram_id_bad_user=t_id_bad_user,
                                            reason=reason,
                                            count=count)

            await bot.send_message(chat_id=message.chat.id,
                                   text=f'Отправлено жалоба на {username}')

            count_complaint = len(Database().sql_select_complaint(user_id=t_id_bad_user).fetchall())
            if count_complaint >= 3:
                await bot.send_message(chat_id=t_id_bad_user,
                                       text=f'На вас 3 раза пожаловались. '
                                            f'Вы исключены из группы!')
                ban_date = datetime.now() + timedelta(days=365)
                await bot.ban_chat_member(message.chat.id, t_id_bad_user, ban_date)
            else:
                await bot.send_message(chat_id=t_id_bad_user,
                                       text=f'На вас пожаловались. '
                                            f'Ещё {3 - count_complaint} жалоба и вас исключат из группы!')
        else:
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'Пользователь не найден!')


# Dispatcher
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, lambda call: call.data == "button_call_1")
    dp.register_poll_answer_handler(handle_poll_answer)
    dp.register_message_handler(random_integer, commands=['random'])
    dp.register_message_handler(complaint_member, commands=['complaint'])
