# GB Python2 lession 7
#
import getopt
import select
import sys
import socket
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

RECV_BUFFER = 4096
socket_list = []


def usage():
    print('Usage: ', sys.argv[0], "-a <addr> -p <port>")
    print("Defaults: addr - ", confJson['addr'])
    print("\t  port - ", confJson['port'])


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


# unicast chat messages to only one connected client
def unicast(socket, message):
    try:
        print(socket)
        socket.send(message.encode('utf-8'))
    except:
        # broken socket connection
        socket.close()
        # broken socket, remove it
        if socket in socket_list:
            socket_list.remove(socket)


# broadcast chat messages to all connected clients
def broadcast(server_socket, sock, message):
    for socket in socket_list:
        # send the message only to peer
        if socket != server_socket and socket != sock:
            try:
                print(socket)
                socket.send(message.encode('utf-8'))
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in socket_list:
                    socket_list.remove(socket)


def server(argv):
    # parse options
    main(argv)

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создает сокет TCP
        server_socket.setblocking(0)
        server_socket.bind((confJson['addr'], confJson['port']))
        server_socket.listen(5)
        server_socket.settimeout(0.2)
    except Exception as ex:
        logger.critical('Server fault: {}'.format(ex))
        print("Server fault: ", ex)
        sys.exit(-1)

    print("Server start: ", confJson['addr'], ':', confJson['port'])
    logger.info("Server start: {} : {}".format(confJson['addr'], confJson['port']))

    # add server socket object to the list of readable connections
    socket_list.append(server_socket)

    while True:
        wait = 0

        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [], wait)

        for sock in ready_to_read:
            # a new connection request recieved
            if sock is server_socket:
                sockfd, addr = server_socket.accept()
                sockfd.setblocking(0)
                socket_list.append(sockfd)
                print("Client (%s, %s) connected" % addr)

                broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)

            # a message from a client, not a new connection
            else:
                # process data recieved from client,
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        process_data(server_socket, sock, data)
                    else:
                        # remove the socket that's broken
                        if sock in socket_list:
                            socket_list.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)

                        # exception
                except:
                    broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    continue

    server_socket.close()


# processed data from client
def process_data(server_socket, sock, data):
    if data:
        dataJson = json.loads(data.decode("utf-8"))
        if 'action' in dataJson and dataJson['action'] == 'presence':
            recvData = {"action": "probe", "time": time.time()}
            msg = json.dumps(recvData)
            print("PR Message send to client: {}".format(msg))
            logger.info("PR Message send to client: {}".format(msg))
            # send probe
            unicast(sock, msg)
        elif 'action' in dataJson and dataJson['action'] == 'msg':
            send_msg = dataJson['message']
            recvData = {"response": 200, "time": time.time(), "alert": "Сообщение доставлено"}
            msg = json.dumps(recvData)
            print("MSG Message send to client: {}".format(msg))
            logger.info("MSG Message send to client: {}".format(msg))
            # send 200
            unicast(sock, msg)
            # send to all
            broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + send_msg)
        else:
            recvData = {"response": 200, "time": time.time(), "alert": "Необязательное сообщение/уведомление"}
            msg = json.dumps(recvData)
            print("Send alert to client: {}".format(msg))
            logger.info("Send alert to client: {}".format(msg))
            # send response
            unicast(sock, msg)
    else:
        if len(data) > 0:
            recvData = {"response": 400, "time": time.time(), "alert": "неправильный запрос/JSON-объект"}
            msg = json.dumps(recvData)
            print("Send alert to client: {}".format(msg))
            logger.info("Send alert to client: {}".format(msg))
            unicast(sock, msg)


if __name__ == '__main__':
    server(sys.argv[1:])
