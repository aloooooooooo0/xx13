# -----------------------------------------------------------------------
# Импорты
from menuBot import goto_menu


activeGames = {}


def newGame(chatID, newGame):
    activeGames.update({chatID: newGame})
    return newGame

def getGame(chatID):
    return activeGames.get(chatID)

def stopGame(chatID):
    activeGames.pop(chatID)

# -----------------------------------------------------------------------
# Игра кмн


class GameRPS():
    values = ["Камень", "Ножницы", "Бумага"]
    def __init__(self):
        self.computerChoice = self.__class__.getRandomChoice()

    def newGame(self):
        self.computerChoice = self.__class__.getRandomChoice()

    @classmethod
    def getRandomChoice(cls):
        lenValues = len(cls.values)
        import random
        rndInd = random.randint(0, lenValues - 1)
        return cls.values[rndInd]

    def playerChoice(self, player1Choice):
        winner = None
        code = player1Choice[0] + self.computerChoice[0]
        if player1Choice == self.computerChoice:
            winner = "Ничья!"
        elif code == "КН" or code == "БК" or code == "НБ":
            winner = "Молодец, ты победил!"
        else:
            winner = "Ха-ха, я выиграл!"

        return f"{player1Choice} vs {self.computerChoice} = " + winner


def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text
    if ms_text in GameRPS.values:
        GRPS = GameRPS()
        text_game = GRPS.playerChoice(ms_text)
        bot.send_message(chat_id, text=text_game)
        # text_game = GameRPS.playerChoice(ms_text)
        # bot.send_message(chat_id, playerChoice())
        GRPS.newGame()






