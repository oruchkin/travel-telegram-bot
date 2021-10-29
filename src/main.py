import telebot
from decouple import config
from src.botrequests import lowprice
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
                                      "\n/lowprice - Найти самые дешевые")


@bot.message_handler(commands=['lowprice'])
def send_low_price_hotels(message):
    """
    Спрашиваем у пользователя в какой город он собирается поехать и переходим к функции запроса кол-ва отелей.
    В эту функцию передаем город и команду которую запросил пользователь
    """
    city: types.Message = bot.send_message(message.chat.id, 'Где ищем?')
    bot.register_next_step_handler(city, ask_number_hotels)


def ask_number_hotels(message: types.Message):
    """
    Переводим город в строку. И в зависимости от того какая у нас команда, вызывает функцию, которая вернет список
    отелей в городе.
    Спращиваем у пользователя сколько отелей вывести в результате. Переходим к функции вывода результата в которую
    передаем кол-во отелей, список отелей, команду

    :param message: город
    """
    city: str = message.text
    count_of_hotels: types.Message = bot.send_message(message.chat.id, 'Сколько отелей вывести в результат?'
                                                                       '(не более 10)')
    bot.register_next_step_handler(count_of_hotels, ask_photo, city)


def ask_photo(message: types.Message, city: str):
    """
    Проверяем кол-во запрошенное пользователем, если оно больше разрешенного, то принудительно меняем
    Спрашиваем у пользователя, нужны ли ему фотографии.
    Если пользователь введет не число, то его вернет на шаг назад.

    :param city:
    :param message:
    :return:
    """
    try:
        count_of_hotels = int(message.text)
        if count_of_hotels > 10:
            count_of_hotels = 10
        photo_desire: types.Message = bot.send_message(message.chat.id, 'Хотите увидеть фотографии отелей?')
        bot.register_next_step_handler(photo_desire, ask_number_photo, count_of_hotels, city)
    except ValueError:
        bot.reply_to(message, 'Это должно быть число. Попробуйте еще раз.')
        ask_number_hotels(message)


def ask_number_photo(message: types.Message, count_of_hotels: int, city: str):
    """
    Проверяем хочет ли пользователь увидеть фотографии. Есди нет, то переходим к выводу результата без переменной photo,
     если да - то передаем в ту же функцию photo = True

    :param message: ответ на "хотите увидеть фотографии?"
    :param count_of_hotels: кол-во отелей
    :param city: город
    """
    if message.text.lower() == 'нет':
        show_result(message, count_of_hotels, city)
    elif message.text.lower() == 'да':
        number_photo: types.Message = bot.reply_to(message, 'Сколько? (не более 7)')
        photo: bool = True
        bot.register_next_step_handler(number_photo, show_result, count_of_hotels, city, photo)
    else:
        photo_desire: types.Message = bot.reply_to(message, 'Введите "да" или "нет"')
        bot.register_next_step_handler(photo_desire, ask_number_photo, count_of_hotels, city)


def show_result(message: types.Message, count_of_hotels: int, city: str, photo: bool = False):
    """
    Выводим результат перед этим проверим кол-во фотографий, если больше допустимого, тот принудительно меняем число.

    :param message:
    :param count_of_photo:
    :param photo: необходимость фотографий
    :param city: город
    :param count_of_hotels: количество отелей
    """
    count_of_photo: str = message.text
    if int(count_of_photo) > 7:
        count_of_photo = '7'
    if not count_of_photo.isdigit():
        number_photo: types.Message = bot.reply_to(message, 'Введиче число (но не более 7)')
        bot.register_next_step_handler(number_photo, show_result, count_of_hotels, city, photo)
    else:
        bot.send_message(message.chat.id, 'Обзваниваю отели. Подождите, пожалуйста')
        hotels: List[dict] = lowprice.get_properties_list(city)
        hotels: List[dict] = lowprice.get_hotels_info(hotels, count_of_hotels, photo, count_of_photo)
        for i in range(count_of_hotels):
            if photo:
                for p in range(int(count_of_photo)):
                    bot.send_photo(message.chat.id, hotels[i]['photo'][p])
            bot.send_message(message.from_user.id, 'Название отеля: {name}\n'
                                                   'Адрес: {address}\n'
                                                   'Расстояние до центра: {dist}\n'
                                                   'Цена: {price}'.format(name=hotels[i]['name'],
                                                                          address=hotels[i]['addres'],
                                                                          dist=hotels[i]['distance_to_center'],
                                                                          price=hotels[i]['price']))


bot.infinity_polling()
# def show_result(message, hotels, command, dist_min=None, dist_max=None):
#     """
#     В зависимости от команды пользователя, вызываем функцию, которая отправляет в чат информацию об отелях
#
#     :param dist_max: верхняя граница по расстоянию
#     :param dist_min: нижняя граница по расстоянию
#     :param message: кол-во отелей
#     :param hotels: список отелей
#     :param command: команда пользователя
#     """
#     count_of_hotels: int = int(message.text)
#     if command == 'lowprice':
#         hotels: List[dict] = lowprice.get_hotels_info(hotels, count_of_hotels)
#     elif command == 'highprice':
#         hotels: List[dict] = highprice.get_hotels_info(hotels, count_of_hotels)
#     elif command == 'bestdeal':
#         hotels: List[dict] = bestdeal.get_hotels_info(hotels, count_of_hotels, dist_min, dist_max)
#     for i in range(count_of_hotels):
#         bot.send_message(message.from_user.id, 'Название отеля: {name}\n'
#                                                'Адрес: {address}\n'
#                                                'Расстояние до центра: {dist}\n'
#                                                'Цена: {price}'.format(name=hotels[i]['name'],
#                                                                       address=hotels[i]['addres'],
#                                                                       dist=hotels[i]['distance_to_center'],
#                                                                       price=hotels[i]['price']))

