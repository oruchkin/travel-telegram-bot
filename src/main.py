import telebot
from decouple import config
from src.botrequests import lowprice
from src.botrequests import highprice
from src.botrequests import bestdeal
from telebot import types
from src.botrequests import history
import configs
from typing import List

RAPIDAPI_KEY = config('RAPIDAPI_KEY')
BOT_TOKEN = config('TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
headers: dict = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': RAPIDAPI_KEY
}


@bot.message_handler(commands=['restart'])
def restart(message: types.Message) -> None:
    """
    Сброс параметров последнего запроса
    """
    history.delete_last_story(message.chat.id)
    bot.send_message(message.chat.id, "Последний запрос сброшен")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: types.Message) -> None:
    """
    Ответ на команды start, help
    """
    bot.send_message(message.chat.id, "Привет. Я помогу тебе найти отель. Команды:"
                                      "\n/help - помощь по командам бота"
                                      "\n/lowprice - вывод самых дешевых отелей в городе"
                                      "\n/highprice - вывод самых дорогих отелей в городе"
                                      "\n/bestdeal - вывод отелей, наиболее подходящих по цене и расположению от центра"
                                      "\n/history - вывод истории поиска отелей")


@bot.message_handler(commands=['lowprice'])
def send_low_price_hotels(message: types.Message) -> None:
    """
    Ответ на команду lowprice
    Спрашиваем у пользователя в каком городе будем искать отель и переходим к функции проверки города в API hotels

    date_create - будем передавать до самой последней функции вывода результата, нужно чтобы записывать все дальнейшие
    данные в БД, совместно с id_user(беререм из message в каждоый функции, чтобы не передавать) - они являются
    идентефикатором каждой отдельной записи в таблице БД.
    """
    id_user: int = message.from_user.id
    date_create: str = history.create_user(id_user, 'lowprice')

    city = bot.send_message(message.chat.id, 'Где ищем?')
    bot.register_next_step_handler(city, check_city, date_create)


@bot.message_handler(commands=['highprice'])
def send_high_price_hotels(message: types.Message) -> None:
    """
    Ответ на команду highprice
    Спрашиваем у пользователя в каком городе будем искать отель и переходим к функции проверки города в API hotels

    date_create - будем передавать до самой последней функции вывода результата, нужно чтобы записывать все дальнейшие
    данные в БД, совместно с id_user(беререм из message в каждоый функции, чтобы не передавать) - они являются
    идентефикатором каждой отдельной записи в таблице БД.
    """
    id_user: int = message.from_user.id
    date_create: str = history.create_user(id_user, 'highprice')

    city = bot.send_message(message.chat.id, 'Где ищем?')
    bot.register_next_step_handler(city, check_city, date_create)


@bot.message_handler(commands=['bestdeal'])
def send_high_price_hotels(message: types.Message) -> None:
    """
    Ответ на команду bestdeal
    Спрашиваем у пользователя в каком городе будем искать отель и переходим к функции проверки города в API hotels

    date_create - будем передавать до самой последней функции вывода результата, нужно чтобы записывать все дальнейшие
    данные в БД, совместно с id_user(беререм из message в каждоый функции, чтобы не передавать) - они являются
    идентефикатором каждой отдельной записи в таблице БД.
    """
    id_user: int = message.from_user.id
    date_create: str = history.create_user(id_user, 'bestdeal')

    city = bot.send_message(message.chat.id, 'Где ищем?')
    bot.register_next_step_handler(city, check_city, date_create)


@bot.message_handler(commands=['history'])
def send_history(message: types.Message) -> None:
    """
    Ответ на команду history
    Выдаем результат последних number_stories(число задается в файле configs.py) запросов (история).
    При помощи метода history.send_history(message.chat.id) возвращаем необходимые для вывода данные в виде списка
    списков строк(Каждый вложенный список (story) содержит информацию об одном запросе - команду, время создания записи
    в БД, город(в формате для вывода пользователю) и время создания записи в неизмененном формате(чтобы передать в
    функцию show_result)
    В data мы добавляем строку "history", чтобы handler понял, откуда пришла инфа.
    Если пользователь ранее не делал запросы то его история пуста
    """
    hist: List[str] = history.send_history(message.chat.id)
    if hist:
        bot.send_message(message.chat.id, 'Последние запросы : '.format(len(hist)))
        for story in hist:
            restart_button = types.InlineKeyboardMarkup()
            data: str = ''.join([story[-1], 'history'])
            button = types.InlineKeyboardButton(text='Повторить запрос', callback_data=data)
            restart_button.add(button)
            bot.send_message(message.chat.id, ''.join(story[:-1]), reply_markup=restart_button)
    else:
        bot.send_message(message.chat.id, 'История пуста.')


def check_city(message: types.Message, date_create: str) -> None:
    """
    Парсим по запрошенному городу и предлагаем пользователю выбрать из всех совпадений которые найдены в API
    В cities у нас находится список [[full_city_name, id_city], [full_city_name, id_city], [full_city_name, id_city]..]
    В callback передаваемые данных передаем id города, который выбрал пользователь и date_create
    Записываем отдельную таблицу в БД(содержит только город и id), чтобы в call_back_handler по id определить
    название города и отправить в чат с пользователем
    :param date_create: время ввода команды
    :param message: введенный пользователем город
    """
    city: str = message.text
    cities: List[List[str]] = lowprice.check_city(city)
    cities_button = types.InlineKeyboardMarkup()

    for city in cities:
        history.create_city(city[0], city[1])

        data: str = '|'.join([city[1], date_create])
        button = types.InlineKeyboardButton(text=city[0], callback_data=data)
        cities_button.add(button)

    bot.send_message(message.chat.id, 'Выберите город:', reply_markup=cities_button)


@bot.callback_query_handler(func=lambda call: True)
def answer(call: types.CallbackQuery) -> None:
    """
    Ловим нажатие пользователя на кнопку!
    Если данные с кнопки заканчиваются на history, значит пользователь запрашивает повторный вывод из истории,
    следовательно отправляем его в функцию вывода результата. из callback данных убираем последнием 7 символов (history)
    и получаем время создания строки в таблице БД.
    В противном же случае:
    Записываем окончательный выбор города в БД (id и имя) и переходим к функции кол-ва отелей
    В завимимости от команды пользователя отправляем в следующую функцию
    """
    if call.data.endswith('history'):
        show_result(call.message.chat.id, call.data[:-7])
    else:
        data: List[str] = call.data.split('|')
        date_create: str = data[1]
        id_city: str = data[0]

        city: str = history.get_city(id_city)
        text: str = 'Ты выбрал:\n{}'.format(city)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text)
        history.set_city_user(id_city, city, call.message.chat.id, date_create)

        if history.get_command(call.message.chat.id, date_create) == 'bestdeal':
            ask_price(call.message.chat.id, date_create)
        else:
            ask_number_hotels(call.message.chat.id, date_create)


def ask_price(id_user: int, date_create: str) -> None:
    """
    Спрашиваем у пользователя диапазон цен.
    Переходим в функцию запроса дистанции от центра
    :param id_user: id пользователя
    :param date_create: Дата ввода команды пользователем
    """
    user_price: types.Message = bot.send_message(id_user, 'Введите диапазон цен (в рублях, через пробел), '
                                                          'например - "500 2500" ')
    bot.register_next_step_handler(user_price, ask_distance, date_create)


def ask_distance(message: types.Message, date_create: str) -> None:
    """
    Создаем список из диапазона цен (минимум и максимум), записываем в БД, если пользователь ввел что-то некорректо -
    ловим исключение и отправляем в функцию запроса цены.
    Записываем диапазон цен в БД
    Спрашиваем у пользователя диапазон дистанции.
    Переходим в функцию проверки дистанции
    :param date_create: Дата ввода команды пользователем
    :param message: диапазон цен пользователя
    """
    try:
        prices: List[str] = message.text.split(' ')
        history.set_price(prices, message.chat.id, date_create)

        user_distance: types.Message = bot.send_message(message.chat.id, 'Введите диапазон расстояния от центра '
                                                                         'в километрах, напрмер - "0.5 2"')
        bot.register_next_step_handler(user_distance, check_distance, date_create)
    except (IndexError, SyntaxError, ValueError):
        ask_price(message.chat.id, date_create)


def check_distance(message: types.Message, date_create: str) -> None:
    """
    Проверяем, что ввел пользователь в диапазоне расстояний и записываем в БД. Переходим на запрос кол-ва отелей
    :param date_create: Дата ввода команды пользователем
    :param message: диапазон расстояний от центра
    """
    try:
        distances: List[str] = message.text.split(' ')
        history.set_distance(distances, message.chat.id, date_create)
        ask_number_hotels(message.chat.id, date_create)
    except (IndexError, SyntaxError, ValueError):
        user_distance: types.Message = bot.send_message(message.chat.id, 'Введите диапазон расстояния от центра '
                                                                         'в километрах, напрмер - "0.5 2"')
        bot.register_next_step_handler(user_distance, check_distance)


def ask_number_hotels(id_user: int, date_create: str) -> None:
    """
    Запрос кол-ва отелей
    Создаем клавиатуру из 9 кнопок и отправляем пользователю
    Переходим в функцию запроса необходимости вывода фотографий
    :param date_create: Дата ввода команды пользователем
    :param id_user: id пользователя
    """

    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                         resize_keyboard=True,
                                         input_field_placeholder='не более 9 отелей')
    keyboard.row('1', '2', '3')
    keyboard.row('4', '5', '6')
    keyboard.row('7', '8', '9')
    count_of_hotels: types.Message = bot.send_message(id_user, 'Сколько отелей вывести в результат?',
                                                      reply_markup=keyboard)

    bot.register_next_step_handler(count_of_hotels, ask_photo, date_create)


def ask_photo(message: types.Message, date_create: str) -> None:
    """
    Проверяем кол-во запрошенное пользователем, если оно больше разрешенного(файл configs.py), то принудительно меняем.
    Спрашиваем у пользователя, нужны ли ему фотографии.
    Если пользователь введет не число или дробное число, то его вернет на шаг назад.
    Записываем в БД кол-во отелей
    Переходим в функцию запроса кол-ва фотографий
    :param date_create: Дата ввода команды пользователем
    :param message: кол-во отелей, запрошенное пользователем
    """
    try:
        count_of_hotels: int = int(message.text)
        if count_of_hotels > configs.count_of_hotels:
            count_of_hotels: int = configs.count_of_hotels
        history.set_count_of_hotels(message.chat.id, count_of_hotels, date_create)

        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                             resize_keyboard=True,
                                             input_field_placeholder='да/нет')
        keyboard.row('да', 'нет')
        photo_desire: types.Message = bot.send_message(message.chat.id, 'Хотите увидеть фотографии отелей?',
                                                       reply_markup=keyboard)
        bot.register_next_step_handler(photo_desire, ask_number_photo, date_create)
        types.ReplyKeyboardRemove()
    except ValueError:
        bot.reply_to(message, 'Это должно быть целое число. Попробуйте еще раз.')
        ask_number_hotels(message.chat.id, date_create)


def ask_number_photo(message: types.Message, date_create: str) -> None:
    """
    Проверяем хочет ли пользователь увидеть фотографии. Есди нет, то переходим к выводу результата.
    если да - то спрашиваем сколько фотографий показать, передаем клавиатуру для упрощения ввода из 6 цифр.
    В обоих случаях записываем в БД кол-во фотограий и нужны ли они.
    Если пользователсь ввел что-то кроме да/нет - возвращаемся в предыдущую функцию
    Переходим к проверке ввода кол-ва фотографий
    :param date_create: Дата ввода команды пользователем
    :param message: ответ на "хотите увидеть фотографии?"
    """

    if message.text.lower() == 'нет':
        history.set_photo(message.chat.id, False, date_create)
        history.set_count_of_photo(message.chat.id, 0, date_create)
        bot.send_message(message.chat.id, 'Обзваниваю отели. Подождите, пожалуйста',
                         reply_markup=types.ReplyKeyboardRemove())
        show_result(message.chat.id, date_create)
    elif message.text.lower() == 'да':
        history.set_photo(message.chat.id, True, date_create)
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                             resize_keyboard=True,
                                             input_field_placeholder='не более 6 фотографий')
        keyboard.row('1', '2', '3')
        keyboard.row('4', '5', '6')
        number_photo: types.Message = bot.reply_to(message, 'Сколько?', reply_markup=keyboard)
        bot.register_next_step_handler(number_photo, check_count_of_photo, date_create)
    else:
        photo_desire: types.Message = bot.reply_to(message, 'Введите "да" или "нет"')
        bot.register_next_step_handler(photo_desire, ask_number_photo, date_create)


def check_count_of_photo(message: types.Message, date_create: str) -> None:
    """
    Проверяем адекватность ввода кол-ва фоторграфий.
    Сложность условия из-за того, что бы не было ситуации, когда пользователь сначала сказал что фотографии нужны, потом
    начал вводить не цифры, его начинает кидать обратно, а потом он вводит "нет". И если условие сделать попроще, то в
    этот момент скрипт посчитает, что ему не нужны фотографии, но первое слово дороже второго.

    Если пользователь ввел число больше разрешенного(файл configs.py), то принудительно меняем его
    :param message: кол-во фотографий
    :param date_create: Дата ввода команды пользователем
    :return:
    """
    count_of_photo: str = message.text

    if (count_of_photo.isdigit() and history.get_photo(message.chat.id, date_create)) or \
            (count_of_photo == 'нет' and not history.get_photo(message.chat.id, date_create)):

        if count_of_photo.isdigit() and int(count_of_photo) > configs.count_of_photo:
            count_of_photo = configs.count_of_photo

        history.set_count_of_photo(message.chat.id, count_of_photo, date_create)
        bot.send_message(message.chat.id, 'Обзваниваю отели. Подождите, пожалуйста',
                         reply_markup=types.ReplyKeyboardRemove())
        show_result(message.chat.id, date_create)
    else:
        number_photo: types.Message = bot.reply_to(message, 'Введите число!')
        bot.register_next_step_handler(number_photo, check_count_of_photo, date_create)


def show_result(id_user: int, date_create: str) -> None:
    """
    Выводить результат из БД пользователю.
    В зависимости от команды, вызываем функцию формирования списка отелей и записи его в БД из полученных ранее данных,
    а потом записываем этот список в переменную из БД
    В выводе к каждому отелю прикрепляем кнопку с ссылкой на бронирование номера
    :param date_create: Дата ввода команды пользователем
    :param id_user: id пользователя
    """
    if history.get_command(id_user, date_create) == 'lowprice':
        lowprice.get_hotels_info(id_user, date_create)
    elif history.get_command(id_user, date_create) == 'highprice':
        highprice.get_hotels_info(id_user, date_create)
    else:
        bestdeal.get_hotels_info(id_user, date_create)

    hotels: List[dict] = history.get_hotels(id_user, date_create)

    for hotel in hotels:

        if history.get_photo(id_user, date_create):
            media_group: List[types.InputMediaPhoto] = history.create_media_group(hotel['photo'])
            bot.send_media_group(id_user, media_group)

        link_booking = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Забронировать номер', url=hotel['booking'])
        link_booking.add(button)

        bot.send_message(id_user, 'Название отеля: {name}\n'
                                  'Адрес: {address}\n'
                                  'Расстояние до центра: {dist}\n'
                                  'Цена: {price}'.format(name=hotel['name'],
                                                         address=hotel['address'],
                                                         dist=hotel['distance_to_center'],
                                                         price=hotel['price']),
                         reply_markup=link_booking)
    bot.send_message(id_user, 'Найдено отелей: {}'.format(len(hotels)))


@bot.message_handler(func=lambda message: True)
def dont_understand(message: types.Message):
    bot.reply_to(message, "Я вас не понимаю, введите /help для помощи")


bot.infinity_polling()
