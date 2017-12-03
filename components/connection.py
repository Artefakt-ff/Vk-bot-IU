from json import loads

import requests

from components.settings import access_token

vk_api = 'https://api.vk.com/method/'
default_parameters = param = {'access_token': access_token, 'v': '5.52'}


def get_message(count=1, time_offset=0):  # Get message
    parameters = default_parameters
    parameters['count'] = count
    parameters['time_offset'] = time_offset
    request = requests.get(vk_api+'messages.get', params=parameters).text
    return loads(request)


def send_message(user_id, message):  # Send a message
    parameters = default_parameters
    parameters['user_id'] = user_id
    parameters['message'] = message
    return requests.get(vk_api+'messages.send', params=parameters).text

