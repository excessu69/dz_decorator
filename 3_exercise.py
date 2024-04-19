# Задание №3


import re
from functools import wraps
import requests
import bs4
from fake_headers import Headers
import time
import json
from datetime import datetime

def logger(path):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            start_time = datetime.now()

            result = old_function(*args, **kwargs)

            end_time = datetime.now()
            execution_time = end_time - start_time

            log_entry = f"Function: {old_function.__name__}, Start Time: {start_time}, End Time: {end_time}, Execution Time: {execution_time}\n"

            # Открываем файл для добавления записей (режим 'a') и записываем строку в файл
            with open(path, 'a') as log_file:
                log_file.write(log_entry)

            # Возвращаем результат выполнения оригинальной функции
            return result

        return new_function

    return __logger



def get_headers():
    return Headers(os='win', browser='chrome').generate()

@logger('3_exe.log')  # Применяем декоратор к функции
def get_vacancies():
    response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2',
                            headers=get_headers())
    main_html_data = response.text
    main_soup = bs4.BeautifulSoup(main_html_data, features='lxml')

    tag_div_vacancy_lit = main_soup.find('main', class_='vacancy-serp-content')
    vacancy_tags = tag_div_vacancy_lit.find_all('div', class_='serp-item')

    parsed_data = []

    for vacancy_tag in vacancy_tags:
        h2_tag = vacancy_tag.find('span', class_='serp-item__title-link-wrapper')
        a_tag = h2_tag.find('a')
        absolute_link = a_tag['href']
        title = h2_tag.text

        time.sleep(0.3)
        vacancy_response = requests.get(absolute_link, headers=get_headers())
        vacancy_html_data = vacancy_response.text
        vacancy_soup = bs4.BeautifulSoup(vacancy_html_data, features='lxml')

        description_tag = vacancy_soup.find('div', class_='vacancy-description')
        if description_tag:
            description = description_tag.text.lower()
        else:
            description = ""

        if 'django' in description and 'flask' in description:
            match = re.search(r'(.+?\.)', description)
            if match:
                parsed_data.append({
                    'title': title,
                    'link': absolute_link,
                    'description': match.group()
                })

    with open('vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=4)

    return parsed_data

if __name__ == '__main__':
    get_vacancies()  # Вызываем функцию для получения вакансий
