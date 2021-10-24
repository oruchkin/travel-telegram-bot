import telebot
from decouple import config
from src.botrequests import lowprice
from src.botrequests import highprice
from src.botrequests import bestdeal
from telebot import types
from typing import List

gl = None

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
                                      "\n/lowprice - Найти самые дешевые")


@bot.message_handler(commands=['lowprice'])
def send_low_price_hotels(message):
    """
    Спрашиваем у пользователя в какой город он собирается поехать и переходим к функции запроса кол-ва отелей.
    В эту функцию передаем город и команду которую запросил пользователь
    """
    city: types.Message = bot.send_message(message.chat.id, 'Где ищем?')
    bot.register_next_step_handler(city, ask_number_hotels)


def ask_number_hotels(message):
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
    hotels: List[dict] = lowprice.get_properties_list(city)
    count_of_hotels: types.Message = bot.send_message(message.chat.id, 'Сколько отелей вывести в результат?')
    bot.register_next_step_handler(count_of_hotels, ask_photos, hotels)


def ask_photos(message, hotels):
    """
    Спрашиваем нужно ли фото, если нужно но переходим в функцию запроса кол-ва фотографий, если нет то в функцию
    вывода результата
    :param message:
    :param hotels:
    :param command:
    :param dist_min:
    :param dist_max:
    :return:
    """
    count_of_hotels = int(message.text)
    ask_photo = bot.send_message(message.chat.id, 'Хотите увидеть фото? (да/нет)')
    bot.register_next_step_handler(ask_photo, ask_count_photo, count_of_hotels, hotels)


def ask_count_photo(message, count_of_hotels, hotels):
    """
    Проверяем хочет ли пользователь фотографии, если нет то выводить результат, если да - переходим в функцию
    запроса количества фотографий

    :param ask_photo:
    :param message:
    :param count_of_hotels:
    :param hotels:
    :param command:
    :param dist_min:
    :param dist_max:
    :return:
    """
    print('message', message)
    print('message.text', message.text)
    if message.text == 'нет':
        print('условие выполнено')
        bot.register_next_step_handler(message, show_result, count_of_hotels, hotels)
    else:
        print('не выполнено')
        bot.register_next_step_handler(message, show_result, count_of_hotels, hotels)


def show_result(message, count_of_hotels, hotels):
    """
    В зависимости от команды пользователя, вызываем функцию, которая отправляет в чат информацию об отелях

    :param count_of_hotels:
    :param dist_max: верхняя граница по расстоянию
    :param dist_min: нижняя граница по расстоянию
    :param message: кол-во отелей
    :param hotels: список отелей
    :param command: команда пользователя
    """
    print('Show result')
    hotels: List[dict] = lowprice.get_hotels_info(hotels, count_of_hotels)
    for i in range(count_of_hotels):
        bot.send_message(message.chat.id, 'Название отеля: {name}\n'
                                               'Адрес: {address}\n'
                                               'Расстояние до центра: {dist}\n'
                                               'Цена: {price}'.format(name=hotels[i]['name'],
                                                                      address=hotels[i]['addres'],
                                                                      dist=hotels[i]['distance_to_center'],
                                                                      price=hotels[i]['price']))


bot.infinity_polling()
