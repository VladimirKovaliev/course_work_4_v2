import headhunter_api, superjob_api

hh = headhunter_api
sj = superjob_api
def interacion_with_user():
    while True:
        set_platform = input('На какой платформе искать вакансии?\n'
                             '1 - для HeadHunter\n'
                             '2 - для SuperJob\n'
                             '3 - оба варианта\n'
                             '4 - завершить работу\n')
        if set_platform == '1':
            return('Ищем работу на HH')

        elif set_platform == '2':
            return('Ищем работу на SJ')

        elif set_platform == '3':
            return('Ищем работу сразу на двух платформах')

        elif set_platform == '4':
            return ('Завершаю работу')

        else:
            return('Неизвестный ввод')

        # Дальше идет сортировка, вывод топ вакансий, сохранение в JSON, поиск по ключевым словам, сортировка по зп

go = interacion_with_user()
print(go)