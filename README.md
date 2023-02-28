# Тестовое задание. Медицинский справочник. Реализация REST API

---

## Описание проекта

В проекте реализовано API для работы со следующими объектами: справочник, версия справочника, элемент справочника. 

API предоставляет следующие методы:<br>
***1) Получение списка справочников***<br>
Метод: refbooks/[?date=<date>]
Тип запроса HTTP: GET.<br>
***2) Получение элементов заданного справочника***<br>
Метод: refbooks/<id>/elements[?version=<version>]
Тип запроса HTTP: GET<br>
***3) Валидация элементов***<br>
Метод: refbooks/<id>/check_element?code=<code>&value=<value>[&version=<version>]
Тип запроса HTTP: GET<br>


***Использованный стек:***
* Python 3.7
* Django 3.2.17
* Django REST framework 3.14.0
* drf-yasg (Yet another Swagger generator) 1.21.5
* Python-dotenv 0.20.0
* В качестве базы данных используется SQLite.


---

## Как установить проект
1) Создайте копию проекта командой `git clone https://github.com/Arthur-Akhmadullin/refbooks.git`. Копия будет помещена в папку "refbooks".
2) В командной строке перейдите в папку "refbooks": в Windows это можно сделать командой вида `cd /D D:\MyFiles\refbooks`. 
3) Создайте виртуальное окружение, выполнив команду `python -m venv <название-вашего-виртуального-окружения>`
4) Активируйте виртуальное окружение, выполнив команду `<название-вашего-виртуального-окружения>\Scripts\activate` (для Windows).
5) Далее необходимо установить библиотеки, используемые в проекте. Последовательно выполните команды: `python -m pip install`, `pip install -r requirements.txt`. Будут установлены библиотеки, указанные в файле requirements.txt.
6) В папке refbooks создайте файл ".env", в котором пропишите переменную SECRET_KEY: SECRET_KEY = "сгенерированный ключ". Сгенерировать секретный ключ можно на сайте [djecrety.ir](https://djecrety.ir).
7) Создайте базу данных, выполнив миграции командой: `python manage.py migrate`
8) Создайте профиль суперпользователя (администратора): `python manage.py createsuperuser`
9) При желании вы можете установить тестовую базу данных из файла refbooks.json, выпонив команду `python manage.py loaddata refbooks.json`. Тестовая база данных не содержит сведения о пользователях.
---
