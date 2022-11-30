# alltimetable
Таблица на все времена

Структура:
db_worker.py - модуль работы с БД
models.py - с помощью SQLModel описана структура БД
pydantic_models.py - с помощью pydantic описана выходных данных из парсера, она же будет передаваться в db_worker и другие места по необходимости
settings.py - файл с настройками, например  для подключения к postgres

В alembic.ini в раздел [alembic] нужно добавить
sqlalchemy.url = postgresql://имя_пользователя:пароль@хост/имя_базы