import requests
import json
from decouple import config


RAPIDAPI_KEY = config('RAPIDAPI_KEY')

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': RAPIDAPI_KEY
    }


def get_city_id():
    """
    Спрашиваем город и парсим его ID
    :return: id
    """
    url = "https://hotels4.p.rapidapi.com/locations/search"
    city = input('Where are you going? ')
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
    """
    Выводит в консоль топ 5 дешевых отелей
    :param list_hotels:
    """
    full_list_hotels = list_hotels['data']['body']['searchResults']['results']
    count = 0
    for hotel in full_list_hotels:
        count += 1
        name = hotel['name']
        try:
            adress = hotel['address']['streetAddress']
        except KeyError:
            adress = None
        distance_to_center = hotel['landmarks'][0]['distance']       # возможно не центр, надо делать проверку
        price = hotel['ratePlan']['price']['fullyBundledPricePerStay']
        print('\nName: {name}\nAdress: {adress}\nDistance to center: {distance_to_center}\nPrice: {price}'.format(
            name=name, adress=adress, distance_to_center=distance_to_center, price=price
        ))
        if count == 5:
            break


id = get_city_id()
hotels = get_properties_list(id)
get_hotels_info(hotels)




