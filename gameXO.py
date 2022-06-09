from telebot import types
from inlinebuttons import Translation
from main import Menu
import menuBot

def goto_menu(bot, chat_id, name_menu):
    # получение нужного элемента меню
    cur_menu = Menu.getCurMenu(chat_id)
    if name_menu == "Выход" and cur_menu != None and cur_menu.parent != None:
        target_menu = Menu.getMenu(chat_id, cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(chat_id, name_menu)

class TTT:
    players = []
    values = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    call_list = ["Крестики", "position0", "position1", "position2", "position3", "position4",
                 "position5", "position6", "position7", "position8"]

    @classmethod
    def main_slots(cls, call, bot):
        tmp_player = cls.player_founder(call)
        tmp_player[1] = list(cls.values)
        tmp_player[2] = 0
        tmp_player[3] = 0

        def get_text_messages(bot, cur_user, message):
            chat_id = message.chat.id
            ms_text = message.text

            if message.text == "Играть в Слоты":
                keyboard = types.InlineKeyboardMarkup(row_width=3)
                button = []
                for i in range(0, 9):
                    button.append(types.InlineKeyboardButton(" ", callback_data='position' + str(i)))
                button.append(types.InlineKeyboardButton(
                    Translation.get_menu_expression("Выход", call.from_user.id), callback_data='Menu'))
                keyboard.add(*button)
                bot.edit_message_text(chat_id=call.message.chat.id,
                                    reply_markup=keyboard,
                                    text="❌⭕️",
                                    message_id=call.message.message_id)

    # Найти игрока по ID
    @classmethod
    def player_founder(cls, call):
        while True:
            for player in cls.players:
                if player[0] == call.message.chat.id:
                    return player
            cls.players.append([call.message.chat.id, list(cls.values), 0, 0])

    @classmethod
    def get_callback(cls, call, bot):
        tmp_player = cls.player_founder(call)
        if call.data == 'Крестики':
            cls.main_slots(call, bot)
            return
        if call.from_user.id == tmp_player[3]:
            return
        for i in range(0, 9):
            if call.data == "position" + str(i):
                tmp_player[3] = call.from_user.id
                markup = types.InlineKeyboardMarkup(row_width=3)
                button = []
                for value in range(0, 9):
                    if value == i:
                        if tmp_player[2] % 2 == 0:
                            button.append(types.InlineKeyboardButton('X', callback_data='position' + str(value)))
                            tmp_player[1][value] = 'X'
                        else:
                            button.append(types.InlineKeyboardButton('0', callback_data='position' + str(value)))
                            tmp_player[1][value] = '0'
                        tmp_player[2] += 1
                    else:
                        button.append(types.InlineKeyboardButton(tmp_player[1][value],
                                                                 callback_data='position' + str(value)))
                button.append(types.InlineKeyboardButton(
                    Translation.get_menu_expression("Выход", call.from_user.id), callback_data='Menu'))
                markup.add(*button)
                bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=markup, text=call.message.text,
                                      message_id=call.message.message_id)
                if " " not in tmp_player[1]:
                    keyboard = types.InlineKeyboardMarkup()
                    again = types.InlineKeyboardButton(
                        Translation.get_hangman_exp("play_again", call.from_user.id), callback_data='Крестики')
                    ex = types.InlineKeyboardButton(
                        Translation.get_menu_expression("Выход", call.from_user.id), callback_data='Menu')
                    keyboard.add(again, ex)
                    bot.edit_message_text(chat_id=call.message.chat.id,
                                          reply_markup=keyboard,
                                          text="Ничья",
                                          message_id=call.message.message_id)
                if tmp_player[1][0] == tmp_player[1][1] == tmp_player[1][2] != " " or tmp_player[1][3] == \
                        tmp_player[1][4] == tmp_player[1][5] != " " or \
                        tmp_player[1][6] == tmp_player[1][7] == tmp_player[1][8] != " " or tmp_player[1][0] == \
                        tmp_player[1][3] == tmp_player[1][6] != " " or \
                        tmp_player[1][1] == tmp_player[1][4] == tmp_player[1][7] != " " or tmp_player[1][2] == \
                        tmp_player[1][5] == tmp_player[1][8] != " " or tmp_player[1][0] == tmp_player[1][4] == \
                        tmp_player[1][8] != " " or tmp_player[1][2] == tmp_player[1][4] == tmp_player[1][6] != " ":
                    if tmp_player[2] % 2 == 0:
                        text = '⭕'
                    else:
                        text = '❌'
                    keyboard = types.InlineKeyboardMarkup()
                    again = types.InlineKeyboardButton(
                        Translation.get_hangman_exp("play_again", call.from_user.id), callback_data='Крестики')
                    ex = types.InlineKeyboardButton(
                        Translation.get_menu_expression("Выход", call.from_user.id), callback_data='Menu')
                    keyboard.add(again, ex)
                    bot.edit_message_text(chat_id=call.message.chat.id,
                                          reply_markup=keyboard,
                                          text=text + " - Выиграл",
                                          message_id=call.message.message_id)

def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Крестики":
        TTT.get_callback(message, bot)
    elif ms_text == "Выход":
        menuBot.goto_menu(bot, chat_id, "Главное меню")