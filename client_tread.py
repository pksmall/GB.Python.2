# GB Python2 l03
#
import select
import sys
import getopt
import threading
from socket import socket, AF_INET, SOCK_STREAM
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


def usage():
    print('Usage: ', sys.argv[0], "-a <addr> -p <port>")
    print("Defaults: addr - ", confJson['addr'])
    print("\t\t  port - ", confJson['port'])


def server_action(data_json, data):
    if data_json:
        if 'action' in data_json:
            print('Действие сервера: ', data_json['action'], ', Время: ', date(data_json['time']),
                  ', Длина сообщения: ', len(data), ' байт')
        elif 'response' in data_json:
            print('Сервер прислал: ', data_json['response'], ', Сообщение: ', data_json['alert'],
                  ', Длина сообщения: ', len(data), ' байт')


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


def client(argv):
    # parse options
    main(argv)
    logger.info("Client start.")

    s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
    s.settimeout(2)

    try:
        s.connect((confJson['addr'], confJson['port']))   # Соединиться с сервером
    except Exception as ex:
        logger.critical('Message: {}'.format(ex))
        print('Connection Message:', ex)
        usage()

    recv_data = {"action": "presence", "time": time.time(), "type": "status",
                "user": {"account_name":  "C0deMaver1ck", "status": "Yep, I am here!"}}
    msg = json.dumps(recv_data)
    s.send(str(msg).encode("utf-8"))

    print('Connected to remote host. You can start sending messages')
    exit_flag = False

    def client_send():
        while True:
            msg = input("Text: ")
            if msg == 'exit':
                exit_flag = True
                break
            recv_data = {"action": "msg",
                         "time": time.time(),
                         "to": "#all",
                         "from": "maverick",
                         "encoding": "utf-8",
                         "message": msg}
            recv_msg = json.dumps(recv_data)
            s.send(str(recv_msg).encode("utf-8"))

    def client_recv():
        while True:
            try:
                data = s.recv(4096).decode('utf-8')
                # print data
                data_json = json.loads(data)
                if data_json:
                    server_action(data_json, data)
            except:
                print(data)

    thread_send = []
    thread_rcv = []
    num_threads = 10

    for loop_1 in range(num_threads):
        thread_send.append(threading.Thread(target=client_send))
        thread_send[-1].start()

    for loop_2 in range(num_threads):
        thread_rcv.append(threading.Thread(target=client_recv))
        thread_rcv[-1].start()


if __name__ == '__main__':
    client(sys.argv[1:])
