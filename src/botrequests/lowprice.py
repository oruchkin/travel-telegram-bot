from telebot import types
import requests
import json
from decouple import config
from typing import List, Optional
from datetime import date, timedelta
from src.botrequests import history
import re
RAPIDAPI_KEY = config('RAPIDAPI_KEY')

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': RAPIDAPI_KEY
}


def delete_span(string: str):
    pattern_1 = r"<span class='highlighted'>"
    pattern_2 = r"</span>"
    repl = ''
    res_1 = re.sub(pattern_1, repl, string)
    res_2 = re.sub(pattern_2, repl, res_1)
    return res_2


def check_city(city: str):
    """
    Делаем запрос и проверяем, все результаты ([имя города, id Города]) с type: 'CITY' записываем в список list_cities
    :param city:
    :return: List[str]
    """
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city, "locale": "ru_RU", "currency": "RUB"}
    response_city_id: json = requests.request("GET", url, headers=headers, params=querystring)
    data: json = json.loads(response_city_id.text)
    entities = data['suggestions'][0]['entities']
    list_cities = []
    for entity in entities:
        if entity['type'] == 'CITY':
            full_name = delete_span(entity['caption'])
            list_cities.append([full_name, entity['destinationId']])
    return list_cities


def get_city_id(city: str) -> str:
    """
    Делаем запрос к API и определяем ID требуемого города

    :param city: город, который запросил пользователь
    :return: id города
    """

    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city, "locale": "ru_RU", "currency": "RUB"}
    response_city_id: json = requests.request("GET", url, headers=headers, params=querystring)
    data_city_id: json = json.loads(response_city_id.text)
    city_id: str = data_city_id['suggestions'][0]['entities'][0]['destinationId']
    return city_id


def get_properties_list(id_city: str) -> List[dict]:
    """
    Функция возвращающая список отелей, отсортированным по цене (сначала самые дешевые)
    Внутри querystring у нас функция get_city_id, она принимает город и возвращает ID этого города (строка из цифр)

    :param city: город, в котором будем искать отели
    :return:  список отелей, в котором хранится информация о каждом отеле
    """
    today = date.today()
    check_in = str(today + timedelta(days=2))
    check_out = str(today + timedelta(days=3))
    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": id_city, "pageNumber": "1", "pageSize": "25", "checkIn": check_in,
                   "checkOut": check_out, "adults1": "1", "sortOrder": "PRICE", "locale": "ru_RU", "currency": "RUB"}

    response_properties_list: json = requests.request("GET", url, headers=headers, params=querystring)
    data: json = json.loads(response_properties_list.text)
    full_list_hotels: List[dict] = data['data']['body']['searchResults']['results']

    return full_list_hotels


def get_photo(id_hotel: str, number: str) -> json:
    """
    Получаем адрес фотографии по ID отеля
    :param number: количество фотографий отеля
    :param id_hotel: id Отеля
    :return: адрес фотографии
    """
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": id_hotel}
    response_photo: json = requests.request("GET", url, headers=headers, params=querystring)
    data: json = json.loads(response_photo.text)
    list_photo = []
    for photo in range(int(number)):
        adrress_photo = data['hotelImages'][photo]['baseUrl']
        adrress_photo = adrress_photo.replace('{size}', 'b')
        list_photo.append(types.InputMediaPhoto(adrress_photo))
    return list_photo


def get_hotels_info(id_user, date_create) -> List[dict]:
    """
    Финальная функция. Создает список словарей, которые включают в себя информацию, которую будем выводить пользователю
    по каждому отелю. Число отелей определает пользователь.
    В функции get_properties_list мы берем список 25 отелей и присваиваем его list_hotels
    Сначала мы вы берем необходимые значения из list_hotels, потом присваиваем их новому словарю. На каждой итерации
    цикла мы добавляем созданный словарь в список top

    :param user:
    :return:  список из number словарей, в каждом словаре информация по одному отелю
    """
    count = 0
    top = []
    list_hotels = get_properties_list(history.get_id_city_user(id_user, date_create))
    for hotel in list_hotels:
        hotel_info = dict()
        count += 1
        name: str = hotel['name']
        id_hotel = str(hotel['id'])
        booking = ''.join(['https://ru.hotels.com/ho', id_hotel])
        try:
            address: Optional[str] = hotel['address']['streetAddress']
        except KeyError:
            address: Optional[str] = None
        distance_to_center: str = hotel['landmarks'][0]['distance']
        price: str = hotel['ratePlan']['price']['current']
        hotel_info['name']: str = name
        hotel_info['addres']: str = address
        hotel_info['distance_to_center']: str = distance_to_center
        hotel_info['price']: str = price
        hotel_info['booking']: str = booking
        if history.get_count_of_photo(id_user, date_create):
            hotel_info['photo']: List[str] = get_photo(hotel['id'], history.get_count_of_photo(id_user, date_create))
        top.append(hotel_info)
        if count == history.get_count_of_hotels(id_user, date_create):
            break
    return top


# a = get_properties_list('москва')
# b = get_hotels_info(a, 5, photo=True)
# print(b)
# for i in range(5):
#     print('Название отеля: {name}\n'
#                                            'Адрес: {address}\n'
#                                            'Расстояние до центра: {dist}\n'
#                                            'Цена: {price}'.format(name=b[i]['name'],
#                                                                   address=b[i]['addres'],
#                                                                   dist=b[i]['distance_to_center'],
#                                                                   price=b[i]['price']))

# def get_hotels_info(list_hotels):
#     """
#     Выводит в консоль топ 5 дешевых отелей
#     :param list_hotels:
#     """
#     full_list_hotels = list_hotels['data']['body']['searchResults']['results']
#     count = 0
#     for hotel in full_list_hotels:
#         count += 1
#         name = hotel['name']
#         try:
#             adress = hotel['address']['streetAddress']
#         except KeyError:
#             adress = None
#         distance_to_center = hotel['landmarks'][0]['distance']       # возможно не центр, надо делать проверку
#         price = hotel['ratePlan']['price']['fullyBundledPricePerStay']
#         print('\nName: {name}\nAdress: {adress}\nDistance to center: {distance_to_center}\nPrice: {price}'.format(
#             name=name, adress=adress, distance_to_center=distance_to_center, price=price
#         ))
#         if count == 5:
#             break
#
#
# id = get_city_id('москва')
# hotels = get_properties_list(id)
# get_hotels_info(hotels)
