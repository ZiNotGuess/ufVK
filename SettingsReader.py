import configparser
import os


class GetParams:
    def __init__(self):
        if not os.path.exists("settings.ini"):
            raise FileExistsError("Вы удалили конфиурационный файл settings.ini")
        self.config = configparser.ConfigParser()
        self.config.read("settings.ini")
        scriptsItem = self._paramsGet('Script')
        statusItem = self._paramsGet('Status')
        for i in scriptsItem:
            setattr(Params, i, True if scriptsItem[i].lower() == "true" else
                    False if scriptsItem[i].lower() == "false" else scriptsItem[i])
        for i in statusItem:
            setattr(Params, i, True if statusItem[i].lower() == "true" else False)
        self.par = Params

    def _paramsGet(self, arg):
        return dict(self.config.items(arg))


class Params:
    decorNumber = {'0': '0⃣', '1': '1⃣', '2': '2⃣', '3': '3⃣', '4': '4⃣', '5': '5⃣', '6': '6⃣', '7': '7⃣',
                   '8': '8⃣', '9': '9⃣'}
