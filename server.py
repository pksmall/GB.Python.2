# GB Python2 lession 3
#
import getopt
import sys
from socket import *
from server_log_config import *

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
    print("\t  port - ", confJson['port'])

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
def server(argv):
    # parse optons
    main(argv)
    print("Server start: ", confJson['addr'], ':', confJson['port'])
    logger.info("Server start: {} : {}".format(confJson['addr'], confJson['port']))

    try:
        s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
        s.bind((confJson['addr'], confJson['port']))
        s.listen(5)
    except Exception as ex:
        logger.critical('Server fault: {}'.format(ex))
        print("Server fault: ", ex)
        sys.exit(-1)

    while True:
        try:
            client, addr = s.accept()
            data = client.recv(1000000)
            if data:
                dataJson = json.loads(data.decode("utf-8"))
                if 'type' in dataJson and dataJson['type'] == 'status':
                    recvData = {"action": "probe", "time": time.time()}
                    msg = json.dumps(recvData)
                    client.send(str(msg).encode("utf-8"))
                    logger.info("Message send to client: {}".format(msg))
                else:
                    recvData = {"response": 200, "alert": "Необязательное сообщение/уведомление"}
                    msg = json.dumps(recvData)
                    client.send(str(msg).encode("utf-8"))
                    logger.info("Send alert to client: {}".format(msg))
            else:
                recvData = {"response": 400, "alert": "неправильный запрос/JSON-объект"}
                msg = json.dumps(recvData)
                client.send(str(msg).encode("utf-8"))
                logger.info("Send alert to client: {}".format(msg))
        except Exception as ex:
            logger.critical('Message: {}'.format(ex))
            print("Server fault: ", ex)
            sys.exit(-1)


if __name__ == '__main__':
    server(sys.argv[1:])
