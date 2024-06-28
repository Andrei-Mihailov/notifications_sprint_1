Проектная работа 10 спринта

Проектные работы в этом модуле выполняются в команде. Задания на спринт можно найти в соответствующих темах.

Ссылка на репозиторий: https://github.com/Andrei-Mihailov/notifications_sprint_1

Используемые технологии
Используемые технологии

Django - админка для формирования текста шаблонов и мгновенной отправки уведомлений пользователю/группе пользователей.
PostgreSQL - база данных для хранения информации о шаблонах, уведомлениях, пользователях.
FastAPI - сервис нотификаций, предоставляющий API для отправки уведомлений в очередь RabbitMQ как внутри сервиса уведомлений, так и из внешних сервисов (например, из сервиса Auth).
Clickhouse - хранилище информации об отправленных уведомлениях.
Сборка и запуск

Создайте и заполните .env на основе .env.example в папке envs.
Для сборки проекта из корневой папки выполните:

make build
Для запуска:

make up
Для создания суперпользователя:
make superuser
Поля таблиц БД
Template

slug - PK шаблона
title - Заголовок
description - Описание
content - Текст шаблона
Notification

template - FK на шаблон
name - Название шаблона, определяет имя очереди, в которую полетит уведомление
type - Тип рассылки (одиночная/групповая)
users - Пользователи, кому отправляется рассылка
groups - Группа пользователей для рассылки
Отправка уведомления из админки

Создайте Template.
Создайте Notification - выберите шаблон, тип рассылки, пользователей и/или группы пользователей.
Затем выделите нужное уведомление и в выпадающем окне выберите "Отправить уведомление пользователям".

Отправка уведомления из других сервисов

Пример запроса:

{
    "recipient": "9de57835-28b7-4cc7-be46-95a0fb1b17c1",
    "template_name": "statistic",
    "type_event": "personal",
    "context": {
        "title": "new_films",
        "email": "ivan@yandex.ru",
        "films": [
            {"id": 1, "title": "...", "date": "...", "description": "..."}
        ]
    }
}

Пример команды curl:

curl --location --request GET '127.0.0.1:8080/api/v1/send-notification/email' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=mKjF1tJ1h0WVkk9XM99EP2MAqP8i8cdSDAmcEBVhFsSxuIXaS3ROG87umafmJqcF' \
--data '{
    "recipient": "9de57835-28b7-4cc7-be46-95a0fb1b17c1",
    "template_name": "statistic",
    "type_event": "personal",
    "context": {
        "title": "new_films",
        "email": "ivan@yandex.ru",
        "films": [
            {"id": 1, "title": "...", "date": "...", "description": "..."}
        ]
    }
}'

Поля запроса:
recipient - Один UUID для персональной рассылки или список UUID при рассылке всем пользователям (all) - пустой список.
template_name - Название шаблона.
event - Тип события.
type_event - Тип рассылки (personal/group/all).
context - Контекст для подстановки данных в шаблон.
