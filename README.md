# Общая информация

API для поиска работы на платформах HeadHunter и SuperJob

* Всё API работает по протоколу HTTPS.
* Авторизация осуществляется по протоколу OAuth2.
* Все данные доступны только в формате JSON.
* Базовый URL HH — `https://api.hh.ru/`
* Базовый URL SJ — `https://www.superjob.ru/`

  # Требования к запросам
* Если система просит выбрать один из вариантов, то нужно написать ей требуемое число
* При поиске вакансий нужно использовать кириллицу



API широко использует информирование при помощи кодов ответов.
Приложение должно корректно их обрабатывать.

В случае неполадок и сбоев, возможны ответы с кодом `503` и `500`.

## Внешние ссылки на статьи и стандарты

* [HTTP/1.1](http://tools.ietf.org/html/rfc2616)
* [JSON](http://json.org/)
* [URI Template](http://tools.ietf.org/html/rfc6570)
* [OAuth 2.0](http://tools.ietf.org/html/rfc6749)
* [REST](http://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)
* [ISO 8601](http://en.wikipedia.org/wiki/ISO_8601)
