import sqlite3
import datetime
from typing import List
import re
from telebot import types

connect = sqlite3.connect('database.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users("
               "id_user INTEGER NOT NULL,"
               "command TEXT,"
               "date_create TEXT,"
               "city TEXT,"
               "id_city INTEGER,"
               "count_of_hotels INTEGER,"
               "photo bool,"
               "count_of_photo INTEGER,"
               "top_price TEXT,"
               "lower_price TEXT,"
               "top_dist TEXT,"
               "lower_dist TEXT,"
               "hotels TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS cities(id_city TEXT, city TEXT)")


def create_user(id_user, command):
    """
    Создаем запись в БД. Если такой пользователь уже есть в БД, то обновляем command и записываем текущую дату и время
    :param id_user: id пользователя
    :param command: комманда введенная пользователем
    """
    datetime_now = datetime.datetime.now()
    date = datetime_now.strftime('%H:%M:%S - %d.%m.%Y')
    sql = "INSERT INTO users(id_user, command, date_create) VALUES(?, ?, ?)"
    cursor.execute(sql, (id_user, command, date))
    connect.commit()
    return date


def get_command(id_user, date_create):
    """
    По id пользователя возвращаем его команду
    :return: str команда
    """
    cursor.execute("SELECT command FROM users WHERE id_user=? and date_create=?", (id_user, date_create))
    command = cursor.fetchone()
    return command[0]


def create_city(city, id_city):
    """
    Создаем запись в таблице cities. Если такой город уже есть в БД, то ничего не делаем
    :param city: название города
    :param id_city: id города
    """
    cursor.execute("SELECT id_city FROM cities WHERE id_city=?", (id_city,))
    if not cursor.fetchone():
        sql = "INSERT INTO cities(id_city, city) VALUES(?, ?)"
        cursor.execute(sql, (id_city, city))
        connect.commit()


def get_city(id_city):
    """
    По id Города возвращаем из базы его полное название
    :return: str название города
    """
    cursor.execute("SELECT city FROM cities WHERE id_city=?", (id_city,))
    city = cursor.fetchone()
    return city[0]


def set_count_of_hotels(id_user, count_of_hotels, date_create):
    """
    Записываем в БД кол-во отелей пользователя
    :param count_of_hotels: кол-во отелей
    :param id_user: id пользователя
    """
    sql = "UPDATE users SET count_of_hotels=? WHERE id_user=? and date_create=?"
    cursor.execute(sql, (count_of_hotels, id_user, date_create))
    connect.commit()


def set_photo(id_user: int, photo: bool, date_create):
    """
    Записываем в БД нужны ли пользователю фотографии
    :param photo:
    :param id_user: id пользователя
    """
    sql = "UPDATE users SET photo=? WHERE id_user=? and date_create=?"
    cursor.execute(sql, (photo, id_user, date_create))
    connect.commit()


def set_count_of_photo(id_user: int, count_of_photo: [int, str], date_create):
    """
    Записываем в БД сколько фотографий нужно пользователю
    :param count_of_photo: кол-во фотографий
    :param id_user: id пользователя
    """
    if count_of_photo == 'нет':
        count_of_photo = 0
    sql = "UPDATE users SET count_of_photo=? WHERE id_user=? and date_create=?"
    cursor.execute(sql, (count_of_photo, id_user, date_create))
    connect.commit()


def set_city_user(id_city: int, city: str, id_user: int, date_create: str):
    """
    Записываем в таблицу users город и id города
    :param city:
    :param id_city:
    :param id_user: id пользователя
    """
    sql = "UPDATE users SET id_city=?, city=? WHERE id_user=? and date_create=?"
    cursor.execute(sql, (id_city, city, id_user, date_create))
    connect.commit()


def get_count_of_photo(id_user, date_create):
    """
    По id пользователя кол-во фотографий
    :return: str команда
    """
    cursor.execute("SELECT count_of_photo FROM users WHERE id_user=? and date_create=?", (id_user, date_create))
    count_of_photo = cursor.fetchone()
    return count_of_photo[0]


def get_count_of_hotels(id_user, date_create):
    """
    По id пользователя кол-во отелей
    :return: str команда
    """
    cursor.execute("SELECT count_of_hotels FROM users WHERE id_user=? and date_create=?", (id_user, date_create))
    count_of_hotels = cursor.fetchone()
    return count_of_hotels[0]


def get_id_city_user(id_user, date_create):
    """
    По id пользователя id города
    :return: str команда
    """
    cursor.execute("SELECT id_city FROM users WHERE id_user=? and date_create=?", (id_user, date_create))
    id_city = cursor.fetchone()
    return id_city[0]


def get_photo(id_user, date_create):
    """
    По id пользователя id города
    :return: str команда
    """
    cursor.execute("SELECT photo FROM users WHERE id_user=? and date_create=?", (id_user, date_create))
    photo = cursor.fetchone()
    return photo[0]


def set_price(prices: List[str], id_user, date_create):
    """
    Записываем в БД нижнюю и верхнюю цены.
    :param id_user:
    :param prices: 0 индекс - нижняя цена, 1 - верхняя
    """
    if len(prices) > 2:
        raise ValueError
    lower_price = int(float(re.sub(',', '.', prices[0])))
    top_price = int(float(re.sub(',', '.', prices[1])))
    sql = "UPDATE users SET lower_price=?, top_price=? WHERE id_user=? and date_create=?"
    cursor.execute(sql, (lower_price, top_price, id_user, date_create))
    connect.commit()


def set_distance(distances: List[str], id_user, date_create):
    """
    Записываем в БД нижнюю и верхнюю цены.
    :param distances: 0 - нижняя граница, 1 - верхняя
    :param id_user:
    """
    if len(distances) > 2:
        raise ValueError
    lower_distance: float = float(re.sub(',', '.', distances[0]))
    top_distance: float = float(re.sub(',', '.', distances[1]))
    sql = "UPDATE users SET lower_dist=?, top_dist=? WHERE id_user=? and date_create=?"
    cursor.execute(sql, (lower_distance, top_distance, id_user, date_create))
    connect.commit()


def get_price(id_user, date_create):
    """
    По id пользователя возвращаем кортеж из границ цен
    :return: str команда
    """
    cursor.execute("SELECT lower_price, top_price FROM users WHERE id_user=? and date_create=?", (id_user, date_create))
    prices = cursor.fetchone()
    return prices


def get_distance(id_user, date_create):
    """
    По id пользователя возвращаем кортеж из границ дистанции от центра
    :return: str команда
    """
    cursor.execute("SELECT lower_dist, top_dist FROM users WHERE id_user=? and date_create=?", (id_user, date_create))
    distances = cursor.fetchone()
    return distances


#
# def get_time(id_user):
#     """
#     По id пользователя время последнего запроса
#     :return: str команда
#     """
#     cursor.execute("SELECT date_create FROM users WHERE id_user=?", (id_user,))
#     time = cursor.fetchone()
#     return time


# def get_city_user(id_user):
#     """
#     По id пользователя город последнего запроса
#     :return: str команда
#     """
#     cursor.execute("SELECT city FROM users WHERE id_user=?", (id_user,))
#     city = cursor.fetchone()
#     return city
#
#
# def get_date(id_user):
#     """
#     По id пользователя время последнего запроса
#     :return: str команда
#     """
#     cursor.execute("SELECT date_create FROM users WHERE id_user=?", (id_user,))
#     date = cursor.fetchone()
#     return date[0]


def set_hotels(id_user: int, hotels: List[dict], date_create):
    """
    Записываем в БД нужны ли пользователю фотографии
    :param hotels:
    :param id_user: id пользователя
    """
    hotels = str(hotels)
    sql = "UPDATE users SET hotels=? WHERE id_user=? and date_create=?"
    cursor.execute(sql, (hotels, id_user, date_create))
    connect.commit()


def get_hotels(id_user, date_create):
    """
    По id пользователя id города
    :return: str команда
    """
    cursor.execute("SELECT hotels FROM users WHERE id_user=? and date_create=?", (id_user, date_create))
    hotels = cursor.fetchone()
    hotels = eval(hotels[0])
    return hotels


def create_media_group(photos: List[str]) -> List[types.InputMediaPhoto]:
    media_group = []
    for photo in photos:
        media_group.append(types.InputMediaPhoto(photo))
    return media_group


def send_history(id_user):
    sql = "SELECT command, date_create, hotels FROM users WHERE user_id=?"
    cursor.execute(sql, (id_user, ))
    history = cursor.fetchall()
    for i in history:
        print(i)
