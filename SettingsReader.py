import configparser
import os


class SettingsReader:
    def __init__(self):
        if not os.path.exists("settings.ini"):
            raise FileExistsError("Вы удалили конфигурационный файл settings.ini")
        self.config = configparser.ConfigParser()
        self.config.read("settings.ini")

    def get_param(self, arg: str) -> str:
        """
        Параметры скрипта
        :param arg: название параметра
        :return: значение
        """
        value = self.config["Script"][arg]
        return True if value.lower() == "true" else False if value.lower() == "false" else value

    def get_status_param(self, arg: str) -> bool:
        """
        Параметры статуса
        :param arg: название параметра
        :return: значение
        """
        value = self.config["Status"][arg]
        return value.lower() == "true"
