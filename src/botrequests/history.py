import sqlite3
import datetime

connect = sqlite3.connect('database.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users("
               "id_user INTEGER NOT NULL PRIMARY KEY,"
               "command TEXT,"
               "date_create TEXT,"
               "city TEXT,"
               "id_city INTEGER,"
               "count_of_hotels INTEGER,"
               "photo bool,"
               "count_of_photo INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS cities(id_city TEXT, city TEXT)")


def create_user(id_user, command):
    """
    Создаем запись в БД. Если такой пользователь уже есть в БД, то обновляем command и записываем текущую дату и время
    :param id_user: id пользователя
    :param command: комманда введенная пользователем
    """
    cursor.execute("SELECT id_user FROM users WHERE id_user=?", (id_user,))
    datetime_now = datetime.datetime.now()
    if not cursor.fetchone():
        sql = "INSERT INTO users(id_user, command, date_create) VALUES(?, ?, ?)"
        cursor.execute(sql, (id_user, command, datetime_now))
        connect.commit()
    else:
        sql = "UPDATE users SET command = ?, date_create = ? WHERE id_user = ?"
        cursor.execute(sql, (command, datetime_now, id_user))
        connect.commit()


def get_command(id_user):
    """
    По id пользователя возвращаем его команду
    :return: str команда
    """
    cursor.execute("SELECT command FROM users WHERE id_user=?", (id_user, ))
    command = cursor.fetchone()
    return command[0]


def create_city(city, id_city):
    """
    Создаем запись в таблице cities. Если такой город уже есть в БД, то ничего не делаем
    :param city: название города
    :param id_city: id города
    """
    cursor.execute("SELECT id_city FROM cities WHERE id_city=?", (id_city, ))
    if not cursor.fetchone():
        sql = "INSERT INTO cities(id_city, city) VALUES(?, ?)"
        cursor.execute(sql, (id_city, city))
        connect.commit()


def get_city(id_city):
    """
    По id Города возвращаем из базы его полное название
    :return: str название города
    """
    cursor.execute("SELECT city FROM cities WHERE id_city=?", (id_city, ))
    city = cursor.fetchone()
    return city[0]


def set_count_of_hotels(id_user, count_of_hotels):
    """
    Записываем в БД кол-во отелей пользователя
    :param count_of_hotels: кол-во отелей
    :param id_user: id пользователя
    """
    sql = "UPDATE users SET count_of_hotels=? WHERE id_user=?"
    cursor.execute(sql, (count_of_hotels, id_user))
    connect.commit()


def set_photo(id_user: int, photo: bool):
    """
    Записываем в БД нужны ли пользователю фотографии
    :param photo:
    :param id_user: id пользователя
    """
    sql = "UPDATE users SET photo=? WHERE id_user=?"
    cursor.execute(sql, (photo, id_user))
    connect.commit()


def set_count_of_photo(id_user: int, count_of_photo: [int, str]):
    """
    Записываем в БД сколько фотографий нужно пользователю
    :param count_of_photo: кол-во фотографий
    :param id_user: id пользователя
    """
    if count_of_photo == 'нет':
        count_of_photo = 0
    sql = "UPDATE users SET count_of_photo=? WHERE id_user=?"
    cursor.execute(sql, (count_of_photo, id_user))
    connect.commit()


def set_city_user(id_city: int, city: str, id_user: int):
    """
    Записываем в таблицу users город и id города
    :param city:
    :param id_city:
    :param id_user: id пользователя
    """
    sql = "UPDATE users SET id_city=?, city=? WHERE id_user=?"
    cursor.execute(sql, (id_city, city, id_user))
    connect.commit()


def get_count_of_photo(id_user):
    """
    По id пользователя кол-во фотографий
    :return: str команда
    """
    cursor.execute("SELECT count_of_photo FROM users WHERE id_user=?", (id_user, ))
    count_of_photo = cursor.fetchone()
    return count_of_photo[0]


def get_count_of_hotels(id_user):
    """
    По id пользователя кол-во отелей
    :return: str команда
    """
    cursor.execute("SELECT count_of_hotels FROM users WHERE id_user=?", (id_user, ))
    count_of_hotels = cursor.fetchone()
    return count_of_hotels[0]


def get_id_city_user(id_user):
    """
    По id пользователя id города
    :return: str команда
    """
    cursor.execute("SELECT id_city FROM users WHERE id_user=?", (id_user, ))
    id_city = cursor.fetchone()
    return id_city[0]


def get_photo(id_user):
    """
    По id пользователя id города
    :return: str команда
    """
    cursor.execute("SELECT photo FROM users WHERE id_user=?", (id_user, ))
    photo = cursor.fetchone()
    return photo[0]

