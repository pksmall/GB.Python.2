# logging - стандартный модуль для организации логирования
import logging
import logging.handlers
import time
from app_config import *

# Можно выполнить более расширенную настройку логирования.
# Создаем объект-логгер с именем app.main:
logger = logging.getLogger('server')

# Создаем объект форматирования:
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")

# Создаем файловый обработчик логирования (можно задать кодировку):
log_file = confJson['logdir'] + "server-{}.log".format(time.strftime("%Y%m%d"))
time_handler = logging.handlers.TimedRotatingFileHandler(log_file, when='d', encoding='utf-8')
time_handler.setLevel(logging.DEBUG)
time_handler.setFormatter(formatter)

# Добавляем в логгер новый обработчик событий и устанавливаем уровень логирования
logger.addHandler(time_handler)
logger.setLevel(logging.DEBUG)


def logwrapper(func_to_deco):
    # Данная "обёртка" принимает любые аргументы
    def logwrapper_with_args(*args, **kwargs):
        print(' запустили из функции ( %s ) ' % func_to_deco)
        logger.info(' запустили из функции ( {} ) '.format(func_to_deco))

        print("Передали ли мне что-нибудь?:")
        logger.info("Передали ли мне что-нибудь?:")

        print(func_to_deco, args, kwargs)
        logger.info(func_to_deco, args, kwargs)
        func_to_deco(*args, **kwargs)
    return logwrapper_with_args()


def set_logging(level):
    # Создаем потоковый обработчик логирования (по умолчанию sys.stderr):
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(formatter)
    logger.addHandler(console)


if __name__ == '__main__':
    logger.info('Тестовый запуск логирования сервера')
