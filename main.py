# -----------------------------------------------------------------------
# Импорты необходимые для бота

import telebot
from telebot import types
import menuBot
from menuBot import Menu
# import DZ   домашнее задание от первого урока
import SECRET
import botGames
import random
import wiki
import gameXO


bot = telebot.TeleBot(SECRET.TELEGRAM_TOKEN)
import fun


# -----------------------------------------------------------------------
# Класс цветов - не понимаю, они просто не работают

class color:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# -----------------------------------------------------------------------
# Функция, обрабатывающая команду start

@bot.message_handler(commands="start")
def command(message):  # CAACAgIAAxkBAAEE1HZikA-X4PsOYWekoxPv8voOobWn5wACGxQAAk9VcEn_Ed1DKZ44WSQE
    chat_id = message.chat.id  #
    txt_message = f"Добро пожаловать, {message.from_user.first_name}!" + "   Я - " + "BotLiki" + ", бот созданный чтобы быть подопытным кроликом.\n\nСписок моих возможностей приведён снизу:" + "\n - могу прислать анекдот" + "\n - могу прислать аниме GIF" + "\n - могу прислать номер" + "\n - могу прислать не существующего челоека" + "\n - могу прислать курсы валют" + "\n - могу прислать фильм" + "\n - могу прислать сериал" + "\n - могу прислать погоду" + "\n - могу прислать книгу для прочтения" + "\n - во мне есть дз" + "\n - во мне есть незавершённый Джарвис" + "\n - во мне есть простенькие игры" + "\n - реагирую на команды /help, /online и \n/start"
    bot.send_message(chat_id, text=txt_message, reply_markup=Menu.getMenu(chat_id, "Главное меню").markup)
    bot.send_sticker(chat_id, "CAACAgIAAxkBAAEE5J1imHGEvDM4v0_hoel0d71gIBBQPAAC_hYAAufTaUmqys3-dkKlhSQE")


# -----------------------------------------------------------------------
# Функция, обрабатывающая команду asistent
#
# @bot.message_handler(commands="asistent")
# def asistent(message, call):
#     chat_id = message.chat.id
#     bot.send_message(chat_id, 'Отправьте мне любое слово, и я найду его значение на Wikipedia')
#     # bot.send_message(chat_id, text=txt_message, reply_markup=Menu.getMenu(chat_id, "Главное меню").markup)
#     bot.register_next_step_handler(call.message, my_jar, call)
# -----------------------------------------------------------------------
# Функция, обрабатывающая команду help

@bot.message_handler(commands=['help'])
def help_command(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Спросить у разработчика', url='https://t.me/alo0ooooo')
    markup.add(btn1)
    bot.send_message(chat_id,
                     ' - Автор: Зыков Даниил\n\n' + ' - Это первый созданный его руками бот.\n' + ' - Бот является проектной работой по предмету "Алоритмизация и програмирование"\n' + ' - Наставником на верный путь был Швец Андрей.',
                     reply_markup=markup)
    bot.send_sticker(chat_id, "CAACAgIAAxkBAAEE5JRimG3700XiIPkZ4f9o80MyNzpN-AAC4RUAAu_7iEn9jgO1a0v3MSQE")


# -----------------------------------------------------------------------
# Функция, обрабатывающая команду online

@bot.message_handler(commands="online")
def command(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, "Активные пользователи чат-бота:")
    for el in menuBot.Users.activeUsers:
        bot.send_message(chat_id, menuBot.Users.activeUsers[el].getUserHTML(), parse_mode='HTML')
    # bot.send_sticker(chat_id, "CAACAgIAAxkBAAEE1HZikA-X4PsOYWekoxPv8voOobWn5wACGxQAAk9VcEn_Ed1DKZ44WSQE")


# -----------------------------------------------------------------------
# Получение не сообщений от юзера

@bot.message_handler(content_types=['audio', 'sticker', 'voice', 'photo', 'vidio', 'document', 'location', 'contact'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type + ", мне запретили отвечать на сообщения этого типа.")


# -----------------------------------------------------------------------
# Получение сообщений от юзера

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    cur_user = menuBot.Users.getUser(chat_id)
    if cur_user is None:
        cur_user = menuBot.Users(chat_id, message.json["from"])

    subMenu = menuBot.goto_menu(bot, chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if subMenu is not None:
        if subMenu.name == "Игра КНБ":
            GameRPS = botGames.newGame(chat_id, botGames.GameRPS())  # создаём новый экземпляр игры и регистрируем его
        return
    # проверим, является ли текст текущий команды кнопкой действия
    cur_menu = Menu.getCurMenu(chat_id)
    if cur_menu is not None and ms_text in cur_menu.buttons:  # проверим, что команда относится к текущему меню
        module = cur_menu.module

        if module != "":  # проверим, есть ли обработчик для этого пункта меню в другом модуле, если да - вызовем его (принцип инкапсуляции)
            exec(module + ".get_text_messages(bot, cur_user, message)")

    else:  # ======================================= случайный текст
        bot.send_message(chat_id,
                         text=" - Я не могу распознать вашу команду, мой хозяин не добавлял подобного функцианала: " + ms_text)
        menuBot.goto_menu(bot, chat_id, "Главное меню")


# -----------------------------------------------------------------------
# Так и не могу понять что это такое

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    chat_id = call.message.chat.id
    message_id = call.message.id
    cur_user = menuBot.Users.getUser(chat_id)
    if cur_user is None:
        cur_user = menuBot.Users(chat_id, call.message.json["from"])

    tmp = call.data.split("|")
    menu = tmp[0] if len(tmp) > 0 else ""
    cmd = tmp[1] if len(tmp) > 1 else ""
    par = tmp[2] if len(tmp) > 2 else ""


#    if menu == "GameRPSm":
#        botGames.callback_worker(bot, cur_user, cmd, par, call)

# -----------------------------------------------------------------------
# Пуск

# def get_text_messages(bot, cur_user, message):
#     chat_id = message.chat.id
#     ms_text = message.text
#
#     if ms_text == "Угадай число":
#         digit_games(message)

# -----------------------------------------------------------------------
# Игра Числа

# storage = dict()
#
# def init_storage(user_id):
#     storage[user_id] = dict(attempt=None, random_digit=None)
#
#
# def set_data_storage(user_id, key, value):
#     storage[user_id][key] = value
#
#
# def get_data_storage(user_id, chat_id):
#     return storage[user_id]
#
#
# def digit_games(bot, message, chat_id):
#     init_storage(message.chat.id)
#
#     attempt = 5
#     set_data_storage(message.chat.id, "attempt", attempt)
#
#     bot.send_message(message.chat.id, f'Игра "угадай число"!\nКоличество попыток: {attempt}')
#
#     random_digit = random.randint(1, 10)
#
#     set_data_storage(message.chat.id, "random_digit", random_digit)
#
#     bot.send_message(message.chat.id, 'Готово! Загадано число от 1 до 10!')
#     bot.send_message(message.chat.id, 'Ну давай, введи число, попробуй угадай;)')
#     bot.register_next_step_handler(message, process_digit_step)
#
#
# def process_digit_step(bot, message):
#     chat_id = message.chat.id
#     user_digit = message.text
#
#     if not user_digit.isdigit():
#         msg = bot.reply_to(message, 'Ты ввел не цифры. Вводи только цифры!')
#         bot.register_next_step_handler(msg, process_digit_step)
#         return
#
#     attempt = get_data_storage(chat_id)["attempt"]
#     random_digit = get_data_storage(chat_id)["random_digit"]
#
#     if int(user_digit) == random_digit:
#         bot.send_sticker(chat_id, "CAACAgIAAxkBAAEE5btimROuB5eos0VdeyZn2J5RXUg_WAAC-AsAAqydAAFIkwFAkULAXYYkBA")
#         bot.send_message(chat_id, f'Ура! Ты угадал число! Это была цифра {random_digit}')
#         init_storage(chat_id)
#         return
#     elif attempt > 1:
#         attempt -= 1
#         set_data_storage(chat_id, "attempt", attempt)
#         bot.send_message(chat_id, f'Неверно, осталось попыток: {attempt}')
#         bot.register_next_step_handler(message, process_digit_step)
#     else:
#         bot.send_message(chat_id, 'Твои попытки закончились, ты проиграл!')
#         init_storage(chat_id)
#         return
#
#


bot.polling(none_stop=True, interval=0)
