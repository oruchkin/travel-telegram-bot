import sqlite3
connect = sqlite3.connect('database.db', check_same_thread=False)
cursor = connect.cursor()


def delete_last_story(id_user) -> None:
    """
    Удаляем запись в БД
    """
    sql = "SELECT date_create FROM users WHERE id_user=?"
    cursor.execute(sql, (id_user, ))
    date_tuple = cursor.fetchall()
    date_create = date_tuple[-1][0]
    sql_delete = "DELETE FROM users WHERE id_user=? and date_create=?"
    cursor.execute(sql_delete, (id_user, date_create))
    connect.commit()


delete_last_story(441815129)