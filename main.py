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
            user_filter = input('По какому фильтру подбирать вакансии?')
        print('Идет поиск, подождите', end=' ')
        for _ in range(3):
            time.sleep(1)
            print('.', end='', flush=True)
        print()
        json = Save_to_json()

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
            json.add_vacancy(sorted_vacancies)
            json.save_to_file()
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

        # Дальше идет сортировка, вывод топ вакансий, сохранение в JSON, поиск по ключевым словам, сортировка по зп

go = interacion_with_user()
print(go)