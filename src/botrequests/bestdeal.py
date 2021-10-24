import requests
import json
from decouple import config
from typing import List


RAPIDAPI_KEY = config('RAPIDAPI_KEY')

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': RAPIDAPI_KEY
    }


def get_city_id(city):
    """
    Возвращает ID требуемого города
    :return: id
    """
    url = "https://hotels4.p.rapidapi.com/locations/search"
    querystring = {"query": city, "locale": "ru_RU"}
    response_city_id = requests.request("GET", url, headers=headers, params=querystring)
    data_city_id = json.loads(response_city_id.text)
    city_id = data_city_id['suggestions'][0]['entities'][0]['destinationId']
    return city_id


def get_properties_list(city: str, price_min: str, price_max: str, upp_board: str) -> List[dict]:
    """
    Парсим API для по городу, границам цен.
    В зависимости от верхней границы расстаяния от центра парсим с разными характеристиками сортировки (если очень
    близко к центру - сортируем по расстоянию от центра (пользователю важнее приближенность к центру чем деньги),
    если далеко от центра (пользователю важнее сэкономить) - сортируем по цене)
    :param upp_board: верхняя граница расстояния от центра
    :param price_max: максимальная цена
    :param price_min: минимальная цена
    :param city: город
    :return: лист отелей
    """

    url = "https://hotels4.p.rapidapi.com/properties/list"
    if float(upp_board) <= 2.5:
        querystring = {"destinationId": get_city_id(city), "pageNumber": "1", "pageSize": "25", "checkIn": "2021-10-25",
                       "checkOut": "2021-10-26", "adults1": "1", "priceMin": price_min, "priceMax": price_max,
                       "sortOrder": "DISTANCE_FROM_LANDMARK", "locale": "ru_RU", "currency": "RUB"}
    else:
        querystring = {"destinationId": get_city_id(city), "pageNumber": "1", "pageSize": "25", "checkIn": "2021-10-25",
                       "checkOut": "2021-10-26", "adults1": "1", "priceMin": price_min, "priceMax": price_max,
                       "sortOrder": "PRICE", "locale": "ru_RU", "currency": "RUB"}
    response_properties_list = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response_properties_list.text)
    data = data['data']['body']['searchResults']['results']
    return data


def string_to_number(string: str) -> [int, float]:
    """
    Вытаскивает из строки число, меняет запятую на точку

    :param string: строка состоящая из цифр и букв
    """
    number = ''
    for sym in string:
        if sym == ',':
            number += '.'
        elif sym == ' ':
            break
        else:
            number += sym
    if '.' in number:
        return float(number)
    return int(number)


def get_hotels_info(list_hotels: List[dict], number: int, lower_bond: str, upp_board: str) -> List[dict]:
    """
    Сортируем список по цене (сначала дешевые)
    Потом в цикле проверяем каждый отель на соответствие запрошенного расстояния от центра города.
    Далее берем необходимые значения из list_hotels, потом присваиваем их новому словарю. На каждой итерации
    цикла мы добавляем созданный словарь в список top
    :param list_hotels: лист отелей
    :param number: кол-во отелей
    :param lower_bond: нижняя граница по расстоянию
    :param upp_board: верхняя граница по расстоянию
    :return: список словарей отелей с необходимыми характеристиками
    """
    sorted_list_hotels = sorted(list_hotels, key=lambda x: int(x['ratePlan']['price']['exactCurrent']))
    count = 0
    top = []
    for hotel in sorted_list_hotels:
        if string_to_number(lower_bond) <= string_to_number(hotel['landmarks'][0]['distance']) <= string_to_number(upp_board):
            hotel_info = dict()
            count += 1
            name = hotel['name']
            try:
                address = hotel['address']['streetAddress']
            except KeyError:
                address = None
            distance_to_center = hotel['landmarks'][0]['distance']
            price = hotel['ratePlan']['price']['current']
            hotel_info['name'] = name
            hotel_info['addres'] = address
            hotel_info['distance_to_center'] = distance_to_center
            hotel_info['price'] = price
            top.append(hotel_info)
        if count == number:
            break
    return top






