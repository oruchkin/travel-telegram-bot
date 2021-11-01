import telebot
from decouple import config
from src.botrequests import lowprice
from src.botrequests import highprice
from telebot import types
from typing import List

RAPIDAPI_KEY = config('RAPIDAPI_KEY')
BOT_TOKEN = config('TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
headers: dict = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': RAPIDAPI_KEY
}


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.command = None
        self.city = None
        self.count_of_hotels = None
        self.photo = False
        self.count_of_photo = None


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
    user = User(message.chat.id)
    user.command = 'lowprice'
    city: types.Message = bot.send_message(message.chat.id, 'Где ищем?')
    bot.register_next_step_handler(city, check_city, user)


@bot.message_handler(commands=['highprice'])
def send_low_price_hotels(message):
    """
    Спрашиваем у пользователя в какой город он собирается поехать и переходим к функции запроса кол-ва отелей.
    В эту функцию передаем город и команду которую запросил пользователь
    """
    user = User(message.chat.id)
    user.command = 'highprice'
    city: types.Message = bot.send_message(message.chat.id, 'Где ищем?')
    bot.register_next_step_handler(city, ask_number_hotels, user)


def check_city(message: types.Message, user):
    """
    Парсим по запрошенному город и предлагаем пользователю выбрать из всех совпадений которые найдены в API
    В cities у нас находится список [[full_city_name, id_city], [full_city_name, id_city], [full_city_name, id_city]..]

    :param message: запрошенный город
    """
    cities_button = types.InlineKeyboardMarkup()
    user.city = message.text
    cities = lowprice.check_city(user.city)
    for city in cities:
        button = types.InlineKeyboardButton(text=city[0], callback_data=city[1], user=user)
        cities_button.add(button)
    bot.send_message(message.chat.id, 'Выберите город:', reply_markup=cities_button)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    print(call.message)
    print(call.data)


def ask_number_hotels(message: types.Message, user):
    """
    Переводим город в строку. И в зависимости от того какая у нас команда, вызывает функцию, которая вернет список
    отелей в городе.
    Спращиваем у пользователя сколько отелей вывести в результате. Переходим к функции вывода результата в которую
    передаем кол-во отелей, список отелей, команду

    :param user:
    :param message: подтвержденный город
    """
    city: str = message.text
    user.city = city
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                         resize_keyboard=True,
                                         input_field_placeholder='не более 9 отелей')
    keyboard.row('1', '2', '3')
    keyboard.row('4', '5', '6')
    keyboard.row('7', '8', '9')
    count_of_hotels: types.Message = bot.send_message(message.chat.id, 'Сколько отелей вывести в результат?',
                                                      reply_markup=keyboard)
    bot.register_next_step_handler(count_of_hotels, ask_photo, user)


def ask_photo(message: types.Message, user: User):
    """
    Проверяем кол-во запрошенное пользователем, если оно больше разрешенного, то принудительно меняем
    Спрашиваем у пользователя, нужны ли ему фотографии.
    Если пользователь введет не число, то его вернет на шаг назад.

    :param user:
    :param message:
    :return:
    """
    try:
        count_of_hotels = int(message.text)
        user.count_of_hotels = count_of_hotels
        if user.count_of_hotels > 9:
            user.count_of_hotels = 9
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                             resize_keyboard=True,
                                             input_field_placeholder='да/нет')
        keyboard.row('да', 'нет')
        photo_desire: types.Message = bot.send_message(message.chat.id, 'Хотите увидеть фотографии отелей?',
                                                       reply_markup=keyboard)
        bot.register_next_step_handler(photo_desire, ask_number_photo, user)
        types.ReplyKeyboardRemove()
    except ValueError:
        bot.reply_to(message, 'Это должно быть число. Попробуйте еще раз.')
        ask_number_hotels(message, user)


def ask_number_photo(message: types.Message, user):
    """
    Проверяем хочет ли пользователь увидеть фотографии. Есди нет, то переходим к выводу результата без переменной photo,
     если да - то передаем в ту же функцию photo = True

    :param user: объект пользователь
    :param message: ответ на "хотите увидеть фотографии?"
    """
    if message.text.lower() == 'нет':
        show_result(message, user)
    elif message.text.lower() == 'да':
        user.photo = True
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                             resize_keyboard=True,
                                             input_field_placeholder='не более 9 фотографий')
        keyboard.row('1', '2', '3')
        keyboard.row('4', '5', '6')
        keyboard.row('7', '8', '9')
        number_photo: types.Message = bot.reply_to(message, 'Сколько?', reply_markup=keyboard)
        user.photo = True
        bot.register_next_step_handler(number_photo, show_result, user)
    else:
        photo_desire: types.Message = bot.reply_to(message, 'Введите "да" или "нет"')
        bot.register_next_step_handler(photo_desire, ask_number_photo, user)


def show_result(message: types.Message, user):
    """
    Выводим результат перед этим проверим кол-во фотографий, если больше допустимого, тот принудительно меняем число.

    :param user:
    :param message: если фотографии нужны тот тут кол-во фоторгафий, если они не нужны тот тут "нет"
    """
    user.count_of_photo = message.text
    if not user.count_of_photo.isdigit() and user.photo:
        number_photo: types.Message = bot.reply_to(message, 'Введиче число!')
        bot.register_next_step_handler(number_photo, show_result, user)
    else:
        bot.send_message(message.chat.id, 'Обзваниваю отели. Подождите, пожалуйста',
                         reply_markup=types.ReplyKeyboardRemove())

        if user.command == 'lowprice':
            hotels: List[dict] = lowprice.get_hotels_info(user)
        elif user.command == 'highprice':
            hotels: List[dict] = highprice.get_hotels_info(user)
        else:
            hotels = []

        for i in range(user.count_of_hotels):

            if user.photo:
                bot.send_media_group(message.chat.id, hotels[i]['photo'])

            link_booking = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text='Забронировать номер', url=hotels[i]['booking'])
            link_booking.add(button)

            bot.send_message(message.from_user.id, 'Название отеля: {name}\n'
                                                   'Адрес: {address}\n'
                                                   'Расстояние до центра: {dist}\n'
                                                   'Цена: {price}'.format(name=hotels[i]['name'],
                                                                          address=hotels[i]['addres'],
                                                                          dist=hotels[i]['distance_to_center'],
                                                                          price=hotels[i]['price']),
                             reply_markup=link_booking)


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
