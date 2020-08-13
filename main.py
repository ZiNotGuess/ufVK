import datetime
import time
import requests
from SettingsReader import Params


def VkMethod(methodName: str, methodParams: dict = None) -> dict or list or str or int:
    """
    :param methodName: название метода
    :param methodParams: параметры метода
    :return: ответ ВКонтакте
    """
    if methodParams is None:
        methodParams = {}
    methodParams['v'] = params.getScriptParams("apiVersion")
    methodParams['access_token'] = params.getScriptParams("access_token")
    r = requests.post('https://api.vk.com/method/' + methodName, methodParams)
    r_json = r.json()
    if 'error' in r_json:
        raise requests.exceptions.RequestException(f'[{r_json["error"]["error_code"]}] '
                                                   f'{r_json["error"]["error_msg"]}')
    return r_json['response']


numbers = {'0': '0⃣', '1': '1⃣', '2': '2⃣', '3': '3⃣', '4': '4⃣', '5': '5⃣', '6': '6⃣', '7': '7⃣',
           '8': '8⃣', '9': '9⃣'}
params = Params()
while True:
    try:
        if params.getScriptParams("status"):
            status = ''
            if params.getStatusParams("time"):
                t = datetime.datetime.now()
                status += f"🕰 {t.strftime('%H:%M')} | 🗓 {t.strftime('%d.%m.%Y')} | "

            if params.getStatusParams("photoProfile") and params.getStatusParams("photoLikeCount"):
                LikeCount = VkMethod('photos.get', {'album_id': 'profile', 'rev': 1, 'extended': 1, 'count': 1})
                status += f"❤ На аве: {LikeCount['items'][0]['likes']['count']} | "

            if params.getStatusParams("followersCount"):
                FollowersCount = VkMethod('users.getFollowers', {'count': '1000'})
                status += f"👥 Подписиков: {FollowersCount['count']} | "

            if params.getStatusParams("unreadMessagesCount"):
                MessageCount = VkMethod('account.getCounters', {'filter': 'messages'})
                status += f"📬 Сообщений: {MessageCount['messages']} | "

            if params.getStatusParams("blackListMemberCount"):
                memberCount = VkMethod('account.getBanned', {'count': '200'})
                status += f"⛔ В ЧС: {memberCount['count']} | "

            if params.getStatusParams("giftsCount"):
                gifts = VkMethod('gifts.get', {'count': '200'})
                status += f"🎁 Подарки: {gifts['count']} | "

            if params.getStatusParams("decor"):
                for number in numbers:
                    status = status.replace(number, numbers[number])

            VkMethod("status.set", {"text": status[:-3]})

        if params.getScriptParams("eternalOnline"):
            VkMethod("account.setOnline")

        if params.getScriptParams("deleteAllFriendsRequests"):
            VkMethod("friends.deleteAllRequests")

    except Exception as Error:
        t = datetime.datetime.now()  # получение полного времени для ошибки
        print('При установки статуса произошла ошибка. Убедитесь, что все настройки в settings.ini введены правильно'
              f'\nВремя:\n {t.strftime("%H:%M")}\nОшибка:\n{str(Error)}\n{"--" * 5}')

    finally:
        time.sleep(int(params.getScriptParams("timeToSleep")))
