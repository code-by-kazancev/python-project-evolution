import time
from DownloadAndSaveFileData import load_data, save_data
from Operations import add_requests, view_all_requests, statistika_requests, delete_id_requests
from HelpOperations import view_id_requests, filter_search_requests, set_categories

PRODUCT_NAME = "IT-СЕРВИС"
VERSION = "1.9"
author = "code-by-kazancev"
urgent = False

now_id = 0
colvo_zayvok = 0
live_zayvki = 1

flag = True
requests = load_data("data.json")

# Если файл был пуст или только что создан, добавляем 3 тестовые заявки
if not requests:
    requests = [
        {
            "id": 1, "applicant": "Иванов И.И.", "workshop": 1,
            "category": "Не работает сетевой принтер", "description": "Принтер не печатает",
            "priority": "B", "hours": 1.0, "minutes": 60, "status": "Новая",
            "live_zayvki": 1, "urgent": False
        },
        {
            "id": 2, "applicant": "Петров П.П.", "workshop": 2,
            "category": "Пропал доступ к базе 1С", "description": "Нет связи с сервером",
            "priority": "A", "hours": 2.0, "minutes": 120, "status": "Новая",
            "live_zayvki": 1, "urgent": True
        },
        {
            "id": 3, "applicant": "Сидоров С.С.", "workshop": 3,
            "category": "Сломалась учётная запись", "description": "Не могу войти в систему",
            "priority": "C", "hours": 0.5, "minutes": 30, "status": "Новая",
            "live_zayvki": 1, "urgent": False
        }
    ]
    now_id = 3
    colvo_zayvok = 3
    save_data(requests)
else:
    now_id = max(r.get("id", 0) for r in requests)
    colvo_zayvok = len(requests)

categories = [
    "Не работает сетевой принтер",
    "Пропал доступ к базе 1С",
    "Завис сервер учёта продукции",
    "Не подключается рабочий VPN",
    "Сломалась учётная запись",
]
priorities = ["A", "B", "C", "D", "FBI"]

print(f"================== {PRODUCT_NAME} {VERSION} ==================")
print(f"| Автор: {author} |")

name = input("Введите ваше имя >> ")
print(f"Здравствуйте, {name}!")

while flag:
    print("""
    |--------| Меню |---------| 
    |    1. Создать заявку    |
    | 2. Показать все заявки  |
    |  3. Найти заявку по id  |
    |  4. Статистика  заявок  |
    | 5. Удалить заявку по id |
    |    6. Фильтр / Поиск    |
    |  7. Множества Категорий |
    |   8. Сохранить данные   |
    |       0. Выход          |
    |--------| Меню |---------| 
    """)

    user_input = input(f"{name}, выберите одно из перечисленных >> ").lower()

    if user_input == "1": 
        now_id, colvo_zayvok = add_requests(now_id, colvo_zayvok, live_zayvki, requests, priorities, categories)

    elif user_input == "2":
        if not requests:  print("| Прежде чем найти что-то, это надо сначала создать, гений!"); continue
        else: view_all_requests(requests)

    elif user_input == "3":
        if not requests:  print("| Прежде чем найти что-то, это надо сначала создать, гений!"); continue
        else: view_id_requests(requests)

    elif user_input == "4":
        if not requests:  print("| Прежде чем найти что-то, это надо сначала создать, гений!"); continue
        else: statistika_requests(requests)

    elif user_input == "5":
        if not requests:  print("| Прежде чем найти что-то, это надо сначала создать, гений!"); continue
        else: colvo_zayvok = delete_id_requests(colvo_zayvok, requests)

    elif user_input == "6":
        if not requests:  print("| Прежде чем найти что-то, это надо сначала создать, гений!"); continue
        else: filter_search_requests(requests, urgent)

    elif user_input == "7":
        if not requests:  print("| Прежде чем найти что-то, это надо сначала создать, гений!"); continue
        else: set_categories(requests)

    elif user_input == "8":
        save_data(requests)
        continue

    elif user_input == "0":
        save_data(requests)
        print(f"\n| {name}, благодарю вас за использование моей программы...")
        time.sleep(1)
        print(f"| До свидания: {name}!")
        break

    elif user_input == "меню".lower():
        print("""
    |--------| Меню |---------| 
    |       0. Выход          |
    |   8. Сохранить данные   |
    | 7. Множества Категорий  |
    |    6. Фильтр / Поиск    |
    | 5. Удалить заявку по id |
    |  4. Статистика  заявок  |
    |  3. Найти заявку по id  |
    |  2. Показать все заявки |
    |    1. Создать заявку    |
    |--------| Меню |---------| 
    """)   
        user_input = input(f"{name}, выберите одно из перечисленных << ")

        if user_input == '0':
            save_data(requests)
            print(f"\n| {name}, благодарю вас за использование моей программы...")
            time.sleep(1)
            print(f"| До свидания: {name}!")
            break
        else: continue

    else:
        print("| Активирую протокол перезагрузки: ")
        for i in range(10, 0, -1):
            print(f"| {i}")
            time.sleep(0.1)
        continue

print("================== Конец программы ==================")