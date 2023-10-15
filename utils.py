import json
from headhunter_api import HeadHunter_API
from superjob_api import SuperJobAPI, get_vacancy_info
from save_to_json import Save_to_json

import time


def filter_by_salary(json_file, min_salary):
    """Функция для сортировки вакансий"""
    with open(json_file) as f:
        data = json.load(f)
    filtered_data = []
    for job in data:
        if job['salary'].startswith('Зарплата от'):
            try:
                salary_from = int(job['salary'].split()[2])
                if salary_from >= min_salary:
                    filtered_data.append(job)
            except ValueError:
                pass
        else:
            try:
                salary = int(job['salary'].split()[0])
                if salary >= min_salary:
                    filtered_data.append(job)
            except ValueError:
                pass
    return filtered_data


def get_top_vacancies(json_file, vacancies_count):
    """Функция для вывода N количества вакансий"""
    with open(json_file) as f:
        data = json.load(f)
    sort_vacancies = []
    for vacancy in data:
        if vacancy['salary'].startswith('Зарплата от'):
            salary = int(vacancy['salary'].split()[2])
            sort_vacancies.append({'id': vacancy['id'],
                                   'name': vacancy['name'],
                                   'salary': salary,
                                   'location': vacancy.get('location', 'Локация не указана'),
                                   'experience': vacancy.get('experience', 'Опыт не нужен'),
                                   'link': vacancy.get('link', 'Ссылка отсутствует')})
        else:
            continue

    sort_vacancies = sorted(sort_vacancies, key=lambda x: x['salary'], reverse=True)
    return sort_vacancies[:vacancies_count]


def print_vacancies(vacancies):
    """Функция для вывода вакансий"""
    for job in vacancies:
        print(f" ID: {job.get('id', 'ID вакансии не указанно')},"
              f" {job.get('name', 'Название вакансии не указано')},"
              f" Зарплата: {job['salary']},"
              f" Локация: {job.get('location', 'Локация не указана')},"
              f" Опыт: {job.get('experience', '')},"
              f" Ссылка: {job.get('link', 'Ссылка отсутствует')}")


def interacion_with_user():
    """Функция для работы с пользователем, если он выбрал поиск вакансий"""
    global sj_sorted_vacancies, hh_sorted_vacancies, sorted_vacancies, user_filter
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
            sorted_vacancies = get_vacancy_info(data)
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
            sj_sorted_vacancies = get_vacancy_info(sj_data)
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
                except NameError:
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
    """Функция для работы с пользователем, если он выбрал работу с JSON файлом"""
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
            sort_vacancies = filter_by_salary('result.json', min_salary)
            print_vacancies(sort_vacancies)

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
