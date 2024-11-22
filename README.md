<h1 align="center">Расчет стоимости страхования по имеющимся тарифам</h1>


##  Описание ##

REST API сервис по расчёту стоимости страхования в зависимости от типа груза и объявленной стоимости (ОС). При старте проекта заполняется таблица трифов по исходному json-файлу по пути api/app/static/rates.json.
![](https://github.com/katecapri/images-for-readme/blob/main/tables.png) 


##  Используемые технологии ##

- Python
- FastApi
- SQLAlchemy
- Asyncpg
- Alembic
- Docker
- Pylint
- Aiofiles
- PyJWT
- Confluent_kafka


##  Инструкция по запуску ##

1. Запуск всего проекта производится командой:

> make run


##  Результат ##

1. Новый пользоваель создается методом POST http://localhost:8000/auth/signup/
   
![](https://github.com/katecapri/images-for-readme/blob/main/signup_insurance.png)

2. Логин - метод POST http://localhost:8000/auth/login/
   
![](https://github.com/katecapri/images-for-readme/blob/main/login_insurance.png)


3. Расчет стоимости страхования, используя актуальный тариф, производится методом GET http://0.0.0.0:8000/insurance_cost с параметрами date, cargo_type, declared_value
   
![](https://github.com/katecapri/images-for-readme/blob/main/ins_cost.png)

4. Можно получать, изменять и удалять определенный тариф из таблицы тарифов соответствующими мметодами GET, POST, DELETE по url http://0.0.0.0:8000/rate/<rate_id> .
Обновление и удаление доступны только авторизованному пользователю (в запросе присылается JWT, полученный при логине). Сообщения об обновлении и удалении отправляются в Kafka.

![](https://github.com/katecapri/images-for-readme/blob/main/read.png)
![](https://github.com/katecapri/images-for-readme/blob/main/update.png)
![](https://github.com/katecapri/images-for-readme/blob/main/delete.png)
