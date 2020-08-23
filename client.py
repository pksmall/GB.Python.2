# GB Python2 l03
#
import datetime
import json
import sys
import time
from socket import *
import getopt

'''
клиент отправляет запрос серверу;
сервер отвечает соответствующим кодом результата. Клиент и сервер должны быть реализованы в виде отдельных скриптов,
содержащих соответствующие функции. Функции клиента: сформировать presence-сообщение; отправить сообщение серверу;
получить ответ сервера; разобрать сообщение сервера; параметры командной строки скрипта client.py <addr> [<port>]:
addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777. Функции сервера: принимает сообщение клиента;
формирует ответ клиенту; отправляет ответ клиенту; имеет параметры командной строки: -p <port> — TCP-порт для работы
(по умолчанию использует 7777); -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
'''

CONF_FILE = '.config.json'
confJson = None


def load_config():
    global confJson

    with open("./" + CONF_FILE) as f_n:
        f_n_content = f_n.read()
        confJson = json.loads(f_n_content)


def date(unixtime, format = '%Y-%m-%d %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

def usage():
    print('Usage: ', sys.argv[0], "-a <addr> -p <port>")
    print("Defaults: addr - ", confJson['addr'])
    print("\t\t  port - ", confJson['port'])


def main(argv):
    global addr, port

    try:
        opts, args = getopt.getopt(argv, "ha:p:v", ["help", "address=", "port="])
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-a", "--address"):
            confJson['addr'] = a
        elif o in ("-p", "--port"):
            confJson['port'] = a


if __name__ == '__main__':
    load_config()
    main(sys.argv[1:])
    try:
        s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
        s.connect((confJson['addr'], confJson['port']))   # Соединиться с сервером

        recvData = {"action": "presence", "time": time.time(), "type": "status",
                    "user": {"account_name":  "C0deMaver1ck", "status":"Yep, I am here!"}}
        msg = json.dumps(recvData)
        s.send(str(msg).encode("utf-8"))
        data = s.recv(1000000)
        dataJson = json.loads(data.decode("utf-8"))
        if dataJson:
            if 'action' in dataJson and dataJson['action'] == 'probe':
                print('Действие сервера: ', dataJson['action'], ', Время: ', date(dataJson['time']),
                      ', Длина сообщения: ', len(data), ' байт')
            elif 'response' in dataJson:
                print('Сервер прислал: ', dataJson['response'], ', Сообщение: ', dataJson['alert'],
                      ', Длина сообщения: ', len(data), ' байт')
    except Exception as ex:
        print('Connection Message:', ex)
        usage()