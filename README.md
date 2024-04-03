# Тестовое задание в компанию _"ООО БУЛАТ"_

## Задание

Задание пока что не прикрепляю, чтобы случайно не распространить решение.

## Реализовано

- [x] gRPC-приложение
- [x] Корректное завершение приложения (graceful shutdown)
- [x] Миграции для базы данных
- [x] Логирование
- [x] Тестирование
- [x] Линтер
- [x] Сборка приложения в контейнеры

## gRPC-приложение

Контракт описан в файле [transaction.proto](protos%2Ftransaction.proto).

### sum_amount

> **Считает общую сумму для всех транзакций во временном диапазоне для определенного пользователя.**

На вход принимает **CalculateUserTotalSumRequest**, где

- user_id - идентификатор пользователя (int32);
- start_from - от какой даты берутся транзакции (unix time);
- end_from - до какой даты берутся транзакции (unix time);

```protobuf
message CalculateUserTotalSumRequest {
  uint32 user_id = 1;
  uint32 start_from = 2;
  uint32 end_from = 3;
}
```

Возвращает **CalculateUserTotalSumResponse**, где

- value - сумма всех транзакций (int32);
- execution_time - время выполнения в миллисекундах (int32);

```protobuf
message CalculateUserTotalSumResponse {
  uint32 value = 1;
  uint32 execution_time = 2;
}
```

## Запуск

```shell 
docker compose --project-name test --file deployment/docker-compose.yaml up
```

> Важно! После того как база данных поднялась, требуется применить [миграции](#миграции).

### Переменные окружения

|    Переменная    | Обязательная | Описание                           | Значение по умолчанию |
|:----------------:|:------------:|------------------------------------|-----------------------|
|     DB_USER      |      Да      | Пользователь для подключения к БД. | `test`                |
|   DB_PASSWORD    |      Да      | Пароль для подключения к БД.       | `test`                |
|     DB_HOST      |      Да      | Хост для подключения к БД.         | `localhost`           |
|     DB_PORT      |      Да      | Порт для подключения к БД.         | `6432`                |
|   DB_DATABASE    |      Да      | Название БД для подключения к БД.  | `postgres`            |
| APPLICATION_HOST |     Нет      | Хост приложения.                   | `0.0.0.0`             |
| APPLICATION_PORT |     Нет      | Порт приложения.                   | `50501`               |

## Увеличение скорости работы приложения

Имеем 10_000_000 строк и 1_000 пользователей.

Чтобы запросы выполнялись быстро:

- В базу данных добавлен индекс на атрибуты user_id и timestamp (ускорение более, чем в 10 раз);
- Используется пул подключений к базе данных;

## Миграции

Мне не хотелось иметь зависимость от SQLAlchemy и Alembic, поэтому миграции написаны и применяются вручную.
После того как база данных поднялась, требуется применить миграции:

1. [1_create_transaction_table.sql](migrations%2F1_create_transaction_table.sql)
2. [2_populate_transaction_table.sql](migrations%2F2_populate_transaction_table.sql)

## Структурированное логирование

С помощью [structlog](https://www.structlog.org/en/stable/) реализовано структурированное логирование в файл
**application.log** и **stdout**.

## Тестирование

> **Для корректного запуска тестов требуется установленный Docker.**

Установка зависимостей для тестирования:

```shell
pip install -r requirements-test.txt
```

Для запуска тестов требуется в корневой директории проекта выполнить команду:

```shell 
python -m pytest
```

## Линтер

В качестве линтера используется [Ruff](https://docs.astral.sh/ruff/).
Настройка правил производится в [pyproject.toml](pyproject.toml).
Подробнее про настройки правил можно прочитать в [документации Ruff](https://docs.astral.sh/ruff/configuration/).

Для проверки кода требуется в корневой директории проекта выполнить команду:

```shell 
ruff check .
```

## Корректно выполненный запрос

![img.png](assets/postman.png)