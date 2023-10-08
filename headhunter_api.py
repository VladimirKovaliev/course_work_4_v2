import requests
import json

class HeadHunter_API():
    URL = 'https://api.hh.ru/vacancies'

    def __init__(self, text):
        self.__text = text
        self.params = {'text': self.__text,
                       'per_page': 100,
                       'area': 1}
        self.header = {'User-Agent': 'User'}
        self.vacations_list = []
        self.response = requests.get(HeadHunter_API.URL)
        if not self.response.ok:
            raise Exception('HeadHunterAPI problem')

    def set_text(self, text):
        self.__text = text
        self.params['text'] = self.__text

    def get_vacancies(self):
        self.vacations_list = requests.get(HeadHunter_API.URL, params=self.params, headers=self.header)
        return self.vacations_list.json()['items']

    def get_vacancy_info(self, vacancies):
        '''Получает название вакансии и информацию о зарплате'''
        result_list = []
        for vacancy in vacancies:
            name = vacancy['name']
            salary = vacancy['salary']
            if not salary:
                result_list.append({'name': name, 'salary': 'Зарплата не указана'})
            elif salary.get('from'):
                result_list.append({'name': name, 'salary': f"Зарплата от {salary['from']} {salary['currency']}"})
            elif salary.get('to'):
                result_list.append({'name': name, 'salary': f"Зарплата до {salary['to']} {salary['currency']}"})
            elif salary.get('currency'):
                result_list.append({'name': name, 'salary': f"Зарплата по договорённости в {salary['currency']}"})
            else:
                result_list.append({'name': name, 'salary': 'Зарплата не указана'})
        return result_list


# создание объекта класса, указываем текст запроса
hh = HeadHunter_API('Уборщица')
data = hh.get_vacancies()
sorted_vacancies = hh.get_vacancy_info(data)
for vacancy in sorted_vacancies:
    print(f"{vacancy['name']}: {vacancy['salary']}")  # НУЖНО ДОБАВИТЬ В КЛАСС АБСТРАТНЫЙ МЕТОД