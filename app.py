import subprocess
import platform
import locale


def subproc(site):
    if platform.system == 'Windows':
        args = ['ping', '-n 1', site]
    else:
        args = ['ping', '-c 1', site]

    subprocess_ping = subprocess.Popen(args, stdout=subprocess.PIPE)

    for line in subprocess_ping.stdout:
        line = line.decode('cp866').encode('utf-8')
        print(line.decode('utf-8'))

### 1
str_1 = "разработка"
str_2 = "сокет"
str_3 = "декоратор"
str_u_1 = "\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430"
str_u_2 = "\u0441\u043e\u043a\u0435\u0442"
str_u_3 = "\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440"
print(type(str_1))
print(type(str_2))
print(type(str_3))
print(type(str_u_1))
print(type(str_u_2))
print(type(str_u_3))

### 2
str_1 = b"class"
str_2 = b"function"
str_3 = b"method"
print(type(str_1))
print(type(str_2))
print(type(str_3))
print(len(str_1))
print(len(str_2))
print(len(str_3))

### 3 закоменченные нельзя записать в байтовом ввиде
### str_1 = b"attribute»"
### str_2 = b"класс"
### str_3 = b"функция"
str_4 = b"type"

### 4
str_1 = "разработка"
str_2 = "администрирование"
str_3 = "protocol"
str_4 = "standard"
str_1 = str_1.encode('utf-8')
print(str_1)
print(str_1.decode('utf-8'))
str_2 = str_2.encode('utf-8')
print(str_2)
print(str_2.decode('utf-8'))
str_3 = str_3.encode('utf-8')
print(str_3)
print(str_3.decode('utf-8'))
str_4 = str_4.encode('utf-8')
print(str_4)
print(str_4.decode('utf-8'))

### 5
subproc('yandex.ru')
subproc('youtube.com')

### 6
str_1 = "сетевое программирование"
str_2 = "сокет"
str_3 = "декоратор"
fileName = "test_file.txt"

file = open(fileName, "w")
file.write(str_1 + " ")
file.write(str_2 + " ")
file.write(str_3 + "\n")
file.close()

def_coding = locale.getpreferredencoding()
print(def_coding)

with open(fileName) as file:
   for strLine in file:
       print(strLine)
