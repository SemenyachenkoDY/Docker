# Лабораторная работа 1. 1. Установка и настройка Docker. Работа с контейнерами в Docker

## Цель работы
Освоить процесс установки и настройки Docker, научиться работать с основными командами CLI, контейнерами и образами. Понять принципы контейнеризации для развертывания аналитических сред и сервисов.

## Ход работы

Проверка версии Docker

<img width="747" height="528" alt="image" src="https://github.com/user-attachments/assets/3b3ae362-4853-4ff6-b15c-2ea6c9862de9" />

Просмотр скачанных образов

<img width="837" height="552" alt="image" src="https://github.com/user-attachments/assets/5a0a98c6-bf90-427b-b126-bfc91cbffb27" />

Просмотр запущенных контейнеров

<img width="830" height="125" alt="image" src="https://github.com/user-attachments/assets/7f1b897c-b369-4f60-94c7-4bbcd290601a" />

Просмотр запущенных контейнеров, включая остановленных

<img width="1053" height="523" alt="image" src="https://github.com/user-attachments/assets/0763bd6b-4592-4f1a-920b-ad6e0b4ac5d7" />

## Индивидуальное задание
### Вариант 5
#### Кэширование/NoSQL. Запустить контейнер, подключиться через redis-cli и создать несколько ключей (например, user:1, user:2) для имитации кэша сессий пользователей.

Запуск контейнера Redis

<img width="1060" height="197" alt="image" src="https://github.com/user-attachments/assets/306ecf22-45ca-4ecb-90cd-1e2f4e9cb716" />

Запуск CLI Redis, создание ключей

<img width="688" height="398" alt="image" src="https://github.com/user-attachments/assets/973a8288-8d6b-4bd6-a6a1-443e43642e64" />

Создание временного ключа (на 60 секунд) и выход из CLI

<img width="674" height="71" alt="image" src="https://github.com/user-attachments/assets/2ef2cc8d-729d-487f-802c-57c07cab8adb" />
<img width="337" height="179" alt="image" src="https://github.com/user-attachments/assets/570c3a9a-2564-4fb3-8121-d3af587a9a53" />

Остановка контейнера, проверка

<img width="1051" height="185" alt="image" src="https://github.com/user-attachments/assets/df9afa39-60cd-429c-af0d-8e34fde06a3f" />

## Вывод
В ходе выполнения лабораторной работы был изучен функционал Docker, а конкретно: запуск и остановка контейнеров, просмотр образов и запущенных контейнеров. Также была проведена работа в Redis: создание ключей сессии, обновление данных в сессии, установка времени жизни для ключа
