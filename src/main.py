import telebot
from decouple import config
from src.botrequests import lowprice
from src.botrequests import highprice
from src.botrequests import bestdeal
from telebot import types
from typing import List

RAPIDAPI_KEY = config('RAPIDAPI_KEY')
BOT_TOKEN = config('TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
headers: dict = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': RAPIDAPI_KEY
}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: types.Message):
    bot.send_message(message.chat.id, "Привет. Я помогу тебе найти отель. Команды:"
                                      "\n/lowprice - Найти самые дешевые"
                                      "\n/highprice - Найти самые дорогие"
                                      "\n/bestdeal - Найти по расстоянию от центра и цене")


@bot.message_handler(commands=['lowprice'])
def send_low_price_hotels(message):
    """
    Спрашиваем у пользователя в какой город он собирается поехать и переходим к функции запроса кол-ва отелей.
    В эту функцию передаем город и команду которую запросил пользователь
    """
    city: types.Message = bot.send_message(message.chat.id, 'Где ищем?')
    bot.register_next_step_handler(city, ask_number_hotels, command='lowprice')


@bot.message_handler(commands=['highprice'])
def send_high_price_hotels(message):
    """
    Спрашиваем у пользователя в какой город он собирается поехать и переходим к функции запроса кол-ва отелей.
    """
    city = bot.send_message(message.chat.id, 'Где ищем?')
    bot.register_next_step_handler(city, ask_number_hotels, command='highprice')


@bot.message_handler(commands=['bestdeal'])
def send_bestdeal_hotels(message):
    """
    Спрашиваем у пользователя в какой город он собирается поехать и переходим к функции запроса кол-ва отелей.
    """
    city: types.Message = bot.send_message(message.chat.id, 'Где ищем?')
    bot.register_next_step_handler(city, ask_price)


def ask_price(message: types.Message):
    """
    Спрашиваем у пользователя диапазон цен и расстояния от центра.
    message переводим в строку и присваиваем его переменной city, чтобы передать в следующую функцию.
    """
    city: str = message.text
    user_price: types.Message = bot.send_message(message.chat.id, 'Введите диапазон цен (в рублях), '
                                                                  'например - "500 2500" ')
    bot.register_next_step_handler(user_price, ask_distance, city)


def ask_distance(message: types.Message, city: str):
    """
    Создаем список из диапазона цен (минимум и максимум)
    Спрашиваем у пользователя диапазон дистанции.
    Потом переходим в функцию запроса кол-ва отелей
    :param message: диапазон цен пользователя
    :param city: город
    """
    user_price: List[str] = message.text.split()
    user_distance: types.Message = bot.send_message(message.chat.id, 'Введите диапазон расстояния от центра '
                                                                     'в километрах, напрмер - "0.5 2"')
    bot.register_next_step_handler(user_distance, ask_number_hotels_best_deals, user_price, city)


def ask_number_hotels_best_deals(message: types.Message, user_price: List[str], city: str):
    """
    Создаем список из диапазона расстояний (минимум и максимум)
    Вызываем функцию get_properties_list для получения списка отелей в границах цены пользователя,
    кроме цен, передаем в нее верхнюю границу расстояния (для лучшего отбора отелей)
    Запрашиваем у пользователя сколько показать ему отелей в результате
    Переходим к функции вывода результата

    :param message: types.Message диапазон расстояний
    :param user_price: список из диапазона цен
    :param city:  город
    """
    user_distance: List[str] = message.text.split()
    hotels: List[dict] = bestdeal.get_properties_list(city, user_price[0], user_price[1], user_distance[1])
    count_of_hotels = bot.send_message(message.chat.id, 'Сколько отелей показать в результате?')
    bot.register_next_step_handler(count_of_hotels, show_result, hotels, 'bestdeal', user_distance[0], user_distance[1])


def ask_number_hotels(message, command):
    """
    Переводим город в строку. И в зависимости от того какая у нас команда, вызывает функцию, которая вернет список
    отелей в городе.
    Спращиваем у пользователя сколько отелей вывести в результате. Переходим к функции вывода результата в которую
    передаем кол-во отелей, список отелей, команду
    :param command: команда выбранная пользователем
    :param message: город
    """
    bot.send_message(message.chat.id, 'Обзваниваю отели. Подождите, пожалуйста')
    city: str = message.text
    if command == 'lowprice':
        hotels: List[dict] = lowprice.get_properties_list(city)
    else:
        hotels: List[dict] = highprice.get_properties_list(city)
    count_of_hotels: types.Message = bot.send_message(message.chat.id, 'Сколько отелей вывести в результат?')
    bot.register_next_step_handler(count_of_hotels, show_result, hotels, command)


def show_result(message, hotels, command, dist_min=None, dist_max=None):
    """
    В зависимости от команды пользователя, вызываем функцию, которая отправляет в чат информацию об отелях

    :param dist_max: верхняя граница по расстоянию
    :param dist_min: нижняя граница по расстоянию
    :param message: кол-во отелей
    :param hotels: список отелей
    :param command: команда пользователя
    """
    count_of_hotels: int = int(message.text)
    if command == 'lowprice':
        hotels: List[dict] = lowprice.get_hotels_info(hotels, count_of_hotels)
    elif command == 'highprice':
        hotels: List[dict] = highprice.get_hotels_info(hotels, count_of_hotels)
    elif command == 'bestdeal':
        hotels: List[dict] = bestdeal.get_hotels_info(hotels, count_of_hotels, dist_min, dist_max)
    for i in range(count_of_hotels):
        bot.send_message(message.from_user.id, 'Название отеля: {name}\n'
                                               'Адрес: {address}\n'
                                               'Расстояние до центра: {dist}\n'
                                               'Цена: {price}'.format(name=hotels[i]['name'],
                                                                      address=hotels[i]['addres'],
                                                                      dist=hotels[i]['distance_to_center'],
                                                                      price=hotels[i]['price']))


bot.infinity_polling()
