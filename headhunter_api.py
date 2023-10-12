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


class HeadHunter_API(BaseHeadHunter):
    URL = 'https://api.hh.ru/vacancies'

    def __init__(self, text, area):
        self.__text = text
        self.__area = area
        self.params = {'text': self.__text,
                       'per_page': 100,
                       'area': self.__area}
        self.header = {'User-Agent': 'User'}
        self.vacations_list = []
        self.response = requests.get(HeadHunter_API.URL)
        if not self.response.ok:
            raise Exception('HeadHunterAPI problem')

    def set_text(self, text):
        self.__text = text
        self.params['text'] = self.__text
    def set_area(self, area):
        self.__area = area
        self.params['area'] = self.__area

    def get_vacancies(self):
        self.vacations_list = requests.get(HeadHunter_API.URL, params=self.params, headers=self.header)
        return self.vacations_list.json()['items']

    @staticmethod
    def get_city_name(city_id):
        url = f"https://api.hh.ru/areas/{city_id}"
        response = requests.get(url)
        if response.ok:
            data = response.json()
            return data['name']
        else:
            return "Неизвестная локация"

    def get_vacancy_url(self, vacancy_id):
        return f'https://hh.ru/vacancy/{vacancy_id}'


    def get_vacancy_info(self, vacancies):
        '''Получает название вакансии, информацию о зарплате и местоположении'''
        result_list = []
        for vacancy in vacancies:
            name = vacancy['name']
            salary = vacancy['salary']
            area = HeadHunter_API.get_city_name(vacancy['area']['id'])
            url = self.get_vacancy_url(vacancy['id'])
            if not salary:
                result_list.append({'name': name, 'salary': 'Зарплата не указана', 'area': area, 'url': url})
            elif salary.get('from'):
                result_list.append({'name': name, 'salary': f"Зарплата от {salary['from']} {salary['currency']}", 'area': area, 'url': url})
            elif salary.get('to'):
                result_list.append({'name': name, 'salary': f"Зарплата до {salary['to']} {salary['currency']}", 'area': area, 'url': url})
            elif salary.get('currency'):
                result_list.append({'name': name, 'salary': f"Зарплата по договорённости в {salary['currency']}", 'area': area, 'url': url})
            else:
                result_list.append({'name': name, 'salary': 'Зарплата не указана', 'area': area, 'url': url})
        return result_list



hh = HeadHunter_API('Python', 3)
data = hh.get_vacancies()
sorted_vacancies = hh.get_vacancy_info(data)
for vacancy in sorted_vacancies:
    print(f"{vacancy['name']}: {vacancy['salary']} ({vacancy['area']}), URL:{vacancy['url']}")