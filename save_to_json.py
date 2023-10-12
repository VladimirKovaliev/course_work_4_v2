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

class Save_to_json(AbstractSaveToJSON, MixinSave):
    """Класс для работы с вакансиями с JSON"""
    PATH = 'result.json'
    list_to_save = []
    parser_list1 = []
    parser_list2 = []
    instance_list = []

    def add_vacancy(self, vacancy) -> None:
        """Функция для сохранения вакансий в JSON файл"""
        Save_to_json.parser_list1.extend(Save_to_json.parser_list2)
        if os.path.exists('result.json'):
            with open(Save_to_json.PATH, 'r') as file:
                if open(Save_to_json.PATH, 'r').read():
                    saved_vacations = json.loads(file.read())
                    Save_to_json.list_to_save += saved_vacations  # добавляем сохраненные вакансии
        for instance in Save_to_json.parser_list1:
            if 'id' in instance.keys() and int(instance['id'] == int(vacancy.id)):
                if instance not in Save_to_json.list_to_save:  # проверяем, нет ли такой вакансии уже в списке
                    Save_to_json.list_to_save.append(instance)

    def get_vacancies_by_salary(self, salary: int) -> None:
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

    def delete_vacancy(self, vacancy):
        pass