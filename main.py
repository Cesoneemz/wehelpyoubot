import time
import os

import telebot
from telebot import apihelper

import markups

from functions import check_is_banned as isBanned
from functions import check_bad_words as check_bad_words
from functions import check_is_message_exists as check
from functions import get_help_message as get
from functions import add_new_message as add
from functions import send_user_his_message as send
from functions import edit_message as edit
from functions import delete_message as delete
from functions import like_on_message as like
from functions import report_to_message as report

from admin import admins_list as admins_list
from admin import show_all_reports as reports
from admin import ban_author as ban
from admin import unban_author as unban
from admin import delete_report as delete_report
from admin import clear_all_reports as clear
from admin import delete_message_from_admin as delete_message_from_admin
from admin import add_admin_to_admins_list as add_admin
from admin import delete_admin_from_admins_list as delete_admin

TOKEN = os.environ.get('TOKEN')

bot = telebot.TeleBot(TOKEN)


def check_is_banned_decorator(function):
    def wrapper(message):
        if not isBanned(message.chat.username):
            function(message)
        else:
            bot.send_message(message.chat.id, "Вы были забанены за нарушение правил пользования.")

    return wrapper


@bot.message_handler(commands=['start', 'help'])
@check_is_banned_decorator
def send_welcome(message):
    msg = bot.send_message(message.chat.id,
                           "Привет! Данный бот предназначен для того, чтобы пользователи смогли обменитваться тёплыми "
                           "сообщениями поддержки друг с другом. Ниже, на клавиатуре представлены команды, которыми "
                           "можно пользоваться.\n\nВнимание! Администрация не несёт ответственность за сохранность "
                           "личных данных! При добавлении личных сообщений, не нужно вводить:\n- Адреса проживания "
                           "или прописки\n- Паспортные данные\n- Номера телефонов\n- Данные банковских карт\n- Данные "
                           "иных личных документов\n- Логины и пароли\n-Иные личные данные",
                           reply_markup=markups.markup)


@bot.message_handler(commands=['ineedhelp'])
@check_is_banned_decorator
def send_help_message_to_user(message):
    global author, help_message
    help_message, author = get()
    bot.send_message(message.chat.id, help_message, reply_markup=markups.like_dismiss_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "like":
        like(author)
        bot.send_message(call.message.chat.id, "Лайк поставлен!")
    elif call.data == "report":
        report(author, help_message)
        bot.send_message(call.message.chat.id, "Жалоба отправлена")


@bot.message_handler(commands=['new'])
@check_is_banned_decorator
def create_new_message(message):
    if not check(message.chat.username):
        msg = bot.send_message(message.chat.id, "Пожалуйста, введите сообщение, которое вы хотите добавить.")
        bot.register_next_step_handler(msg, process_create_new_message)
    else:
        bot.send_message(message.chat.id,
                         "У вас уже создано сообщение. Для просмотра его статистики наберите \"Моё сообщение\".")


def process_create_new_message(message):
    bad_words = check_bad_words(message.text.lower())
    if bad_words == '':
        add(message)
        bot.send_message(message.chat.id, "Сообщение успешно добавлено!")
    else:
        bot.send_message(message.chat.id, f"Ваше сообщение содержит недопустимые слово(-а) ({bad_words}) и не было "
                                          f"добавлено.")


@bot.message_handler(commands=['message'])
@check_is_banned_decorator
def send_user_his_message(message):
    if check(message.chat.username):
        msg = bot.send_message(message.chat.id, send(message), reply_markup=markups.my_message_markup)
        bot.register_next_step_handler(msg, process_my_message)
    else:
        bot.send_message(message.chat.id, "У вас ещё не созданного сообщения. Для того, чтобы его создать введите "
                                          "\"Добавить сообщение\".")


def process_my_message(message):
    if message.text.lower() == "изменить сообщение":
        msg = bot.send_message(message.chat.id, "Пожалуйста, введите новое сообщение")
        bot.register_next_step_handler(msg, edit_message)
    elif message.text.lower() == "удалить сообщение":
        delete_message(message)
    elif message.text.lower() == "назад":
        go_back(message)


def edit_message(message):
    edit(message)
    bot.send_message(message.chat.id, "Успешно отредактировано!", reply_markup=markups.markup)


def delete_message(message):
    delete(message)
    bot.send_message(message.chat.id, "Успешно удалено!", reply_markup=markups.markup)


def go_back(message):
    msg = bot.send_message(message.chat.id, "Возвращаюсь назад...", reply_markup=markups.markup)
    bot.register_next_step_handler(msg, router)


@bot.message_handler(content_types=['text'])
@check_is_banned_decorator
def router(message):
    if message.text.lower() == "мне нужна помощь!":
        send_help_message_to_user(message)
    elif message.text.lower() == "добавить сообщение":
        create_new_message(message)
    elif message.text.lower() == "моё сообщение":
        send_user_his_message(message)
    elif message.text.lower() == "показать все жалобы" and message.chat.username in admins_list:
        msg = reports()
        bot.send_message(message.chat.id, msg, reply_markup=markups.admin_markup)
    elif message.text.lower() == "удалить жалобу" and message.chat.username in admins_list:
        msg = bot.send_message(message.chat.id, "Введите имя человека, жалобу которого нужно удалить")
        bot.register_next_step_handler(msg, delete_report_process)
    elif message.text.lower() == "очистить жалобы" and message.chat.username in admins_list:
        clear()
        bot.send_message(message.chat.id, "Все жалобы были очищены")
    elif message.text.lower() == "забанить автора" and message.chat.username in admins_list:
        msg = bot.send_message(message.chat.id, "Введите имя человека, которого хотите забанить.",
                               reply_markup=markups.admin_markup)
        bot.register_next_step_handler(msg, ban_message)
    elif message.text.lower() == "разбанить автора" and message.chat.username in admins_list:
        msg = bot.send_message(message.chat.id, "Введите имя человека, которого хотите разбанить.",
                               reply_markup=markups.admin_markup)
        bot.register_next_step_handler(msg, unban_message)
    elif message.text.lower() == "удалить сообщение(Админ)" and message.chat.username in admins_list:
        msg = bot.send_message(message.chat.id, "Введите имя человека, сообщение которого нужно удалить.",
                               reply_markup=markups.admin_markup)
        bot.register_next_step_handler(msg, delete_message_admin)
    elif message.text.lower() == "выход из админ-панели" and message.chat.username in admins_list:
        go_back(message)
    elif message.text.lower() == "добавить админа" and message.chat.username == "cesoneemz":
        msg = bot.send_message(message.chat.id, "Введите имя человека")
        bot.register_next_step_handler(msg, process_add_admin)
    elif message.text.lower() == "удалить админа" and message.chat.username == "cesoneemz":
        msg = bot.send_message(message.chat.id, "Введите имя человека")
        bot.register_next_step_handler(msg, process_delete_admin)
    else:
        bot.send_message(message.chat.id, "Я не знаю такой команды :(")

def process_add_admin(message):
    add_admin(message.text)
    bot.send_message(message.chat.id, f"Пользователь {message.text} был добавлен в группу администраторов")

def process_delete_admin(message):
    try:
        delete_admin(message.text)
    except:
        bot.send_message(message.chat.id, "Админа с таким ником не найдено.")


def ban_message(message):
    try:
        ban(message.text)
    except Exception as e:
        bot.send_message(message.chat.id, "Сообщение с таким автором не найдено.")


def unban_message(message):
    try:
        unban(message.text)
    except Exception as e:
        bot.send_message(message.chat.id, "Сообщение с таким автором не найдено.")


def delete_report_process(message):
    try:
        delete_report(message.text)
        bot.send_message(message.chat.id, "Жалоба удалена.")
    except Exception as e:
        bot.send_message(message.chat.id, "Сообщение с таким автором не найдено.")


def delete_message_admin(message):
    try:
        delete_message_from_admin(message.text)
        bot.send_message(message.chat.id, "Сообщение удалено.")
    except Exception as e:
        bot.send_message(message.chat.id, "Сообщение с таким автором не найдено.")


while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(e.args)
        time.sleep(2)
