from socket import *
from client_log_config import *

ADDRESS = (confJson['addr'], confJson['port'])


def server_action(data_json, data):
    if data_json:
        if 'action' in data_json:
            print('Действие сервера: ', data_json['action'], ', Время: ', date(data_json['time']),
                  ', Длина сообщения: ', len(data), ' байт')
        elif 'response' in data_json:
            print('Сервер прислал: ', data_json['response'], ', Сообщение: ', data_json['alert'],
                  ', Длина сообщения: ', len(data), ' байт')


def echo_client():
    # Начиная с Python 3.2 сокеты имеют протокол менеджера контекста
    # При выходе из оператора with сокет будет автоматически закрыт
    with socket(AF_INET, SOCK_STREAM) as sock:  # Создать сокет TCP
        sock.connect(ADDRESS)  # Соединиться с сервером

        recv_data = {"action": "presence", "time": time.time(), "type": "status",
                     "user": {"account_name":  "maverick", "status": "Yep, I am here!"}}
        msg = json.dumps(recv_data)
        sock.send(msg.encode('utf-8'))  # Отправить!
        data = sock.recv(10000000)
        data_json = json.loads(data.decode("utf-8"))
        server_action(data_json, data)

        while True:
            msg = input('Ваше сообщение: ')
            if msg == 'exit':
                break
            recv_data = {"action": "msg",
                         "time": time.time(),
                         "to": "#all",
                         "from": "maverick",
                         "encoding": "utf-8",
                         "message": "message"}
            msg = json.dumps(recv_data)
            sock.send(msg.encode('utf-8'))  # Отправить!
            data = sock.recv(1024).decode('utf-8')
            data_json = json.loads(data)
            if data_json:
                server_action(data_json, data)


if __name__ == '__main__':
    echo_client()
