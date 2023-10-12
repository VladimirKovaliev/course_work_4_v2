import requests
from abc import ABC, abstractmethod


class BaseHeadHunter(ABC):
    def get_vacancies(self):
        pass
class SuperJobAPI(BaseHeadHunter):
    """Класс для работы с АПИ hh.ru"""
    URL = 'https://api.superjob.ru/2.0/vacancies/'
    SECRET_KEY = 'v3.r.129594070.86ce97965df4aa99171a8b221330abf05a2b9f99.e7e10463137c9ac551eefa17ef14d0b27d536dcc'

    def __init__(self, text):
        self.__text = text
        self.params = {
            'keyword': self.__text,
        }
        self.header = {"X-Api-App-Id": SuperJobAPI.SECRET_KEY}
        self.vacations_list = []
        self.response = requests.get(SuperJobAPI.URL, headers=self.header)
        if not self.response.ok:
            raise Exception('SuperJobAPI problem')

    @property
    def text(self):
        return self.__text

    def get_vacancies(self):
        self.vacations_list = requests.get(SuperJobAPI.URL, headers=self.header, params=self.params)
        return self.vacations_list.json()['objects']

    def get_vacancy_info(self, vacancies):
        result_list = []
        for vacancy in vacancies:
            name = vacancy['profession']
            vacancy_id = vacancy['id']
            vacancy_link = vacancy['link']
            payment_from = vacancy['payment_from'] # от
            payment_to = vacancy['payment_to'] # до
            vacancy_location = vacancy['town']['title']
            experience = vacancy['experience']['title']
            #result_list.append({'name': name, 'id': vacancy_id,'payment_from': payment_from, 'payment_to': payment_to})
            if payment_from != 0 and payment_to != 0:
                result_list.append({'name': name, 'id': vacancy_id, 'salary': f'Зарплата от {payment_from} до {payment_to}', 'location': vacancy_location, 'experience': experience, 'link' : vacancy_link})
            elif payment_from != 0 and payment_to == 0:
                result_list.append({'name': name, 'id': vacancy_id, 'salary': f'Зарплата от {payment_from}', 'location': vacancy_location, 'experience': experience, 'link': vacancy_link})
            elif payment_from == 0 and payment_to != 0:
                result_list.append({'name': name, 'id': vacancy_id, 'salary': f'Зарплата до {payment_to}', 'location': vacancy_location, 'experience': experience, 'link': vacancy_link})
            elif payment_from == 0 and payment_to == 0:
                result_list.append({'name': name, 'id': vacancy_id, 'salary': f'Зарплата не указана', 'location': vacancy_location, 'experience': experience, 'link': vacancy_link})
            else:
                result_list.append({'name': name, 'id': vacancy_id, 'salary': f'Зарплата по договоренности', 'location': vacancy_location, 'experience': experience, 'link': vacancy_link})
        # currency = vacancy['currency']
        return result_list


# sj = SuperJobAPI('Мойщик окон')
# data = sj.get_vacancies()
# sorted_data = sj.get_vacancy_info(data)
# for vacancy in sorted_data:
#     print(f'{vacancy["name"]}, {vacancy["salary"]}, ID вакансии : {vacancy["id"]}, ({vacancy["location"]}) Опыт работы: {vacancy["experience"]} URL: {vacancy["link"]}')
#     print()

#{'canEdit': False, 'is_closed': False, 'id': 47316909, 'id_client': 235578, 'payment_from': 0, 'payment_to': 0, 'date_pub_to': 1698658223, 'date_archived': 0, 'date_published': 1697102867, 'address': 'Москва, Пресненская набережная, 10с1', 'profession': 'Продуктовый web-аналитик (Стрим дебетовые карты и счета)', 'work': None, 'compensation': None, 'candidat': 'Обязанности:\n• настройка системы сбора, процессов и методов по сбору данных;\n• настройка новых отчетов из Яндекс.Метрики;\n• настройка метрик на сайтах и посадочных страницах;\n• проверка данных на достоверность в системах аналитики при формировании еженедельных/ежедневных отчетов в системе Яндекс.Метрика;\n• проведение анализа результативности всех каналов трафика;\n• проведение анализа количественных и качественных показателей трафика на веб-сайте;\n• мониторинг поведенческих характеристик пользователей при посещении веб-сайта;\n• участие в подготовке тех.заданий на новые лендинги компании;\n• подготовка регулярного отчета по сайту и лендингам;\n• подготовка отчетов в различных срезах (по страницам, по городам, по продуктам, по аудитории, по конверсиям, по событиям, выстраивание воронки);\n• анализ данных и подготовка рекомендаций для команды маркетинга.\nТребования:\n• опыт работы не менее 2-х лет в банке/агентстве работающем с банками;\n• обязательное владение SQL на уровне сложных запросов;\n• опыт работы с системами визуализации данных PowerBI / Google Data Studio и т.д.;\n• визуализация данных с помощью дашбордов;\n• умение работать с большим массивом данных;\n• желательно знание Python;\n• свободное владение основными инструментами веб-аналитики (Яндекс Метрика, Google Analytics);\n• логика и cтратегическое мышление.', 'metro': [{'id': 555, 'title': 'Деловой центр', 'id_metro_line': 45}, {'id': 196, 'title': 'Международная', 'id_metro_line': 4}], 'currency': 'rub', 'vacancyRichText': '<p><b>Обязанности:</b></p><p><ul><li>настройка системы сбора, процессов и методов по сбору данных;</li><li>настройка новых отчетов из Яндекс.Метрики;</li><li>настройка метрик на сайтах и посадочных страницах;</li><li>проверка данных на достоверность в системах аналитики при формировании еженедельных/ежедневных отчетов в системе Яндекс.Метрика;</li><li>проведение анализа результативности всех каналов трафика;</li><li>проведение анализа количественных и качественных показателей трафика на веб-сайте;</li><li>мониторинг поведенческих характеристик пользователей при посещении веб-сайта;</li><li>участие в подготовке тех.заданий на новые лендинги компании;</li><li>подготовка регулярного отчета по сайту и лендингам;</li><li>подготовка отчетов в различных срезах (по страницам, по городам, по продуктам, по аудитории, по конверсиям, по событиям, выстраивание воронки);</li><li>анализ данных и подготовка рекомендаций для команды маркетинга.</li></ul><b>Требования:</b></p><p><ul><li>опыт работы не менее 2-х лет в банке/агентстве работающем с банками;</li><li>обязательное владение SQL на уровне сложных запросов;</li><li>опыт работы с системами визуализации данных PowerBI / Google Data Studio и т.д.;</li><li>визуализация данных с помощью дашбордов;</li><li>умение работать с большим массивом данных;</li><li>желательно знание Python;</li><li>свободное владение основными инструментами веб-аналитики (Яндекс Метрика, Google Analytics);</li><li>логика и cтратегическое мышление.</li></ul></p>', 'covid_vaccination_requirement': {'id': 1, 'title': 'Не важно'}, 'moveable': False, 'agreement': True, 'anonymous': False, 'is_archive': False, 'is_storage': False, 'type_of_work': {'id': 6, 'title': 'Полный рабочий день'}, 'place_of_work': {'id': 0, 'title': 'Не имеет значения'}, 'education': {'id': 0, 'title': 'Не имеет значения'}, 'experience': {'id': 2, 'title': 'От 1 года'}, 'maritalstatus': {'id': 0, 'title': 'Не имеет значения'}, 'children': {'id': 0, 'title': 'Не имеет значения'}, 'client': {'id': 235578, 'title': 'Банк ВТБ', 'link': 'https://www.superjob.ru/clients/bank-vtb-235578/vacancies.html', 'industry': [], 'description': 'Банк ВТБ является одним из лидеров национального банковского сектора и занимает прочные конкурентные позиции на всех сегментах рынка банковских услуг.\n\nГлавным акционером ВТБ с долей в 77,5% является Правительство РФ. В ходе проведенного в мае 2007 года IPO среди российских и международных инвесторов было размещено 22,5% акций ВТБ. Общий объем средств, привлеченных в рамках дополнительной эмиссий акций, составил около $8 млрд., что сделало IPO ВТБ крупнейшим публичным размещением акций в мире в 2007 году.\n\nКроме того, оно стало самым "народным IPO" в России за всю историю национального фондового рынка, по его итогам акционерами ВТБ стали более 120 тыс. россиян. Рыночная капитализация ВТБ, акции которого обращаются на ММВБ и РТС, а также на Лондонской фондовой бирже в форме Глобальных депозитарных расписок, по итогам размещения акций превысила $35,5 млрд. Размер уставного капитала ВТБ составляет 67,2 млрд. рублей.\nВТБ имеет наивысший для российских банков рейтинг международных рейтинговых агентств Moody`s Investors Service, Standard & Poor`s и Fitch. Российские рейтинговые агентства традиционно относят ВТБ к высшей группе надежности.\n\nДиверсифицируя свою деятельность, ВТБ постоянно расширяет круг проводимых на российском рынке операций и предоставляет клиентам широкий комплекс услуг, принятых в международной банковской практике.', 'vacancy_count': 118, 'staff_count': 'более 5000', 'client_logo': 'https://public.superjob.ru/images/clients_logos.ru/235578_94e8efbcca860a6a0147c0c1ad02b209.png', 'address': None, 'addresses': [], 'url': 'http://www.vtb.ru', 'short_reg': False, 'is_blocked': False, 'registered_date': 1224231921, 'town': {'id': 4, 'title': 'Москва', 'declension': 'в Москве', 'hasMetro': True, 'genitive': 'Москвы'}}, 'languages': [], 'driving_licence': [], 'catalogues': [{'id': 381, 'title': 'Банки, инвестиции, лизинг', 'key': 381, 'positions': [{'id': 411, 'title': 'Методология, разработка и продажа розничных продуктов', 'key': 411}]}], 'agency': {'id': 1, 'title': 'прямой работодатель'}, 'town': {'id': 4, 'title': 'Москва', 'declension': 'в Москве', 'hasMetro': True, 'genitive': 'Москвы'}, 'already_sent_on_vacancy': False, 'rejected': False, 'response_info': [], 'phone': '+7 (999) 13955XX', 'phones': [{'number': '799913955XX', 'additionalNumber': None}], 'fax': None, 'faxes': None, 'client_logo': 'https://public.superjob.ru/images/clients_logos.ru/235578_94e8efbcca860a6a0147c0c1ad02b209.png', 'highlight': True, 'age_from': 0, 'age_to': 0, 'gender': {'id': 0, 'title': 'Не имеет значения'}, 'firm_name': 'Банк ВТБ (ПАО)', 'firm_activity': 'Банк ВТБ является одним из лидеров национального банковского сектора и занимает прочные конкурентные позиции на всех сегментах рынка банковских услуг.\n\nГлавным акционером ВТБ с долей в 77,5% является Правительство РФ. В ходе проведенного в мае 2007 года IPO среди российских и международных инвесторов было размещено 22,5% акций ВТБ. Общий объем средств, привлеченных в рамках дополнительной эмиссий акций, составил около $8 млрд., что сделало IPO ВТБ крупнейшим публичным размещением акций в мире в 2007 году.\n\nКроме того, оно стало самым "народным IPO" в России за всю историю национального фондового рынка, по его итогам акционерами ВТБ стали более 120 тыс. россиян. Рыночная капитализация ВТБ, акции которого обращаются на ММВБ и РТС, а также на Лондонской фондовой бирже в форме Глобальных депозитарных расписок, по итогам размещения акций превысила $35,5 млрд. Размер уставного капитала ВТБ составляет 67,2 млрд. рублей.\nВТБ имеет наивысший для российских банков рейтинг международных рейтинговых агентств Moody`s Investors Service, Standard & Poor`s и Fitch. Российские рейтинговые агентства традиционно относят ВТБ к высшей группе надежности.\n\nДиверсифицируя свою деятельность, ВТБ постоянно расширяет круг проводимых на российском рынке операций и предоставляет клиентам широкий комплекс услуг, принятых в международной банковской практике.', 'link': 'https://www.superjob.ru/vakansii/produktovyj-web-analitik-47316909.html', 'latitude': 55.748913, 'longitude': 37.535477}
