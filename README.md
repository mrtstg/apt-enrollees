# apt-enrollees

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/) [![Svelte](https://img.shields.io/badge/svelte-%23f1413d.svg?style=for-the-badge&logo=svelte&logoColor=white)](https://svelte.dev/) [![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

Приложение для удобного просмотра абитуриентов с сайта [Альметьевского политехнического техникума](https://almetpt.ru).

[Опробовать приложение](https://almetpt.mrtstg.ru)

## Общие принципы работы

Бэкенд приложения на FastAPI осуществляет парсинг HTML-таблиц абитуриентов и кэширует данные в Redis для дальнейшего отображения через API.

Веб-приложение на Svelte обращается к API, получает список групп и студентов.

> В конце августа страницы со списками абитуриентов станут недоступны, так что приложение перестанет работать

## Структура проекта

    .
    ├── configs - директория с конфигурацией сервера
    ├── deployment - директория, содержащая Dockerfile и прочие файлы для развертывания
    ├── dist - директория с собранными webpack'ом файлами
    ├── modules - директория для подмодулей сервера
    ├── src - исходники для сборки
    │   ├── css
    │   └── js
    └── template - папка с шаблонами HTML

## Конфигурация сервера

Файл конфигурации распологается по пути ./configs/config.yaml

Примерный файл конфигурации (*и пояснения к полям*):

```yaml
    server:
        address: 127.0.0.1 - сеть, из которой сервер принимает запросы
        port: 30000 - порт сервера
        root_path: "" - корневой путь всех URL. Меняется в случае если приложение хостится по какому-то из пути доменов

    redis:
        host: redis - hostname или адрес базы
        port: 6379 - порт redis'а

    static:
        path: /static/ - путь по которому будут доступны статические файлы
        folder: ./dist - путь к директории содержащей их

    env_mapping: - alias'ы переменных конфига к переменным виртуального окружения
        server.port: PORT - например, сервер сначала проверит есть ли переменная окружения PORT и если ее нет, то возьмет переменную из конфига, что позволяет переписывать часть значений при деплое
        redis.host: REDIS_HOST
        redis.port: REDIS_PORT
```

## Развертывание

На продакшене приложение развертывается в контейнере при помощи podman ([примерный файл деплоя](/deployment/podman.yaml))

Для деплоя при помощи файла используйте команду

```bash
podman play kube deployment/podman.yaml
```

Для свертывания приложения используйте команду

```bash
podman play kube --down deployment/podman.yaml
```

> Остальные системы контейнеризации также могут использовать Dockefile для сборки приложения и его последующего развертывания

## Небольшие нюансы

- Приложение использует по умолчанию redis без аутентификации, поэтому не рекомендую разворачивать приложение там где к redis есть доступ извне
- При желании можно убрать декораторы кэширования в redis и обойтись без него. Но пожалейте сайт, все таки.
