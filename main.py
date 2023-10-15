from utils import interacion_with_user, user_interaction_with_json

greetings = input(f'Приветствую! Чем займемся? \n'
                  f'1 - Поиск вакансий\n'
                  f'2 - Работа с существующим JSON файлом ')
if greetings == '1':
    go = interacion_with_user()
    print(go)
elif greetings == '2':
    go = user_interaction_with_json()
    print(go)

