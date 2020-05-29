import datetime
import time
import requests
from SettingsReader import GetParams


def VkMethod(methodName, methodParams=None):
    """
    :param methodName: имя метода
    :param methodParams: параметры метода
    :return: ответ сервера
    """
    if methodParams is None:
        methodParams = {}
    methodParams['v'] = param.apiversion
    methodParams['access_token'] = param.access_token
    r = requests.post('https://api.vk.com/method/' + methodName, methodParams)
    r_json = r.json()
    if 'error' in r_json:
        raise requests.exceptions.RequestException(f'[{r_json["error"]["error_code"]}] '
                                                   f'{r_json["error"]["error_msg"]}')
    return r_json['response']


param = GetParams().par
while True:
    try:
        if param.status:
            status = ''
            if param.time:
                t = datetime.datetime.now()
                status += f"🕰 {t.strftime('%H:%M')} | 🗓 {t.strftime('%d.%m.%Y')} | "

            if param.photoprofile and param.photolikecount:
                LikeCount = VkMethod('photos.get', {'album_id': 'profile', 'rev': 1, 'extended': 1, 'count': 1})
                status += f"❤ На аве: {LikeCount['items'][0]['likes']['count']} | "

            if param.followerscount:
                FollowersCount = VkMethod('users.getFollowers', {'count': '1000'})
                status += f"👥 Подписиков: {FollowersCount['count']} | "

            if param.unreadmmssagecount:
                MessageCount = VkMethod('account.getCounters', {'filter': 'messages'})
                status += f"📬 Сообщений: {MessageCount['messages']} | "

            if param.blacklistmembercount:
                memberCount = VkMethod('account.getBanned', {'count': '200'})
                status += f"⛔ В ЧС: {memberCount['count']} | "

            if param.giftscount:
                gifts = VkMethod('gifts.get', {'count': '200'})
                status += f"🎁 Подарки: {gifts['count']} | "

            if param.decor:
                for number in param.decorNumber:
                    status = status.replace(number, param.decorNumber[number])

            VkMethod("status.set", {"text": status[:-3]})

        if param.eternalonline:
            VkMethod("account.setOnline")

        if param.deleteallfriendsrequests:
            VkMethod("friends.deleteAllRequests")

    except Exception as Error:
        t = datetime.datetime.now()  # получение полного времени для ошибки
        print('При установки статуса произошла ошибка. Убедитесь, что все настройки в settings.ini введены правильно'
              f'\nВремя:\n {t.strftime("%H:%M")}\nОшибка:\n{str(Error)}\n{"--" * 5}')
    finally:
        time.sleep(int(param.timetosleep))
