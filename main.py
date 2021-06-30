import datetime
import time
import requests
from SettingsReader import SettingsReader


def vk_method(name: str, params: dict = None):
    """
    :param name: название метода
    :param params: параметры метода
    :return: ответ ВКонтакте
    """
    if params is None:
        params = {}
    params['v'] = settings.get_param("api_version")
    params['access_token'] = settings.get_param("access_token")
    r = requests.post('https://api.vk.com/method/' + name, params)
    r_json = r.json()
    if 'error' in r_json:
        raise requests.exceptions.RequestException(f'[{r_json["error"]["error_code"]}] '
                                                   f'{r_json["error"]["error_msg"]}')
    return r_json['response']


numbers = {'0': '0⃣', '1': '1⃣', '2': '2⃣', '3': '3⃣', '4': '4⃣', '5': '5⃣', '6': '6⃣', '7': '7⃣',
           '8': '8⃣', '9': '9⃣'}
settings = SettingsReader()
while True:
    try:
        if settings.get_param("status"):
            status = ''
            if settings.get_status_param("time"):
                t = datetime.datetime.now()
                status += f"🕰 {t.strftime('%H:%M')} | 🗓 {t.strftime('%d.%m.%Y')} | "

            if settings.get_status_param("photo_like_count"):
                like_count = vk_method('photos.get', {'album_id': 'profile', 'rev': 1, 'extended': 1, 'count': 1})
                status += f"❤ На аве: {like_count['items'][0]['likes']['count']} | "

            if settings.get_status_param("followers_count"):
                followers_count = vk_method('users.getFollowers', {'count': '1000'})
                status += f"👥 Подписчиков: {followers_count['count']} | "

            if settings.get_status_param("unread_messages_count"):
                message_count = vk_method('account.getCounters', {'filter': 'messages'})
                status += f"📬 Сообщений: {message_count['messages']} | "

            if settings.get_status_param("blacklist_member_count"):
                blacklist_member_count = vk_method('account.getBanned', {'count': '200'})
                status += f"⛔ В ЧС: {blacklist_member_count['count']} | "

            if settings.get_status_param("gifts_count"):
                gifts = vk_method('gifts.get', {'count': '200'})
                status += f"🎁 Подарки: {gifts['count']} | "

            if settings.get_status_param("decor"):
                for number in numbers:
                    status = status.replace(number, numbers[number])

            vk_method("status.set", {"text": status[:-3]})

        if settings.get_param("eternal_online"):
            vk_method("account.setOnline")

        if settings.get_param("delete_all_friends_requests"):
            vk_method("friends.deleteAllRequests")

    except Exception as Error:
        t = datetime.datetime.now()
        print('При установки статуса произошла ошибка. Убедитесь, что все настройки в settings.ini введены правильно'
              f'\nВремя:\n {t.strftime("%H:%M")}\nОшибка:\n{str(Error)}\n{"--" * 5}')

    finally:
        time.sleep(int(settings.get_param("time_to_sleep")))
