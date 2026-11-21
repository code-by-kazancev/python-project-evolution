from AlgoritmamTutNeMesto import linear_search, find_first
from models import UrgentRequest, ScheduledRequest
from TableUtils import draw_table


# Поиск заявки по ID в цикле — ТАБЛИЦА
def view_id_requests(requests):
    while True:
        active = [r for r in requests if r.status != 'Выполнена']

        if not active:
            print("\n| Нет активных заявок.")
            break

        # Таблица доступных ID
        headers = ["ID", "Категория", "Статус"]
        col_widths = [5, 35, 15]

        rows = [[str(r.id), r.category, r.status] for r in active]
        draw_table(headers, rows, col_widths=col_widths, title="ДОСТУПНЫЕ ЗАЯВКИ")

        user_choice = input("\n| Введите ID заявки для поиска (или '0' для возврата в меню) >> ").strip()

        if user_choice == '0':
            print("| Возврат в главное меню.")
            break

        try:
            search_id = int(user_choice)
            found = False
            for r in requests:
                if r.id == search_id:
                    # Детальная информация в табличном формате
                    headers = ["Параметр", "Значение"]
                    col_widths = [22, 50]

                    rows = [
                        ["ID", str(r.id)],
                        ["Тип", r.get_type_name()],
                        ["Заявитель", r.applicant],
                        ["Цех", f"№{r.workshop}"],
                        ["Категория", r.category],
                        ["Приоритет", r.priority],
                        ["Описание", r.description],
                        ["Время", f"{r.hours} ч. ({r.minutes} мин.)"],
                        ["Статус", r.status],
                        ["Исполнитель", r.executor],
                    ]

                    if isinstance(r, UrgentRequest):
                        rows.append(["Время реакции", f"{r.response_hours} ч."])
                    elif isinstance(r, ScheduledRequest):
                        rows.append(["Дата выполнения", r.planned_date])

                    draw_table(headers, rows, col_widths=col_widths, title="ДЕТАЛЬНАЯ ИНФОРМАЦИЯ О ЗАЯВКЕ")
                    found = True
                    break

            if not found:
                print(f"\n| ❌ Заявка с ID {search_id} не найдена.")

        except ValueError:
            print("| ⚠ Ошибка! Введите целое число (ID заявки) или '0'.")


# Фильтрация заявок по различным критериям — ВСЕ ПУНКТЫ ТАБЛИЦА
def filter_search_requests(requests, urgent):
    while True:
        width = 50
        print(f"""
{"=" * width}
|{"ФИЛЬТР / ПОИСК".center(width - 2)}|
{"=" * width}
|{"1. Показать срочные (по типу)".center(width - 2)}|
|{"2. Показать по статусу".center(width - 2)}|
|{"3. Показать по категории".center(width - 2)}|
|{"4. Фильтр по типу заявки".center(width - 2)}|
|{"0. Назад в главное меню".center(width - 2)}|
{"=" * width}
""")

        filter_choice = input("| Ваш выбор (0–4) >> ").strip()

        if filter_choice == "0":
            break

        if filter_choice not in ["1", "2", "3", "4"]:
            print("| Неверный выбор. Введите 0–4.")
            continue

        found = False

        headers = ["ID", "Категория", "Приоритет", "Статус", "Доп. инфо"]
        col_widths = [5, 32, 11, 12, 20]

        # --- СРОЧНЫЕ (Используем isinstance вместо старого поля urgent) ---
        if filter_choice == "1":
            rows = []
            for r in requests:
                if isinstance(r, UrgentRequest):
                    extra_info = f"СРОЧНО: {r.response_hours} ч."
                    rows.append([
                        str(r.id),
                        r.category,
                        r.priority,
                        r.status,
                        extra_info
                    ])
                    found = True

            if found:
                draw_table(headers, rows, col_widths=col_widths, title="СРОЧНЫЕ ЗАЯВКИ (UrgentRequest)")
            else:
                print(f"\n| {'Срочных заявок нет. Можно прокастинировать!'.center(width - 2)}")
                print("=" * width)

        # --- ПО СТАТУСУ ---
        elif filter_choice == "2":
            status_filter = input("\n| Введите статус (Новая, В работе, Выполнена) >> ").lower()

            rows = []
            for r in requests:
                if status_filter in r.status.lower():
                    extra_info = ""
                    if isinstance(r, UrgentRequest):
                        extra_info = f"СРОЧНО: {r.response_hours} ч."
                    elif isinstance(r, ScheduledRequest):
                        extra_info = f"Дата: {r.planned_date}"

                    rows.append([
                        str(r.id),
                        r.category,
                        r.priority,
                        r.status,
                        extra_info
                    ])
                    found = True

            if found:
                draw_table(headers, rows, col_widths=col_widths, title=f"ЗАЯВКИ СО СТАТУСОМ: {status_filter.upper()}")
            else:
                msg = f"Заявок со статусом '{status_filter}' не найдено."
                print(f"\n| {msg.center(width - 2)}")
                print("=" * width)

        # --- ПО КАТЕГОРИИ ---
        elif filter_choice == "3":
            cat_filter = input("\n| Введите категорию или часть названия >> ").lower()

            rows = []
            for r in requests:
                if cat_filter in r.category.lower():
                    extra_info = ""
                    if isinstance(r, UrgentRequest):
                        extra_info = f"СРОЧНО: {r.response_hours} ч."
                    elif isinstance(r, ScheduledRequest):
                        extra_info = f"Дата: {r.planned_date}"

                    rows.append([
                        str(r.id),
                        r.category,
                        r.priority,
                        r.status,
                        extra_info
                    ])
                    found = True

            if found:
                draw_table(headers, rows, col_widths=col_widths, title=f"ЗАЯВКИ ПО КАТЕГОРИИ: {cat_filter.upper()}")
            else:
                msg = f"Категорий с '{cat_filter}' не найдено."
                print(f"\n| {msg.center(width - 2)}")
                print("=" * width)

        # --- ПО ТИПУ ЗАЯВКИ (Демонстрация isinstance) ---
        elif filter_choice == "4":
            print("\n| 1. Обычные\n| 2. Срочные\n| 3. Запланированные")
            type_choice = input("| Выберите тип для фильтрации (1-3) >> ").strip()

            rows = []
            for r in requests:
                show = False
                if type_choice == "1" and type(r).__name__ == "Request":
                    show = True
                elif type_choice == "2" and isinstance(r, UrgentRequest):
                    show = True
                elif type_choice == "3" and isinstance(r, ScheduledRequest):
                    show = True

                if show:
                    extra_info = ""
                    if isinstance(r, UrgentRequest):
                        extra_info = f"СРОЧНО: {r.response_hours} ч."
                    elif isinstance(r, ScheduledRequest):
                        extra_info = f"Дата: {r.planned_date}"

                    rows.append([
                        str(r.id),
                        r.category,
                        r.priority,
                        r.status,
                        extra_info
                    ])
                    found = True

            if found:
                type_names = {"1": "ОБЫЧНЫЕ", "2": "СРОЧНЫЕ", "3": "ЗАПЛАНИРОВАННЫЕ"}
                table_title = f"ФИЛЬТР ПО ТИПУ: {type_names.get(type_choice, 'ВСЕ')}"
                draw_table(headers, rows, col_widths=col_widths, title=table_title)
            else:
                print(f"\n| {'Заявок выбранного типа не найдено.'.center(width - 2)}")
                print("=" * width)

        print(f"\n{'=' * width}\n")


# Вывод списка уникальных категорий заявок
def set_categories(requests):
    used_categories = {req.category for req in requests}

    print("\n| ========== | Используемые категории | ========== |")
    for i, cat in enumerate(sorted(used_categories), start=1):
        print(f"| {i}. {cat}")
    print(f"""
| Всего уникальных категорий: {len(used_categories)}
| {"=" * 48} |""")