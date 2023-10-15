from abc import ABC, abstractmethod
import json
import os


class AbstractSaveToJSON(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class MixinSave:
    @staticmethod
    def save_to_file() -> None:
        """Функция для сохранения в файл"""
        with open(Save_to_json.PATH, 'w') as file:
            json.dump(Save_to_json.list_to_save, fp=file)


def get_vacancies_by_salary(salary: int) -> None:
    """Функция для просмотра сохраненных вакансий из JSON файла"""
    salary = salary if salary else 0
    try:
        with open(Save_to_json.PATH, 'r') as file:
            saved_vacations = json.loads(file.read())
    except FileNotFoundError:
        raise FileNotFoundError('Файла result.json не существует')

    for vacation in saved_vacations:
        for instance in Save_to_json.instance_list:
            if vacation['id'] == instance.id and instance.payment > int(salary):
                print('*' * 100)
                print(instance, sep='\n')


class Save_to_json(AbstractSaveToJSON, MixinSave):
    """Класс для работы с вакансиями с jSOB"""
    PATH = 'result.json'
    list_to_save = []
    parser_list1 = []
    parser_list2 = []
    instance_list = []

    def add_vacancy(self, vacancies) -> None:
        """Функция для сохранения вакансий в JSON файл"""
        Save_to_json.parser_list1.extend(Save_to_json.parser_list2)
        if os.path.exists('result.json'):
            with open(Save_to_json.PATH, 'r') as file:
                if open(Save_to_json.PATH, 'r').read():
                    saved_vacations = json.loads(file.read())
                    Save_to_json.list_to_save += saved_vacations
        Save_to_json.list_to_save += vacancies  # добавление списка вакансий

    def delete_vacancy(self, vacancy_id: int) -> None:
        """ Функция для удаления вакансий из списка по id """
        try:
            with open(Save_to_json.PATH, 'r') as file:
                saved_vacation_list = json.loads(file.read())
        except FileNotFoundError:
            raise FileNotFoundError("нет файла JSONSaver.PATH = 'result.json'")
        for vacation in saved_vacation_list:
            if int(vacation['id']) == int(vacancy_id):
                del saved_vacation_list[saved_vacation_list.index(vacation)]
                print('Вакансия удалена')
                break
        else:
            print('Нет вакансии с таким id')
        with open(Save_to_json.PATH, 'w') as file:
            json.dump(saved_vacation_list, fp=file)
