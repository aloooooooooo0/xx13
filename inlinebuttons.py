import json
import os

if_heroku = ""

if os.environ.get('HEROKU'):
    if_heroku = "gameXO/"

class Translation:
    __players = {}
    __menu_translation_path = f'{if_heroku}menu.json'
    __xo_translation_path = f'{if_heroku}xo.json'
    __hm_translation_path = f'{if_heroku}hangman.json'

    @classmethod
    def get_menu_expression(cls, key: str, user_id: int) -> str:
        """
        Метод получения выражения из menu.json по ключу.

        :param key: Ключ.
        :param user_id: ID пользователя.
        :return: Выражение.
        """

        with open(cls.__menu_translation_path, "r", encoding="utf8") as read:
            return json.load(read)[key][cls.__players[user_id]]

    @classmethod
    def get_xo_menu_expression(cls, key, user_id):
        """
        Метод получения xo_menu выражения из xo.json по ключу.

        :param key: Ключ.
        :param user_id: ID пользователя.
        :return: Выражение.
        """
        with open(cls.__xo_translation_path, "r", encoding="utf8") as read:
            return json.load(read)["xo_menu"][key][user_id]

    @classmethod
    def get_xo_log_expression(cls, key):
        """
        Метод получения xo_logs выражения из xo.json по ключу.

        :param key: Ключ.
        :return: Выражение.
        """
        with open(cls.__xo_translation_path, "r", encoding="utf8") as read:
            return json.load(read)["xo_logs"][key]

    @classmethod
    def get_hangman_exp(cls, key, user_id):
        """
        Метод получения выражения из hangman.json по ключу.

        :param key: Ключ.
        :param user_id: ID пользователя.
        :return: Выражение.
        """
        if user_id not in cls.__players:
            cls.__players[user_id] = 0
        with open(cls.__hm_translation_path, "r", encoding="utf8") as read:
            return json.load(read)[key][cls.__players[user_id]]