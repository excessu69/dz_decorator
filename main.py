# Задание №1

import os
from datetime import datetime
from functools import wraps


def logger(old_function):

    @wraps(old_function)
    def new_function(*args, **kwargs):

        arg_list = []

        for i, arg in enumerate(args):
            arg_name = old_function.__code__.co_varnames[i]
            arg_list.append(f'{arg_name}={repr(arg)}')

        for key, value in kwargs.items():
            arg_list.append(f'{key}={repr(value)}')

        arg_list_string = ', '.join(arg_list)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = f"{timestamp} - {old_function.__name__}({arg_list_string}): {old_function(*args, **kwargs)}\n"

        with open('main.log', 'a') as log_file:
            log_file.write(log_entry)


        return old_function(*args, **kwargs)


    return new_function



def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
