from telebot import types
from menuBot import goto_menu, gen_menu_keyboard


class TTT:
    players = []
    values = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    call_list = ["XO_start", "position0", "position1", "position2", "position3", "position4",
                 "position5", "position6", "position7", "position8", "Выход"]

    @classmethod
    def main_slots(cls, call, bot):
        tmp_player = cls.player_founder(call)
        tmp_player[1] = list(cls.values)
        tmp_player[2] = 0
        tmp_player[3] = 0

        keyboard = types.InlineKeyboardMarkup(row_width=3)
        button = []
        for i in range(0, 9):
            button.append(types.InlineKeyboardButton(" ", callback_data='position' + str(i)))
        button.append(types.InlineKeyboardButton("Выход", callback_data='Выход'))
        keyboard.add(*button)
        bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard, text="❌⭕️", message_id=call.message.message_id)

    # Найти игрока по ID
    @classmethod
    def player_founder(cls, call):
        print(call)
        while True:
            for player in cls.players:
                if player[0] == call.message.chat.id:
                    return player
            cls.players.append([call.message.chat.id, list(cls.values), 0, 0])

    @classmethod
    def get_callback(cls, call, bot):
        tmp_player = cls.player_founder(call)
        if call.data == 'XO_start':
            cls.main_slots(call, bot)
            return
        elif call.data == "Выход":
            goto_menu(bot, call.message.chat.id, "Главное меню")
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
                button.append(types.InlineKeyboardButton("Выход", callback_data='Выход'))
                markup.add(*button)
                bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=markup, text=call.message.text,
                                      message_id=call.message.message_id)

                if " " not in tmp_player[1]:
                    keyboard = types.InlineKeyboardMarkup()
                    again = types.InlineKeyboardButton("play_again", callback_data='XO_start')
                    ex = types.InlineKeyboardButton("Выход", callback_data='Выход')
                    keyboard.add(again, ex)
                    bot.edit_message_text(chat_id=call.message.chat.id,
                                          reply_markup=keyboard,
                                          text="Ничья",
                                          message_id=call.message.message_id)

                if tmp_player[1][0] == tmp_player[1][1] == tmp_player[1][2] != " " \
                        or tmp_player[1][3] == tmp_player[1][4] == tmp_player[1][5] != " " \
                        or tmp_player[1][6] == tmp_player[1][7] == tmp_player[1][8] != " " \
                        or tmp_player[1][0] == tmp_player[1][3] == tmp_player[1][6] != " " \
                        or tmp_player[1][1] == tmp_player[1][4] == tmp_player[1][7] != " " \
                        or tmp_player[1][2] == tmp_player[1][5] == tmp_player[1][8] != " " \
                        or tmp_player[1][0] == tmp_player[1][4] == tmp_player[1][8] != " " \
                        or tmp_player[1][2] == tmp_player[1][4] == tmp_player[1][6] != " ":
                    if tmp_player[2] % 2 == 0:
                        text = '⭕'
                    else:
                        text = '❌'
                    keyboard = types.InlineKeyboardMarkup()
                    again = types.InlineKeyboardButton("play_again", callback_data='XO_start')
                    ex = types.InlineKeyboardButton("Выход", callback_data='Выход')
                    keyboard.add(again, ex)
                    bot.edit_message_text(chat_id=call.message.chat.id,
                                          reply_markup=keyboard,
                                          text=text + " - Выиграл",
                                          message_id=call.message.message_id)