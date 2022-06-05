#---------------------------------------
# Сам код wiki

import telebot
import wikipedia, re
import SECRET
bot = telebot.TeleBot(SECRET.TELEGRAM_TOKEN)

wikipedia.set_lang("ru")

def get_wiki(message):
    try:
        ny = wikipedia.page(message)
        wikitext=ny.content[:1000]
        wikimas=wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not('==' in x):
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        return wikitext2
    except Exception:
        return 'В энциклопедии нет информации об этом'

#def my_jar(bot, message):
#   bot.send_message(message.chat.id, get_wiki(message.text))

def my_input(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, ResponseHandler)
#
# @bot.message_handler(commands=["asistent"])
# def jar(bot, chat_id):
#     my_input(bot, chat_id, "Джарвис находится на стадии разработки?", jar_ResponseHandler)
#
#
#
# def jar_ResponseHandler(message, bot, chat_id):
#     bot.send_message(chat_id, text=f"{get_wiki(message.text)}")