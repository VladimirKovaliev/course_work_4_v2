import json


def filter_by_salary(json_file, min_salary):
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
    with open(json_file) as f:
        data = json.load(f)
    sorted_vacancies = []
    for vacancy in data:
        if vacancy['salary'].startswith('Зарплата от'):
            salary = int(vacancy['salary'].split()[2])
            sorted_vacancies.append({'id': vacancy['id'],
                                     'name': vacancy['name'],
                                     'salary': salary,
                                     'location': vacancy.get('location', 'Локация не указана'),
                                     'experience': vacancy.get('experience', 'Опыт не нужен'),
                                     'link': vacancy.get('link', 'Ссылка отсутствует')})
        else:
            continue

    sorted_vacancies = sorted(sorted_vacancies, key=lambda x: x['salary'], reverse=True)
    return sorted_vacancies[:vacancies_count]


def print_vacancies(vacancies):
    for job in vacancies:
        print(f" ID: {job.get('id', 'ID вакансии не указанно')},"
              f" {job.get('name', 'Название вакансии не указано')},"
              f" Зарплата: {job['salary']},"
              f" Локация: {job.get('location', 'Локация не указана')},"
              f" Опыт: {job.get('experience', '')},"
              f" Ссылка: {job.get('link', 'Ссылка отсутствует')}")