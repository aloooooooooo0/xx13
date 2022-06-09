def domaxa_1(bot, chat_id):
    bot.send_message(chat_id, text=f"Меня зовут Даниил")

def domaxa_2(bot, chat_id):
    bot.send_message(chat_id, text=f"Мне 18 годиков")

def domaxa_3(bot, chat_id):
    bot.send_message(chat_id, text=f"Зыков " * 5)

def domaxa_4(bot, chat_id):
    domaxa_4_ResponseHandler = lambda message: bot.send_message(chat_id, f"Добро пожаловать {message.text}! У тебя отвратное имя, в нём {len(message.text)} отвратительных букв!")
    my_input(bot, chat_id, "Как тебя звать?", domaxa_4_ResponseHandler)

def domaxa_5(bot, chat_id):
    my_inputInt(bot, chat_id, "Сколько тебе годиков?", domaxa_5_ResponseHandler)

def domaxa_5_ResponseHandler(bot, chat_id, age_int):
    #try:
        bot.send_message(chat_id, text=f"О! тебе уже {age_int}! \nА почти {age_int+1}...")
        if int(age_int) > 50 and int(age_int) < 150:
            bot.send_message(chat_id, text=f'Слушай, да ты уже дед, да еще и живой в таком возрасте {age_int+1}!')
        if int(age_int) > 1 and int(age_int) < 50:
            bot.send_message(chat_id, text=f'А вот мне 18)')

    #except ValueError:
    #    bot.send_message(chat_id, text="Это не число...")

def domaxa_6(bot, chat_id):
    qwerty = lambda message: bot.send_message(chat_id, "{}\n{}\n{}\n{}".format(message.text.upper(), message.text.lower(),
                                                                               message.text.capitalize(),
                                                                               message.text[0].lower() + message.text[1:].upper()))
    my_input(bot, chat_id, "Как тебя зовут?", qwerty)

def domaxa_7(bot, chat_id):
    my_inputInt(bot, chat_id, "Сколько тебе лет?", domaxa_7_ResponseHandler)

def domaxa_7_ResponseHandler(bot, chat_id, x):
    mult = lambda x: int(x[0]) * int(x[1])
    addit = lambda x: int(x[0]) + int(x[1])
    bot.send_message(chat_id, text=f"Произведение цифр твоего возраста: {mult}\nСумма цифр твоего возраста: {addit}")

def my_input(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, ResponseHandler)

def my_inputInt(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, my_inputInt_SecondPart, botQuestion=bot, txtQuestion=txt, ResponseHandler=ResponseHandler)

def my_inputInt_SecondPart(message, botQuestion, txtQuestion, ResponseHandler):
    chat_id = message.chat.id
    try:
        if message.content_type != "text":
            raise ValueError
        var_int = int(message.text)
        ResponseHandler(botQuestion, chat_id, var_int)
    except ValueError:
        botQuestion.send_message(chat_id,
                         text="Можно вводить ТОЛЬКО целое число в десятичной системе исчисления (символами от 0 до 9)!\nПопробуйте еще раз...")
        my_inputInt(botQuestion, chat_id, txtQuestion, ResponseHandler)


def domaxa_8(bot, chat_id):
    my_inputInt(bot, chat_id, "Сколько будет 2+2*2?", domaxa_8_ResponseHandler)

def domaxa_8_ResponseHandler(bot, chat_id, num_int):
    if num_int == int("6"):
        bot.send_message(chat_id, text=f"Молодец!\nДействительно, правильный ответ {num_int}!")
    else:
        bot.send_message(chat_id, text=f"Неправильно, ответ не {num_int}!")