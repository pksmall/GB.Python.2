# GB Python2 l03
#
import sys
import getopt
from socket import *
from client_log_config import *

'''
клиент отправляет запрос серверу;
сервер отвечает соответствующим кодом результата. Клиент и сервер должны быть реализованы в виде отдельных скриптов,
содержащих соответствующие функции. Функции клиента: сформировать presence-сообщение; отправить сообщение серверу;
получить ответ сервера; разобрать сообщение сервера; параметры командной строки скрипта client.py <addr> [<port>]:
addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777. Функции сервера: принимает сообщение клиента;
формирует ответ клиенту; отправляет ответ клиенту; имеет параметры командной строки: -p <port> — TCP-порт для работы
(по умолчанию использует 7777); -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
'''

@logwrapper
def usage():
    print('Usage: ', sys.argv[0], "-a <addr> -p <port>")
    print("Defaults: addr - ", confJson['addr'])
    print("\t\t  port - ", confJson['port'])


@logwrapper
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

@logwrapper
def client(argv):
    # parse options
    main(argv)
    logger.info("Client start.")

    try:
        s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
        s.connect((confJson['addr'], confJson['port']))   # Соединиться с сервером

        recv_data = {"action": "presence", "time": time.time(), "type": "status",
                    "user": {"account_name":  "C0deMaver1ck", "status":"Yep, I am here!"}}
        msg = json.dumps(recv_data)
        s.send(str(msg).encode("utf-8"))
        data = s.recv(1000000)
        data_json = json.loads(data.decode("utf-8"))
        if data_json:
            if 'action' in data_json and data_json['action'] == 'probe':
                print('Действие сервера: ', data_json['action'], ', Время: ', date(data_json['time']),
                      ', Длина сообщения: ', len(data), ' байт')
                logger.info('Действие сервера: {}, Время: {} Длина сообщения: {} байт'
                             .format(data_json['action'], date(data_json['time']), len(data)))
            elif 'response' in data_json:
                print('Сервер прислал: ', data_json['response'], ', Сообщение: ', data_json['alert'],
                      ', Длина сообщения: ', len(data), ' байт')
                logger.info('Сервер прислал: {}, Сообщение: {}, Длина сообщения: {} байт'
                             .format(data_json['response'], data_json['alert'], len(data)))
    except Exception as ex:
        logger.critical('Message: {}'.format(ex))
        print('Connection Message:', ex)
        usage()


if __name__ == '__main__':
    client(sys.argv[1:])
