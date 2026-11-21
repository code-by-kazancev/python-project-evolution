import time, os
from typing import Any
from DownloadAndSaveFileData import load_data, save_data, save_users
from Operations import ( 
    add_requests, view_all_requests, 
    view_archive_requests, validate_priority_map, 
    statistika_requests, delete_id_requests, 
    change_status_to_work, change_status_to_done, 
    show_sorted_by_category, show_sorted_by_hours, 
    compare_sorting, edit_request
)
from HelpOperations import view_id_requests, filter_search_requests, set_categories
from AlgoritmamTutNeMesto import linear_search
from models import Request, UrgentRequest, ScheduledRequest, User 

# --- КОНСТАНТЫ ---
author = "code-by-kazancev"
PRODUCT_NAME = "IT-СЕРВИС"
VERSION = "2.2"
urgent = False

categories = [
    "Не работает сетевой принтер", "Пропал доступ к базе 1С", 
    "Завис сервер учёта продукции", "Не подключается рабочий VPN", "Сломалась учётная запись"
]
priorities = ["A", "B", "C", "D", "FBI"]

# --- ПЕРЕРИСОВКА --- #
def clear_screen():
    # \033[2J — очищает весь экран
    # \033[H — перемещает курсор в левый верхний угол
    print("\033[2J\033[H", end="")

# --- ФУНКЦИЯ ДЛЯ КРАСИВОГО МЕНЮ ---
def draw_menu(title, items, width=50):
    # Рисует красивое центрированное меню #
    print("\n" + "=" * width)
    print("|" + title.center(width - 2) + "|")
    print("=" * width)
    for item in items:
        print("|" + item.center(width - 2) + "|")
    print("=" * width)

# --- ЗАГРУЗКА ДАННЫХ ---
requests = load_data("data.json", Request)
users = load_data("user.json", User)

# Если заявок нет, создаем тестовые (по одной каждого типа) #
if not requests:
    base_kwargs:dict[str, Any] = {
        "applicant": "Тестовый Пользователь",
        "workshop": 1,
        "hours": 2.0,
        "minutes": 120,
        "status": "Новая",
        "live_zayvki": 1,
        "executor": "Не назначен"
    }

    requests = [
        Request(
            id=1, category="Не работает сетевой принтер", 
            description="Обычная тестовая заявка", priority="D", **base_kwargs
        ),
        UrgentRequest(
            id=2, category="Пропал доступ к базе 1С", 
            description="Срочная тестовая заявка", priority="A", response_hours=1.0, **base_kwargs
        ),
        ScheduledRequest(
            id=3, category="Завис сервер учёта продукции", 
            description="Запланированная тестовая заявка", priority="B", planned_date="2026-12-31", **base_kwargs
        )
    ]
    save_data(requests)


print(f"================== {PRODUCT_NAME} {VERSION} ==================")
print(f"| {'Система управления IT-заявками предприятия':^47} |")
print(f"| {f'Автор: {author}':^47} |")
# Проверяем синхронизацию категорий и приоритетов
validate_priority_map(categories)
print("===================================================")


# ========================================================= #
# ГЛАВНЫЙ БЕСКОНЕЧНЫЙ ЦИКЛ ПРОГРАММЫ                   #
# ========================================================= #
while True:
    current_user = None 

    # -----------------------------------------------------
    # 1. ЦИКЛ АВТОРИЗАЦИИ
    # -----------------------------------------------------
    while current_user is None:
        auth_items = [
            "1. Войти в систему",
            "2. Зарегистрироваться как сотрудник",
            "Введите 'exit' для выхода из программы"
        ]
        draw_menu("АВТОРИЗАЦИЯ", auth_items)
        print()

        auth_choice = input("| Ваш выбор >> ").strip().lower()

        if auth_choice in ["exit", "выход", "0"]:
            print("| Программа завершена. До связи!")
            exit() 

        elif auth_choice == "1":
            login_input = input("\n| Введите ваш логин >> ").strip().lower()
            found_user = None

            # Ищем пользователя среди объектов User
            for u in users:
                if u.login == login_input:
                    found_user = u
                    break

            if found_user is None:
                print("| ❌ Пользователь не найден. Попробуйте снова или зарегистрируйтесь.")
                input("\n| Нажмите Enter для возврата в меню...")
                clear_screen()
                continue 

            print(f"\n| Найдена учетная запись: {found_user.name} (Роль: {found_user.role})\n")

            if found_user.role == "it_specialist":
                password = input("| Введите пароль сисадмина >> ").strip()
                # Используем метод объекта для проверки пароля
                if not found_user.check_password(password):
                    print("| ❌ Неверный пароль! Доступ запрещен.")
                    continue
            else: print("| Вход без пароля (сотрудник).")

            current_user = found_user
            clear_screen()
            print(f"| ✅ Добро пожаловать, {current_user.name}!")

        elif auth_choice == "2":
            print("\n|--- Регистрация нового сотрудника ---|")
            new_name = input("| Введите ваше ФИО >> ").strip()

            while True:
                workshop_raw = input("| Введите номер вашего цеха >> ").strip()
                if workshop_raw.isdigit() and int(workshop_raw) >= 1:
                    new_workshop = int(workshop_raw)
                    break
                print("| Пожалуйста, введите корректный номер цеха.")

            new_login = input("| Придумайте логин (латиницей) >> ").strip().lower()

            # Проверяем, свободен ли логин
            if any(u.login == new_login for u in users):
                print("| ❌ Этот логин уже занят!")
                continue

            # Создаем объект User
            new_user = User(
                login=new_login, 
                name=new_name, 
                role="employee", 
                workshop=new_workshop
            )
            users.append(new_user)
            save_users(users)

            print(f"| ✅ Регистрация успешна! Ваш логин: {new_login}")
            current_user = new_user 

        else: print("| Неверный выбор. Попробуйте снова.")

    # ----------------------------------------------------- #
    # 2. ЦИКЛ ГЛАВНОГО МЕНЮ (Работаем, пока не нажмем 0)    #
    # ----------------------------------------------------- #
    while True:
        # Формируем и рисуем меню в зависимости от роли #
        if current_user.role == "employee":
            emp_menu = [
                "1. Создать заявку",
                "2. Мои заявки (статус)",
                "3. Найти МОЮ заявку по id",
                "4. Поиск по категории",
                "0. Выйти из аккаунта"
            ]
            draw_menu("МЕНЮ СОТРУДНИКА", emp_menu)
            print()

        elif current_user.role == "it_specialist":
            admin_menu = [
                "1. Показать активные заявки",
                "2. Взять заявку в работу",
                "3. Закрыть заявку (Выполнена)",
                "4. Удалить заявку по ID",
                "5. Статистика заявок",
                "6. Фильтр / Поиск",
                "7. Множества Категорий",
                "8. Сохранить данные",
                "9. Архив выполненных",
                "10. Сортировка по категории",
                "11. Сортировка по времени",
                "12. Сравнение алгоритмов",
                "13. Редактировать заявку",
                "0. Выйти из аккаунта"
            ]
            draw_menu("МЕНЮ IT-СПЕЦИАЛИСТА", admin_menu)
            print()

        user_input = input(f"| {current_user.name}, ваш выбор >> ").strip()

        # --- ЛОГИКА СОТРУДНИКА ---
        if current_user.role == "employee":
            if user_input == "1": 
                now_id = max((r.id for r in requests), default=0) + 1
                colvo_zayvok = len(requests)
                add_requests(now_id, colvo_zayvok, 1, requests, categories, current_user)
                # add_requests имеет внутренний цикл, пауза не нужна
                clear_screen()

            elif user_input == "2":
                my_requests = [r for r in requests if r.applicant == current_user.name]
                if my_requests: view_all_requests(my_requests)
                else: print("| У вас пока нет заявок.")
                input("\n| Нажмите Enter для возврата в меню...")
                clear_screen()

            elif user_input == "3":
                my_requests = [r for r in requests if r.applicant == current_user.name]
                if my_requests: view_id_requests(my_requests)
                else: print("| У вас пока нет заявок.")
                # view_id_requests имеет внутренний цикл, пауза не нужна
                clear_screen()

            elif user_input == "4":
                my_requests = [r for r in requests if r.applicant == current_user.name]
                if my_requests:
                    search_word = input("| Введите слово для поиска >> ")
                    found, checks = linear_search(my_requests, search_word)
                    print(f"| Найдено: {len(found)}")
                    if found: view_all_requests(found)
                else: print("| У вас пока нет заявок.")
                input("\n| Нажмите Enter для возврата в меню...")
                clear_screen()

            elif user_input == "0":
                print(f"| {current_user.name}, вы вышли из системы.")
                save_data(requests)
                break # Возврат к авторизации

            else: 
                print("| Неверный пункт меню.")
                input("\n| Нажмите Enter...")
                clear_screen()

        # --- ЛОГИКА СИСАДМИНА ---
        elif current_user.role == "it_specialist":
            if user_input == "1": 
                view_all_requests(requests) if requests else print("| Заявок нет.")
                input("\n| Нажмите Enter для возврата в меню...")
                clear_screen()

            elif user_input == "2": 
                change_status_to_work(requests, current_user.name) if requests else print("| Нечего брать.")
                clear_screen()

            elif user_input == "3": 
                change_status_to_done(requests) if requests else print("| Нечего закрывать.")
                clear_screen()

            elif user_input == "4": 
                delete_id_requests(len(requests), requests) if requests else print("| Нечего удалять.")
                clear_screen()

            elif user_input == "5": 
                statistika_requests(requests) if requests else print("| Статистики нет.")
                input("\n| Нажмите Enter для возврата в меню...")
                clear_screen()

            elif user_input == "6": 
                filter_search_requests(requests, urgent) if requests else print("| Нечего фильтровать.")
                clear_screen()

            elif user_input == "7": 
                set_categories(requests) if requests else print("| Категорий нет.")
                input("\n| Нажмите Enter для возврата в меню...")
                clear_screen()

            elif user_input == "8": 
                save_data(requests)
                print("| Данные сохранены.")
                input("\n| Нажмите Enter для возврата в меню...")
                clear_screen()

            elif user_input == "9": 
                view_archive_requests(requests) if requests else print("| Архив пуст.")
                input("\n| Нажмите Enter для возврата в меню...")
                clear_screen()

            elif user_input == "10":
                show_sorted_by_category(requests) if requests else print("| Нечего сортировать.")
                input("\n| Нажмите Enter для возврата в меню...")
                clear_screen()

            elif user_input == "11":
                show_sorted_by_hours(requests) if requests else print("| Нечего сортировать.")
                input("\n| Нажмите Enter для возврата в меню...")
                clear_screen()

            elif user_input == "12":
                compare_sorting(requests) if requests else print("| Нечего сравнивать.")
                input("\n| Нажмите Enter для возврата в меню...")
                clear_screen()

            elif user_input == "13":
                edit_request(requests) if requests else print("| Нечего редактировать.")
                clear_screen()

            elif user_input == "0":
                print(f"| {current_user.name}, вы вышли из системы.")
                save_data(requests)
                break

            else: 
                print("| Неверный пункт меню.")
                input("\n| Нажмите Enter...")
                clear_screen()