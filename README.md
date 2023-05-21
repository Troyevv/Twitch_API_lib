Документация для TwitchAPI:

Класс TwitchAPI предоставляет методы для взаимодействия с Twitch API и получения информации о стриминге, стримере, зрителях, клипах и подписчиках.

Конструктор класса TwitchAPI:
python
Copy code
def __init__(self, username, client_id, client_secret)
username (строка): Имя пользователя Twitch, для которого вы хотите получить информацию.
client_id (строка): Идентификатор клиента Twitch API.
client_secret (строка): Секрет клиента Twitch API.
Методы класса TwitchAPI:
get_token(): Получает авторизационный токен, необходимый для доступа к Twitch API.

get_stream_info(): Получает информацию о текущем потоке.

Возвращает: JSON-объект с данными о текущем потоке. Пример:

python
Copy code
{
    'data': [
        {
            'id': '123456789',
            'user_id': '987654321',
            'user_name': 'example_user',
            'game_id': '54321',
            'type': 'live',
            'title': 'Example Stream',
            'viewer_count': 100,
            'started_at': '2023-05-20T12:34:56Z',
            'language': 'en',
            'thumbnail_url': 'https://example.com/thumbnail.jpg',
            'tag_ids': ['123', '456']
        }
    ]
}
is_stream_online(): Проверяет, транслируется ли поток в данный момент.

Возвращает: True, если поток транслируется, и False, если поток не активен.
channel_image(): Возвращает URL профильного изображения стримера.

Возвращает: URL профильного изображения стримера.
get_viewers_count(): Возвращает количество зрителей текущего потока.

Возвращает: Количество зрителей текущего потока.
get_title(): Возвращает заголовок текущего потока.

Возвращает: Заголовок текущего потока.
get_game(): Возвращает название игры, которую стример в данный момент транслирует.

Возвращает: Название игры, которую стример транслирует.
get_started_at(): Возвращает время начала текущего потока.

Возвращает: Время начала текущего потока в формате ISO 8601.
stream_duration(timezone): Возвращает продолжительность текущего потока в указанном часовом поясе.

Параметры:

timezone (строка): Часовой пояс для вычисления продолжительности потока.
Возвращает: Продолжительность текущего потока в формате datetime.timedelta.

get_broadcaster_id(): Возвращает идентификатор стримера.

Возвращает: Идентификатор стримера.
get_chatters(): Возвращает информацию о зрителях и модераторах текущего потока.

Возвращает: JSON-объект с данными о зрителях и модераторах текущего потока.
create_clip(): Создает клип текущего потока.

Возвращает: Идентификатор созданного клипа.
get_clips(id_clip=None, broadcaster_id=None, game_id=None, started_at=None, ended_at=None): Получает информацию о клипах на основе указанных параметров.

Параметры:

id_clip (строка): Идентификатор клипа.
broadcaster_id (строка): Идентификатор стримера.
game_id (строка): Идентификатор игры.
started_at (строка): Начальная дата и время для фильтрации клипов.
ended_at (строка): Конечная дата и время для фильтрации клипов.
Возвращает: JSON-объект с данными о клипах, удовлетворяющих заданным параметрам.

get_followers(user_id=None): Получает информацию о подписчиках стримера.

Параметры:

user_id (строка): Идентификатор пользователя.
Возвращает: JSON-объект с данными о подписчиках стримера.

Исключения:
MissingParamsError: Вызывается, если не указаны необходимые параметры для выполнения запроса к API.

APIError: Вызывается, если возникает ошибка при выполнении запроса к Twitch API. Содержит информацию о коде статуса и сообщении ошибки.

Пример использования библиотеки:

python
Copy code
import requests
import pytz
import datetime
import json

# Создаем экземпляр класса TwitchAPI
twitch = TwitchAPI(username="example_user", client_id="your_client_id", client_secret="your_client_secret")

# Проверяем, транслируется ли поток в данный момент
is_online = twitch.is_stream_online()
print(is_online)

# Получаем URL профильного изображения стримера
image_url = twitch.channel_image()
print(image_url)

# Получаем количество зрителей текущего потока
viewers_count = twitch.get_viewers_count()
print(viewers_count)

# Получаем заголовок текущего потока
title = twitch.get_title()
print(title)

# Получаем название игры, которую стример в данный момент транслирует
game_name = twitch.get_game()
print(game_name)

# Получаем время начала текущего потока
started_at = twitch.get_started_at()
print(started_at)

# Получаем продолжительность текущего потока в указанном часовом поясе
duration = twitch.stream_duration(timezone="Europe/Moscow")
print(duration)

# Получаем информацию о зрителях и модераторах текущего потока
chatters = twitch.get_chatters()
print(chatters)

# Создаем клип текущего потока
clip_id = twitch.create_clip()
print(clip_id)

# Получаем информацию о клипах
clips = twitch.get_clips(started_at="2023-05-20T00:00:00Z", ended_at="2023-05-20T23:59:59Z")
print(clips)

# Получаем информацию о подписчиках стримера
followers = twitch.get_followers()
print(followers)
Это основная документация по классу TwitchAPI и его методам. Вы можете использовать эти методы для взаимодействия с Twitch API и получения различных данных о стриминге на Twitch.
