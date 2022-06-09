# ======================================================================== Развлечения
# Импорты необходимые для бота

import requests
import bs4
from telebot import types
from io import BytesIO
from SECRET import open_weather_token
from datetime import datetime
import DZ
from pycbrf import ExchangeRates

#from wiki import get_wiki
import random
#from wiki import my_input
#from wiki import jar
import telebot
import SECRET
bot = telebot.TeleBot(SECRET.TELEGRAM_TOKEN)

# -----------------------------------------------------------------------
# Возможности бота

def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

#    if ms_text == "Лиса":
#        bot.send_photo(chat_id, photo=get_foxURL())

    if ms_text == "Анекдот":
        bot.send_message(chat_id, text=get_anekdot())

    elif ms_text == "Обнимашки":
        bot.send_video(chat_id, video=get_obn(), caption="хе-хе, милая")

    elif ms_text == 'USD':
        message_norm = ms_text.strip().lower()
        if message_norm in ['usd', 'eur']:
            rates = ExchangeRates(datetime.now())
            bot.send_message(chat_id, text=f" - Запрос был выполнен в: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n - На текущий момент {message_norm.upper()} можно купить по: {float(rates[message_norm.upper()].rate)} вечно деревянных", parse_mode="html")

    elif ms_text == 'EUR':
        message_norm = ms_text.strip().lower()
        if message_norm in ['usd', 'eur']:
            rates = ExchangeRates(datetime.now())
            bot.send_message(chat_id, text=f" - Запрос был выполнен в: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n - На текущий момент {message_norm.upper()} можно купить по: {float(rates[message_norm.upper()].rate)} вечно деревянных", parse_mode="html")


    elif ms_text == "Номер":
        bot.send_message(chat_id, text=get_number)

    elif ms_text == "Сериал":
        ser_img, ser_name, ser_info = get_ser()
        bot.send_photo(chat_id, photo=ser_img)
        bot.send_message(chat_id, text=f"{ser_name[0]}\n\n{ser_info[0]}")

    elif ms_text == "Кнопка":
        bot.send_message(chat_id, text="вы нажали на кнопку")

    elif ms_text == "Кости":
        #bot.send_message(chat_id, text=game_kost(bot, message))
        bot.send_message(chat_id, text="Кости находится на стадии разработки")

    elif ms_text == "Подмигивание":
        bot.send_video(chat_id, video=get_pod(), caption="Разве не прелесть?")

    elif ms_text == "Поглаживание":
        bot.send_video(chat_id, video=get_pog(), caption="Это прекрасно")

    elif ms_text == "Погода":
        bot.send_message(chat_id, text=get_weather())

    elif ms_text == "Джарвис":
    #     bot.send_message(chat_id, text=jar)
        bot.send_message(message.chat.id, "Джарвис находится на стадии разработки")
        #my_jar(bot, chat_id, text=f"Отправьте мне любое слово, и я найду его значение на Wikipedia", get_wiki())
        # bot.send_message(message.chat.id, 'Отправьте мне любое слово, и я найду его значение на Wikipedia')
        #
        # bot.send_message(message.chat.id, get_wiki(message.text))

#    elif ms_text == "Угадай число":
#        bot.send_message(text=digit_games(bot, message, chat_id))
#        bot.send_message(digit_games(message))
#        bot.send_message(bot, chat_id, digit_games())

    elif ms_text == "Угадай число":

        init_storage(message.chat.id)

        attempt = 5
        set_data_storage(message.chat.id, "attempt", attempt)
        random_digit = random.randint(1, 10)
        set_data_storage(message.chat.id, "random_digit", random_digit)

        bot.send_message(message.chat.id, f'Игра "угадай число от 1 до 10"!')
#        bot.send_message(message.chat.id, 'Готово! Загадано число от 1 до 10!')
        bot.send_message(message.chat.id, 'Ну давай, введи число, попробуй угадай;)')

        bot.register_next_step_handler(message, process_digit_step)
        # bot.send_message(digit_games(message))
        # bot.send_message(bot, chat_id, digit_games())

    elif ms_text == "Биток":
        bot.send_message(chat_id, text=get_bitok())

    elif ms_text == "Библиотека":
        bot.send_message(chat_id, text=get_biblia())

    elif ms_text == "Фильм":
        send_film(bot, chat_id)

    elif ms_text == "Угадай кто?":
        get_ManOrNot(bot, chat_id)

    elif ms_text == "Имя":
        DZ.domaxa_1(bot, chat_id)

    elif ms_text == "Возраст":
        DZ.domaxa_2(bot, chat_id)

    elif ms_text == "Фамилия":
        DZ.domaxa_3(bot, chat_id)

    elif ms_text == "Вопрос":
        DZ.domaxa_4(bot, chat_id)

    elif ms_text == "В0прос":
        DZ.domaxa_5(bot, chat_id)

    elif ms_text == "Регистр":
        DZ.domaxa_6(bot, chat_id)

    # elif ms_text == "В0опрос":
    #     DZ.domaxa_7(bot, chat_id)

    elif ms_text == "Математика":
        DZ.domaxa_8(bot, chat_id)

# -----------------------------------------------------------------------
# Уголок юмора

def get_anekdot():
    array_anekdots = []
    req_anek = requests.get('http://anekdotme.ru/random')
    if req_anek.status_code == 200:
        soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
        result_find = soup.select('.anekdot_text')
        for result in result_find:
            array_anekdots.append(result.getText().strip())
    if len(array_anekdots) > 0:
        return array_anekdots[0]
    else:
        return ""

# -----------------------------------------------------------------------
# Биток

def get_bitok():
    req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
    response = req.json()
    sell_price = response["btc_usd"]["sell"]
    msg = f" - Запрос был выполнен в: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n - На текущий момент биткоин можно купить по: {sell_price} $$$"
    return msg

# -----------------------------------------------------------------------
# Обнимашки

def get_obn():
    url = ""
    req = requests.get('https://some-random-api.ml/animu/hug')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['link']
        return url

# -----------------------------------------------------------------------
# Подмигивание

def get_pod():
    url = ""
    req = requests.get('https://some-random-api.ml/animu/wink')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['link']
        return url

# -----------------------------------------------------------------------
# Поглаживание

def get_pog():
    url = ""
    req = requests.get('https://some-random-api.ml/animu/pat')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['link']
        return url

# -----------------------------------------------------------------------
# Лиса

def get_foxURL():
    url = ""
    req = requests.get('https://randomfox.ca/floof/')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['image']
    return url

# -----------------------------------------------------------------------
# Курсы

#def get_cursi():
#    url = "https://www.fontanka.ru/currency.html"
#    df = pd.read_html(url)[0]
#    return(df.loc[df['Валюта'].isin(['usd','eur']), ['Валюта.1','Курс']].apply(lambda x: print(f'{x[0]}: {x[1]}'), axis=1))

# -----------------------------------------------------------------------
# Кто ты

def get_ManOrNot(bot, chat_id):

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Проверить", url="https://vc.ru/dev/58543-thispersondoesnotexist-sayt-generator-realistichnyh-lic") #http://astronaut.io/#
    markup.add(btn1)

    req = requests.get("https://thispersondoesnotexist.com/image", allow_redirects=True)
    if req.status_code == 200:
        img = BytesIO(req.content)
        bot.send_photo(chat_id, photo=img, reply_markup=markup, caption=" - Этого человека не существует в нашем мире, как - вы можете узнать по ссылке ниже!")

# -----------------------------------------------------------------------
# Кинотеатр

def send_film(bot, chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n" \
               f"Год: {film['Год']}\n" \
               f"Страна: {film['Страна']}\n" \
               f"Жанр: {film['Жанр']}\n" \
               f"Продолжительность: {film['Продолжительность']}"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)

# ---------------------------------------------------------------------
# Фильмы

def get_randomFilm():
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]

    details = result_find.findAll('td')
    infoFilm["Год"] = details[0].contents[1].strip()
    infoFilm["Страна"] = details[1].contents[1].strip()
    infoFilm["Жанр"] = details[2].contents[1].strip()
    infoFilm["Продолжительность"] = details[3].contents[1].strip()
    infoFilm["Режиссёр"] = details[4].contents[1].strip()
    infoFilm["Актёры"] = details[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]

    return infoFilm

# -----------------------------------------------------------------------
# Погода

def get_weather(city = "Sankt-Peterburg"):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric")
    data = r.json()

    city = data["name"]
    cur_weather = data["main"]["temp"]

    weather_description = data["weather"][0]["main"]
    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        wd = "Посмотри в окно, не пойму что там за погода!"

    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind = data["wind"]["speed"]
    sunrise_timestamp = datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset_timestamp = datetime.fromtimestamp(data["sys"]["sunset"])
    length_of_the_day = datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.fromtimestamp(data["sys"]["sunrise"])

    return(f" - Сегодняшняя дата: {datetime.now().strftime('%Y-%m-%d')}\n\n"
           f" - Погода в городе: {city}\n - Температура:      {cur_weather}C°\n                                    {wd}\n\n"
           f" - Влажность:          {humidity}%\n - Давление:            {pressure} мм.рт.ст\n - Ветер:                     {wind} м/с\n\n"
           f" - Восход солнца:   {sunrise_timestamp}\n - Закат солнца:      {sunset_timestamp}\n - Продолжительность дня:      {length_of_the_day}\n\n"
           f" - Желаю вам хорошего, продуктивного проведения этих суток!")

# -----------------------------------------------------------------------
# Библиотека

def get_biblia():
    book = None
    url = ("https://readly.ru/books/i_am_lucky/?show=1")
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, "html.parser")
    for b in soup.select("h3 > a"):
        book = ("https://readly.ru" + str(b.get("href")))
    return book

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

storage = dict()

def init_storage(user_id):
    storage[user_id] = dict(attempt=None, random_digit=None)


def set_data_storage(user_id, key, value):
    storage[user_id][key] = value


def get_data_storage(user_id):
    return storage[user_id]


        # def digit_games(bot, message):



def process_digit_step(message):
    chat_id = message.chat.id
    user_digit = message.text


    if not user_digit.isdigit():
        msg = 'Ты ввел не цифры. Вводи только цифры! Я не буду с тобой игать!'
        bot.send_message(chat_id, msg)
        return

    attempt = get_data_storage(chat_id)["attempt"]
    random_digit = get_data_storage(chat_id)["random_digit"]

    if int(user_digit) == random_digit:
        bot.send_sticker(chat_id, "CAACAgIAAxkBAAEE6oNinINWuH5f0fWH_lGGIssF9VV2uAACdRUAAhoZgEmPLAtTSmwZUiQE")
        msg = f'Ура! Ты угадал число! Это была цифра {random_digit}'
        init_storage(chat_id)
        bot.send_message(chat_id, msg)
        return
    # elif attempt > 1:
    #     attempt -= 1
    #     set_data_storage(chat_id, "attempt", attempt)
    #     msg = f'Неверно, осталось попыток: {attempt}'
    #     bot.send_message(chat_id, msg)
    #     bot.register_next_step_handler(message, process_digit_step)
    else:
        bot.send_sticker(chat_id, "CAACAgIAAxkBAAEE6odinINdSGSHKEnO1BZQwWxIbRbVaQAChhwAAijsaEkCH3PzlydmviQE")
        msg = 'Неверно, ты проиграл!'
        init_storage(chat_id)
        bot.send_message(chat_id, msg)
        return

# -----------------------------------------------------------------------
# Генерация номера

def get_number():
    array_num = []
    req_numbers = requests.get('https://calculator888.ru/random-generator')
    if req_numbers.status_code == 200:
        soup = bs4.BeautifulSoup(req_numbers.text, "html.parser")
        result_find = soup.select('.blok_otvet')
        for result in result_find:
            array_num.append(result.getText().strip())
    if len(array_num) > 0:
        return array_num[0]
    else:
        return ""


# -----------------------------------------------------------------------
# Сериал

def get_ser():
    ar_ser = []
    ar_ser_info = []
    req_ser = requests.get('https://tvfeed.in/serial/random/')
    soup = bs4.BeautifulSoup(req_ser.text, "html.parser")
    result_find_text = soup.select('.serial_info h1')
    result_find_info = soup.select('.serial_info .about p')
    result_find = soup.find('picture')
    image = []
    for img in result_find.find_all('img'):
        image.append(img.get('src'))
    ser_img = image[0]
    for result in result_find_text:
        ar_ser.append(result.getText().strip())
    for result in result_find_info:
        ar_ser_info.append(result.getText().strip())
    return ser_img, ar_ser, ar_ser_info

# -----------------------------------------------------------------------
# Игра

# class YourGreatGame:
#     def __init__(self, bot, message):
#         pass
#     def player_name(self, bot, message):
#        self.name1 = "PS"
#        self.name2 = "YOU"
#        return self.name1, self.name2
#     def dice(self, sides=6):
#        return random.randint(1, sides)
#     def rolling_dices(self, bot, message):
#        self.roll_dice = self.dice()
#        if self.roll_dice == 1:
#           bot.send_message(message.chat.id, "Выпали кости номиналом в один ")
#        if self.roll_dice == 2:
#           bot.send_message(message.chat.id, "Выпали кости номиналом в два ")
#        if self.roll_dice == 3:
#           bot.send_message(message.chat.id, "Выпали кости номиналом в три ")
#        if self.roll_dice == 4:
#           bot.send_message(message.chat.id, "Выпали кости номиналом в четыре ")
#        if self.roll_dice == 5:
#           bot.send_message(message.chat.id, "Выпали кости номиналом в пять")
#        if self.roll_dice == 6:
#           bot.send_message(message.chat.id, "Выпали кости номиналом в шесть")
#        self.roll_dice2 = self.dice()
#        if self.roll_dice2 == 1:
#           bot.send_message(message.chat.id, "и один")
#        if self.roll_dice2 == 2:
#           bot.send_message(message.chat.id, "и два")
#        if self.roll_dice2 == 3:
#           bot.send_message(message.chat.id, "и три")
#        if self.roll_dice2 == 4:
#           bot.send_message(message.chat.id, "и четыре")
#        if self.roll_dice2 == 5:
#           bot.send_message(message.chat.id, "и пять")
#        if self.roll_dice2 == 6:
#           bot.send_message(message.chat.id, "и шесть")
#        return self.roll_dice, self.roll_dice2
#     def results(self, bot, message):
#        bot.send_message(message.chat.id, "Игроку", self.name1, self.roll_dice, self.roll_dice2)
#     def results2(self, bot, message):
#        bot.send_message(message.chat.id, "Игроку", self.name2, self.roll_dice, self.roll_dice2)
#
# def game_kost(bot, message):
#    game = YourGreatGame(bot, message)
#    game.player_name(bot, message)
#    game.rolling_dices(bot, message)
#    game.results(bot, message)
#    game.rolling_dices(bot, message)
#    game.results2(bot, message)


