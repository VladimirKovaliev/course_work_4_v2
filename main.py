import json
from headhunter_api import HeadHunter_API
from superjob_api import SuperJobAPI
from save_to_json import Save_to_json
import time

def interacion_with_user():
    while True:

        set_platform = input('На какой платформе искать вакансии?\n'
                             '1 - для HeadHunter\n'
                             '2 - для SuperJob\n'
                             '3 - оба варианта\n'
                             '4 - завершить работу\n')
        if set_platform == '4':
            return ('Завершаю работу')
        elif set_platform not in ['1', '2', '3', '4']:
            return('Неизвестный ввод, завершаю работу')
        vacancy = input(f'Какую вакансию вы хотите найти? ')
        user_choise = input('Добавить фильтр для поиска?\n'
                            '1 - да \n'
                            '2 - нет \n')
        if user_choise == '1':
            user_filter = input('По какому фильтру подбирать вакансии? ')
        print('Идет поиск, подождите', end=' ')
        for _ in range(3):
            time.sleep(1)
            print('.', end='', flush=True)
        print()


        if set_platform == '1':
            '''Поиск вакансий на HH'''

            if user_choise == '1':
                hh = HeadHunter_API(vacancy, 1, user_filter)
            else:
                hh = HeadHunter_API(vacancy, 1)

            data = hh.get_vacancies()
            sorted_vacancies = hh.get_vacancy_info(data)
            for vacancy in sorted_vacancies:
                print(f"{vacancy['name']}: {vacancy['salary']} ({vacancy['area']}), URL:{vacancy['url']}")

        elif set_platform == '2':
            '''Поиск вакансий на SJ'''
            sj = SuperJobAPI(vacancy)
            data = sj.get_vacancies()
            sorted_vacancies = sj.get_vacancy_info(data)
            for vacancy in sorted_vacancies:
                print(f'{vacancy["name"]}, {vacancy["salary"]}, ID вакансии : {vacancy["id"]}, ({vacancy["location"]}) Опыт работы: {vacancy["experience"]} URL: {vacancy["link"]}')

        elif set_platform == '3':
            hh = HeadHunter_API(vacancy, 1, user_filter)
            sj = SuperJobAPI(vacancy)
            hh_data = hh.get_vacancies()
            sj_data = sj.get_vacancies()
            hh_sorted_vacancies = hh.get_vacancy_info(hh_data)
            sj_sorted_vacancies = sj.get_vacancy_info(sj_data)
            print('Вакансии из HH:')
            for vacancy in hh_sorted_vacancies:
                print(f"{vacancy['name']}: {vacancy['salary']} ({vacancy['area']}), URL:{vacancy['url']}")
            print('Вакансии из SuperJob')
            for vacancy in sj_sorted_vacancies:
                print(f'{vacancy["name"]}, {vacancy["salary"]}, ID вакансии : {vacancy["id"]}, ({vacancy["location"]}) Опыт работы: {vacancy["experience"]} URL: {vacancy["link"]}')

        elif set_platform == '4':
            return ('Завершаю работу')

        else:
            return('Неизвестный ввод')
        while True:
            user_choise = input('Сохранить результат в JSON файл?\n'
                                '1 - да\n'
                                '2 - нет\n'
                                '3 - Зачем это нужно?\n'
                                '4 - Завершить работу\n')
            if user_choise == '1':
                json = Save_to_json()
                json.add_vacancy(sorted_vacancies)
                json.save_to_file()
                print('Данные сохранены.')
                break
            elif user_choise == '2':
                break
            elif user_choise == '3':
                print('Это нужно для того, чтобы вы потом могли вывести, добавить, удалить или отсортировать вакансии')
                print()
            elif user_choise == '4':
                break
            else:
                print('Неверный выбор. Попробуйте снова.')
        user_choise = input('Продолжить работу?\n'
                            '1 - Да\n'
                            '2 - Завершить работу\n')
        if user_choise == '1':
            continue
        return 'Завершаю работу'
def user_interaction_with_json():
    while True:
        user_choise = input('Что вы хотите сделать?\n'
                            '1 - Вывести содержимое JSON файла\n'
                            '2 - Отсортировать вакансии в JSON файле по зарплате\n'
                            '3 - Вывести топ N вакансий\n'
                            '4 - Завершить работу\n')
        if user_choise == '1':
            print('Вывожу содержимое', end=' ')
            for _ in range(3):
                time.sleep(0.3)
                print('.', end='', flush=True)
            print()
            with open('result.json', 'r') as file:
                data = file.read()
                parsed_data = json.loads(data)
                for job in parsed_data:
                    print(job['name'], job['salary'], job.get('location', 'Локация не указана'), job.get('experience', 'Опыт не нужен'), job.get('link', 'Ссылка отсутствует'))
        if user_choise == '2':
            pass
            # Дальше идет сортировка, вывод топ вакансий, сохранение в JSON, поиск по ключевым словам, сортировка по зп




greetings = input(f'Приветствую! Чем займемся? \n'
                  f'1 - Поиск вакансий\n'
                  f'2 - Работа с существующим JSON файлом ')
if greetings == '1':
    go = interacion_with_user()
    print(go)
elif greetings == '2':
    go = user_interaction_with_json()
    print(go)


# with open('result.json', 'r') as file:
#     data = file.read()
#     parsed_data = json.loads(data)
#     for job in parsed_data:
#         print(job['name'], job['salary'], job['location'], job['experience'], job['link'])