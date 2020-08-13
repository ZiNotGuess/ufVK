import configparser
import os


class Params:
    def __init__(self):
        if not os.path.exists("settings.ini"):
            raise FileExistsError("Вы удалили конфиурационный файл settings.ini")
        self.config = configparser.ConfigParser()
        self.config.read("settings.ini")

    def getScriptParams(self, arg: str) -> str:
        """
        Параметры скрипта
        :param arg: название параметра
        :return: значение
        """
        value = self.config["Script"][arg]
        return True if value.lower() == "true" else False if value.lower() == "false" else value

    def getStatusParams(self, arg: str) -> str:
        """
        Параметры статуса
        :param arg: название параметра
        :return: значение
        """
        value = self.config["Status"][arg]
        return True if value.lower() == "true" else False
