import json
from headhunter_api import HeadHunter_API
from superjob_api import SuperJobAPI
from save_to_json import Save_to_json
from utils import filter_by_salary, print_vacancies, get_top_vacancies
import time


def interacion_with_user():
    while True:

        set_platform = input('На какой платформе искать вакансии?\n'
                             '1 - для HeadHunter\n'
                             '2 - для SuperJob\n'
                             '3 - оба варианта\n'
                             '4 - завершить работу\n')
        if set_platform == '4':
            return 'Завершаю работу'
        elif set_platform not in ['1', '2', '3', '4']:
            return 'Неизвестный ввод, завершаю работу'
        vacancy = input(f'Какую вакансию вы хотите найти? ')
        user_choice = input('Добавить фильтр для поиска?\n'
                            '1 - да \n'
                            '2 - нет \n')
        if user_choice == '1':
            user_filter = input('По какому фильтру подбирать вакансии? ')
        print('Идет поиск, подождите', end=' ')
        for _ in range(3):
            time.sleep(0.2)
            print('.', end='', flush=True)
        print()

        if set_platform == '1':
            '''Поиск вакансий на HH'''

            if user_choice == '1':
                hh = HeadHunter_API(vacancy, 1, user_filter)
            else:
                hh = HeadHunter_API(vacancy, 1)

            data = hh.get_vacancies()
            sorted_vacancies = hh.get_vacancy_info(data)
            # json_func = Save_to_json()
            # json_func.add_vacancy(sorted_vacancies)
            # json_func.save_to_file()
            for vacancy in sorted_vacancies:
                print(
                    f"ID:{vacancy['id']} {vacancy['name']}: {vacancy['salary']} "
                    f"({vacancy['location']}), URL:{vacancy['link']}")

        elif set_platform == '2':
            '''Поиск вакансий на SJ'''
            sj = SuperJobAPI(vacancy)
            data = sj.get_vacancies()
            sorted_vacancies = sj.get_vacancy_info(data)
            for vacancy in sorted_vacancies:
                print(f'{vacancy["name"]}, '
                      f'{vacancy["salary"]},'
                      f' ID вакансии : {vacancy["id"]}, '
                      f'({vacancy["location"]}) '
                      f'Опыт работы: {vacancy["experience"]} '
                      f'URL: {vacancy["link"]}')

        elif set_platform == '3':
            if user_choice == '1':
                hh = HeadHunter_API(vacancy, 1, user_filter)
            else:
                hh = HeadHunter_API(vacancy, 1)
            sj = SuperJobAPI(vacancy)
            hh_data = hh.get_vacancies()
            sj_data = sj.get_vacancies()
            hh_sorted_vacancies = hh.get_vacancy_info(hh_data)
            sj_sorted_vacancies = sj.get_vacancy_info(sj_data)
            print('Вакансии из HH:')
            for vacancy in hh_sorted_vacancies:
                print(
                    f"ID: {vacancy['id']},"
                    f" {vacancy['name']},"
                    f" {vacancy['salary']}"
                    f" ({vacancy['location']}), URL:{vacancy['link']}")
            print('Вакансии из SuperJob')
            for vacancy in sj_sorted_vacancies:
                print(f'ID: {vacancy["id"]},'
                      f' {vacancy["name"]}:,'
                      f' {vacancy["salary"]},'
                      f' ({vacancy["location"]})'
                      f' Опыт работы: {vacancy["experience"]}'
                      f' URL: {vacancy["link"]}')

        elif set_platform == '4':
            return 'Завершаю работу'

        else:
            return 'Неизвестный ввод'
        while True:
            user_choice = input('Сохранить результат в JSON файл?\n'
                                '1 - да\n'
                                '2 - нет\n'
                                '3 - Зачем это нужно?\n'
                                '4 - Завершить работу\n')
            if user_choice == '1':
                try:
                    json_func = Save_to_json()
                    json_func.add_vacancy(sorted_vacancies)
                    json_func.save_to_file()
                    print('Данные сохранены.')
                    break
                except UnboundLocalError:
                    json_func = Save_to_json()
                    json_func.add_vacancy(hh_sorted_vacancies)
                    json_func.add_vacancy(sj_sorted_vacancies)
                    json_func.save_to_file()
                    print('Данные с платформ SJ и HH сохранены')
                    break
            elif user_choice == '2':
                break
            elif user_choice == '3':
                print('Это нужно для того, чтобы вы потом могли вывести, добавить, удалить или отсортировать вакансии')
                print()
            elif user_choice == '4':
                break
            else:
                print('Неверный выбор. Попробуйте снова.')
        user_choice = input('Продолжить работу?\n'
                            '1 - Да\n'
                            '2 - Завершить работу\n')
        if user_choice == '1':
            continue
        return 'Завершаю работу'


def user_interaction_with_json():
    while True:
        user_choice = input('Что вы хотите сделать?\n'
                            '1 - Вывести содержимое JSON файла\n'
                            '2 - Отсортировать вакансии в JSON файле по зарплате\n'
                            '3 - Вывести топ N вакансий\n'
                            '4 - Удалить вакансию по ID\n'
                            '5 - Завершить работу\n')
        with open('result.json', 'r') as file:
            data = file.read()
            parsed_data = json.loads(data)

        if user_choice == '1':
            print('Вывожу содержимое', end=' ')
            for _ in range(3):
                time.sleep(0.3)
                print('.', end='', flush=True)
            print()
            print_vacancies(parsed_data)

        if user_choice == '2':
            min_salary = int(input('Введите минимальную зарплату: '))
            sorted_vacancies = filter_by_salary('result.json', min_salary)
            print_vacancies(sorted_vacancies)

        if user_choice == '3':
            vacancies_count = int(input('Сколько вакансий вы хотите вывести? '))
            top_vacancies = get_top_vacancies('result.json', vacancies_count)
            print_vacancies(top_vacancies)

        if user_choice == '4':
            vacancy_id = int(input('Введите ID вакансии, которую хотите удалить '))
            saver = Save_to_json()
            saver.delete_vacancy(vacancy_id)

        if user_choice == '5':
            return 'Завершаю работу'


greetings = input(f'Приветствую! Чем займемся? \n'
                  f'1 - Поиск вакансий\n'
                  f'2 - Работа с существующим JSON файлом ')
if greetings == '1':
    go = interacion_with_user()
    print(go)
elif greetings == '2':
    go = user_interaction_with_json()
    print(go)
