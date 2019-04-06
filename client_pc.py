import requests
import json
import datetime


def registration(login, password):
    if len(login) > 5 and len(password) > 5:
        message_to_server = {'login':login, 'password':password}
        command = requests.post('http://BOBAH.pythonanywhere.com/registration', json=message_to_server)
        return command.text

    return 'недостаточная длинна логина или пароля'


def login(login, password):
    message_to_server = {'login':login, 'password':password}
    command = requests.post('http://BOBAH.pythonanywhere.com/login', json=message_to_server)
    if len(command.text) == 5:
        return command.text
    else:
        return False


def message_send(from_id, to_id, message):
    message_to_server = {'from_id': from_id, 'to_id': to_id, 'message':message,
                         'datetime':str(datetime.datetime.today().timestamp())}
    command = requests.post('https://BOBAH.pythonanywhere.com/send_message', json=message_to_server)
    return command.text


def message_request(id):
    message_to_server = {'id': id}
    command = requests.post('https://bobah.pythonanywhere.com/request_message', json=message_to_server)
    answer = json.loads(command.text)
    return answer


def id_request(id):
    message_to_server = {'id': id}
    command = requests.post('https://bobah.pythonanywhere.com/request_id', json=message_to_server)
    return command.text
