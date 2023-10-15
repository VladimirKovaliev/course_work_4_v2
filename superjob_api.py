import requests
from abc import ABC


class BaseHeadHunter(ABC):
    def get_vacancies(self):
        pass


def get_vacancy_info(vacancies):
    """Функция для сбора информации о вакансии"""
    result_list = []
    for vacancy in vacancies:
        name = vacancy['profession']
        vacancy_id = vacancy['id']
        vacancy_link = vacancy['link']
        payment_from = vacancy['payment_from']  # от
        payment_to = vacancy['payment_to']  # до
        vacancy_location = vacancy['town']['title']
        experience = vacancy['experience']['title']
        if payment_from != 0 and payment_to != 0:
            result_list.append({'name': name, 'id': vacancy_id,
                                'salary': f'Зарплата от {payment_from} RUB до {payment_to} RUB',
                                'location': vacancy_location, 'experience': experience, 'link': vacancy_link})
        elif payment_from != 0 and payment_to == 0:
            result_list.append({'name': name, 'id': vacancy_id,
                                'salary': f'Зарплата от {payment_from} RUB',
                                'location': vacancy_location, 'experience': experience, 'link': vacancy_link})
        elif payment_from == 0 and payment_to != 0:
            result_list.append({'name': name, 'id': vacancy_id,
                                'salary': f'Зарплата до {payment_to} RUB',
                                'location': vacancy_location, 'experience': experience, 'link': vacancy_link})
        elif payment_from == 0 and payment_to == 0:
            result_list.append({'name': name, 'id': vacancy_id,
                                'salary': f'Зарплата не указана',
                                'location': vacancy_location, 'experience': experience, 'link': vacancy_link})
        else:
            result_list.append({'name': name, 'id': vacancy_id,
                                'salary': f'Зарплата по договоренности',
                                'location': vacancy_location, 'experience': experience, 'link': vacancy_link})
    return result_list


class SuperJobAPI(BaseHeadHunter):
    """Класс для работы с АПИ hh.ru"""
    URL = 'https://api.superjob.ru/2.0/vacancies/'
    SECRET_KEY = 'v3.r.129594070.86ce97965df4aa99171a8b221330abf05a2b9f99.e7e10463137c9ac551eefa17ef14d0b27d536dcc'

    def __init__(self, text):
        self.__text = text
        self.params = {
            'keyword': self.__text,
        }
        self.header = {"X-Api-App-Id": SuperJobAPI.SECRET_KEY}
        self.vacations_list = []
        self.response = requests.get(SuperJobAPI.URL, headers=self.header)
        if not self.response.ok:
            raise Exception('SuperJobAPI problem')

    @property
    def text(self):
        return self.__text

    def get_vacancies(self):
        """Функция, которая берет вакансии с платформы"""
        self.vacations_list = requests.get(SuperJobAPI.URL, headers=self.header, params=self.params)
        return self.vacations_list.json()['objects']
