import telebot
from decouple import config
import requests
import json

RAPIDAPI_KEY = config('RAPIDAPI_KEY')
BOT_TOKEN = config('TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': RAPIDAPI_KEY
}


def get_city_id(city):
    """
    Спрашиваем город и парсим его ID
    :return: id
    """
    url = "https://hotels4.p.rapidapi.com/locations/search"
    querystring = {"query": city, "locale": "en_US"}
    response_city_id = requests.request("GET", url, headers=headers, params=querystring)
    data_city_id = json.loads(response_city_id.text)
    city_id = data_city_id['suggestions'][0]['entities'][0]['destinationId']
    return city_id


def get_properties_list(city_id):
    """
    Вовращает десериализованый файл со списком отелей
    :param city_id:
    :return: properties list
    """
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": city_id, "pageNumber": "1", "pageSize": "25", "checkIn": "2021-10-23",
                   "checkOut": "2021-10-24", "adults1": "1", "sortOrder": "PRICE", "locale": "en_US", "currency": "USD"}
    response_properties_list = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response_properties_list.text)
    return data


def get_hotels_info(list_hotels):
    full_list_hotels = list_hotels['data']['body']['searchResults']['results']
    count = 0
    top_5 = []
    for hotel in full_list_hotels:
        hotel_info = dict()
        count += 1
        name = hotel['name']
        try:
            adress = hotel['address']['streetAddress']
        except KeyError:
            adress = None
        distance_to_center = hotel['landmarks'][0]['distance']  # возможно не центр, надо делать проверку
        price = hotel['ratePlan']['price']['fullyBundledPricePerStay']
        hotel_info['name'] = name
        hotel_info['addres'] = adress
        hotel_info['distance_to_center'] = distance_to_center
        hotel_info['price'] = price
        top_5.append(hotel_info)
        # print('\nName: {name}\nAdress: {adress}\nDistance to center: {distance_to_center}\nPrice: {price}'.format(
        #     name=name, adress=adress, distance_to_center=distance_to_center, price=price
        # ))
        if count == 5:
            break
    return top_5


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, where are you going?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    city = message.text
    city_id = get_city_id(city)
    hotels = get_properties_list(city_id)
    hotels = get_hotels_info(hotels)
    for i in range(5):
        bot.send_message(message.from_user.id, 'Name: {name}\nAddress: {address}\nDistance_to_center: {dist}\n'
                                               'Price: {price}'.format(name=hotels[i]['name'],
                                                                       address=hotels[i]['addres'],
                                                                       dist=hotels[i]['distance_to_center'],
                                                                       price=hotels[i]['price']))


bot.infinity_polling()
