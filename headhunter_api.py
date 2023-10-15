from abc import ABC, abstractmethod
import requests


class BaseHeadHunter(ABC):
    @abstractmethod
    def set_text(self, text):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def get_vacancy_info(self, vacancies):
        pass


def get_vacancy_url(vacancy_id):
    """Возвращает ссылку на вакансию"""
    return f'https://hh.ru/vacancy/{vacancy_id}'


class HeadHunter_API(BaseHeadHunter):
    """Класс для работы с API HeadHunter"""
    URL = 'https://api.hh.ru/vacancies'

    def __init__(self, text, area, name=None):
        self.name = name
        self.__text = text
        self.__area = area
        self.params = {'text': self.__text,
                       'name': name,
                       'per_page': 100,
                       'area': self.__area}
        self.header = {'User-Agent': 'User'}
        self.vacations_list = []
        self.response = requests.get(HeadHunter_API.URL)
        if not self.response.ok:
            raise Exception('HeadHunterAPI problem')

    def set_text(self, text):
        """Устанавливает text в params"""
        self.__text = text
        self.params['text'] = self.__text

    def set_area(self, area):
        """Устанавливает area в params"""
        self.__area = area
        self.params['area'] = self.__area

    def get_vacancies(self):
        """Функция возвращает вакансии с платформы"""
        self.vacations_list = requests.get(HeadHunter_API.URL, params=self.params, headers=self.header)
        return self.vacations_list.json()['items']

    @staticmethod
    def get_city_name(city_id):
        """Функция возвращает название города, в котором находится вакансия"""
        url = f"https://api.hh.ru/areas/{city_id}"
        response = requests.get(url)
        if response.ok:
            data = response.json()
            return data['name']
        else:
            return "Неизвестная локация"

    def get_vacancy_info(self, vacancies):
        """Получает название вакансии, информацию о зарплате и местоположении"""
        result_list = []
        for vacancy in vacancies:
            name = vacancy['name']
            salary = vacancy['salary']
            area = HeadHunter_API.get_city_name(vacancy['area']['id'])
            url = get_vacancy_url(vacancy['id'])
            if not salary:
                result_list.append(
                    {'name': name, 'link': url, 'salary': 'Зарплата не указана', 'location': area, 'id': url[-8:]})
            elif salary.get('from'):
                result_list.append(
                    {'name': name, 'salary': f"Зарплата от {salary['from']} {salary['currency']}", 'location':
                        area, 'link': url, 'id': url[-8:]})
            elif salary.get('to'):
                result_list.append(
                    {'name': name, 'salary': f"Зарплата до {salary['to']} {salary['currency']}", 'location':
                        area, 'link': url, 'id': url[-8:]})
            elif salary.get('currency'):
                result_list.append(
                    {'name': name, 'salary': f"Зарплата по договорённости в {salary['currency']}", 'location': area,
                     'link': url, 'id': url[-8:]})
            else:
                result_list.append(
                    {'name': name, 'salary': 'Зарплата не указана', 'location': area, 'link': url, 'id': url[-8:]})
        return result_list
