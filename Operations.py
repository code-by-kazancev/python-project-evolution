from typing import Any
from DownloadAndSaveFileData import save_data
from models import Request, UrgentRequest, ScheduledRequest
from TableUtils import draw_table

CATEGORY_PRIORITY_MAP = {
    "Не работает сетевой принтер": "D",
    "Не подключается рабочий VPN": "C",
    "Завис сервер учёта продукции": "B",
    "Пропал доступ к базе 1С": "A",
    "Сломалась учётная запись": "FBI",
}

URGENT_PRIORITIES = {"A", "FBI"}


# Создание новой заявки с выбором типа (обычная/срочная/запланированная)
def add_requests(now_id, colvo_zayvok, live_zayvki, requests, categories, current_user):
    now_id += 1
    colvo_zayvok += 1

    print(f"""
|-----------| Обращение от сотрудника |-----------|
| ФИО сотрудника: {current_user.name}
| Цех №{current_user.workshop}
|{'-' * 49}|
| Выберите тип заявки:
| 1. Обычная
| 2. Срочная (требует времени реакции)
| 3. Запланированная (требует даты выполнения)
|{'-' * 49}|""")

    while True:
        type_choice = input("| Введите номер типа заявки (1-3) >> ")
        if type_choice in ["1", "2", "3"]:
            break
        print("| Пожалуйста, введите 1, 2 или 3.")

    # --- ВЫБОР КАТЕГОРИИ (общий для всех) ---
    print("\n|---------| Выберите категорию проблемы |---------|")
    for i, cat in enumerate(categories, 1):
        priority_hint = CATEGORY_PRIORITY_MAP.get(cat, "?")
        print(f"| * {i}. {cat:<35} [Приоритет: {priority_hint}]")
    print(f"|{'-' * 49}|")

    while True:
        categ_choice = input("| Введите номер категории >> ")
        if categ_choice.isdigit() and 1 <= int(categ_choice) <= len(categories):
            category = categories[int(categ_choice) - 1]
            break
        else:
            print(f"| Пожалуйста, введите число от 1 до {len(categories)}.")

    # --- АВТОМАТИЧЕСКОЕ ОПРЕДЕЛЕНИЕ ПРИОРИТЕТА ---
    priority = CATEGORY_PRIORITY_MAP.get(category, "D")

    print(f"| Выбранная категория: {category}")
    print(f"| Автоматически установлен приоритет: {priority}")
    print(f"|{'-' * 49}|")

    # --- ОПИСАНИЕ И ВРЕМЯ (общие для всех) ---
    description = input("| Описание проблемы >> ")
    print(f"|{'-' * 49}|")

    print("\n|---------| Выделите время на решение проблемы |---------|")
    while True:
        hours_raw = input("| Оценка времени на решение (в часах) >> ")
        try:
            hours = float(hours_raw)
            if hours > 0:
                print(f"|{'-' * 56}|")
                break
            else:
                print("| Время должно быть больше 0.")
        except ValueError:
            print("| Пожалуйста, введите корректное число (например, 2.5).")

    minutes = int(hours * 60)

    # --- СПЕЦИФИЧНЫЕ ПОЛЯ ДЛЯ РАЗНЫХ ТИПОВ ---
    response_hours = 0.0
    planned_date = ""

    if type_choice == "2": # Срочная
        while True:
            rh_raw = input("| Время реакции на срочную заявку (в часах) >> ")
            try:
                response_hours = float(rh_raw)
                if response_hours > 0:
                    break
                print("| Время реакции должно быть больше 0.")
            except ValueError:
                print("| Введите корректное число.")

    elif type_choice == "3": # Запланированная
        while True:
            pd_raw = input("| Дата выполнения (в формате ГГГГ-ММ-ДД, например 2026-12-31) >> ")
            try:
                from datetime import datetime
                datetime.fromisoformat(pd_raw)
                planned_date = pd_raw
                break
            except ValueError:
                print("| Неверный формат даты. Используйте ГГГГ-ММ-ДД.")

    # --- СОЗДАНИЕ ОБЪЕКТА НУЖНОГО КЛАССА (ПОЛИМОРФИЗМ В ДЕЙСТВИИ) ---
    common_kwargs:dict[str, Any] = {
        "id": now_id,
        "applicant": current_user.name,
        "workshop": current_user.workshop,
        "category": category,
        "description": description,
        "priority": priority,
        "hours": hours,
        "minutes": minutes,
        "status": "Новая",
        "live_zayvki": live_zayvki,
        "executor": "Не назначен"
    }

    if type_choice == "1":
        new_request = Request(**common_kwargs)
    elif type_choice == "2":
        new_request = UrgentRequest(response_hours=response_hours, **common_kwargs)
    elif type_choice == "3":
        new_request = ScheduledRequest(planned_date=planned_date, **common_kwargs)

    requests.append(new_request)
    save_data(requests)

    # --- ФИНАЛЬНЫЙ ВЫВОД В ТАБЛИЧНОМ ФОРМАТЕ ---
    headers = ["Параметр", "Значение"]
    col_widths = [22, 50]

    rows = [
        ["Тип", new_request.get_type_name()],
        ["ID", str(new_request.id)],
        ["Заявитель", new_request.applicant],
        ["Цех", f"№{new_request.workshop}"],
        ["Категория", new_request.category],
        ["Описание", new_request.description],
        ["Приоритет", new_request.priority],
        ["Время на решение", f"{new_request.hours} ч. ({new_request.minutes} мин.)"],
        ["Статус", new_request.status],
        ["Исполнитель", new_request.executor],
    ]

    if isinstance(new_request, UrgentRequest):
        rows.append(["Время реакции", f"{new_request.response_hours} ч."])
    elif isinstance(new_request, ScheduledRequest):
        rows.append(["Дата выполнения", new_request.planned_date])

    draw_table(headers, rows, col_widths=col_widths, title="ЗАЯВКА СОЗДАНА")

    return now_id, colvo_zayvok


# Просмотр списка заявок (активных или всех, включая архив) — ТАБЛИЦА
def view_all_requests(requests, only_active=True):
    if only_active:
        filtered = [r for r in requests if r.status != 'Выполнена']
    else:
        filtered = requests

    if not filtered:
        print("| Пусто.")
        return

    headers = ["ID", "Категория", "Приоритет", "Статус", "Доп. инфо"]
    col_widths = [5, 32, 11, 12, 20]

    rows = []
    for r in filtered:
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

    title = "АКТИВНЫЕ ЗАЯВКИ" if only_active else "ВСЕ ЗАЯВКИ (ВКЛЮЧАЯ АРХИВ)"
    draw_table(headers, rows, col_widths=col_widths, title=title)


# Просмотр архива выполненных заявок (табличный формат)
def view_archive_requests(requests):
    archive = [r for r in requests if r.status == 'Выполнена']

    if not archive:
        active_count = len(requests)
        if active_count > 0:
            print(f"""
| Вставай Толстожопый!
| Заявок навалом: {active_count}, а архив пуст. Совестно не?
""")
        else:
            print("| Молоток! Отдыхай!")
        return

    headers = ["ID", "Категория", "Приоритет", "Исполнитель"]
    col_widths = [5, 32, 11, 22]
    rows = []

    for r in archive:
        rows.append([str(r.id), r.category, r.priority, r.executor])

    draw_table(headers, rows, col_widths=col_widths, title="АРХИВ ВЫПОЛНЕННЫХ ЗАЯВОК")


# Статистика по заявкам — ТАБЛИЦЫ
def statistika_requests(requests):
    total = len(requests)
    completed_count = sum(1 for r in requests if r.status == "Выполнена")
    active_count = total - completed_count

    # Подсчет по типам заявок (полиморфизм)
    type_counts = {"Обычная": 0, "Срочная": 0, "Запланированная": 0}
    for r in requests:
        type_name = r.get_type_name()
        type_counts[type_name] = type_counts.get(type_name, 0) + 1

    # Общая статистика в табличном формате
    headers = ["Показатель", "Значение"]
    col_widths = [25, 15]

    rows = [
        ["Всего заявок", str(total)],
        ["Активных", str(active_count)],
        ["Выполненных", str(completed_count)],
    ]

    draw_table(headers, rows, col_widths=col_widths, title="СТАТИСТИКА")

    # Таблица распределения по типам
    type_headers = ["Тип заявки", "Количество"]
    type_col_widths = [20, 15]
    type_rows = [
        ["Обычная", str(type_counts['Обычная'])],
        ["Срочная", str(type_counts['Срочная'])],
        ["Запланированная", str(type_counts['Запланированная'])]
    ]
    draw_table(type_headers, type_rows, col_widths=type_col_widths, title="РАСПРЕДЕЛЕНИЕ ПО ТИПАМ")

    # Таблица распределения по категориям
    cat_counts = {}
    for r in requests:
        cat = r.category
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    cat_headers = ["Категория", "Количество"]
    cat_col_widths = [35, 15]
    cat_rows = [[cat, str(count)] for cat, count in cat_counts.items()]
    draw_table(cat_headers, cat_rows, col_widths=cat_col_widths, title="РАСПРЕДЕЛЕНИЕ ПО КАТЕГОРИЯМ")

    # Первая и последняя заявка
    if requests:
        first_req = requests[0]
        last_req = requests[-1]
        width = 50
        print(f"""
{"=" * width}
| {"Первая заявка:".ljust(25)} ID {first_req.id}, '{first_req.category}'
| {"Последняя заявка:".ljust(25)} ID {last_req.id}, '{last_req.category}'
{"=" * width}""")


# Удаление заявки по ID в цикле — ТАБЛИЦА
def delete_id_requests(colvo_zayvok, requests):
    while True:
        active_requests = [r for r in requests if r.status != 'Выполнена']

        if not active_requests:
            print("\n| Нет активных заявок для удаления.")
            break

        headers = ["ID", "Категория", "Приоритет", "Статус", "Доп. инфо"]
        col_widths = [5, 32, 11, 12, 20]

        rows = []
        for r in active_requests:
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

        draw_table(headers, rows, col_widths=col_widths, title="СПИСОК ЗАЯВОК ДЛЯ УДАЛЕНИЯ")

        id_to_delete_input = input("\n| Введите ID заявки для удаления (или '0' для выхода) >> ").strip()

        if id_to_delete_input == '0':
            print("| Возврат в главное меню.")
            break

        try:
            id_to_delete = int(id_to_delete_input)
            found = False
            for i, r in enumerate(requests):
                if r.id == id_to_delete:
                    if r.status == 'Выполнена':
                        print("| Нельзя удалить уже выполненную заявку (она в архиве).")
                        found = True
                        break

                    removed = requests.pop(i)
                    colvo_zayvok -= 1
                    save_data(requests)
                    print(f"\n| Удалено: Заявка ID {removed.id}, категория: {removed.category}")
                    found = True
                    break

            if not found:
                print(f"| Заявка с ID {id_to_delete} не найдена!")

        except ValueError:
            print("| Ошибка! Введите целое число (ID заявки) или '0'.")

    return colvo_zayvok


# Взятие заявки в работу сисадмином — ТАБЛИЦА
def change_status_to_work(requests, executor_name):
    while True:
        new_requests = [r for r in requests if r.status == 'Новая']

        if not new_requests:
            print("\n| Нет новых заявок для взятия в работу.")
            break

        headers = ["ID", "Категория", "Приоритет", "Заявитель", "Доп. инфо"]
        col_widths = [5, 32, 11, 22, 20]

        rows = []
        for r in new_requests:
            extra_info = ""
            if isinstance(r, UrgentRequest):
                extra_info = f"СРОЧНО: {r.response_hours} ч."
            elif isinstance(r, ScheduledRequest):
                extra_info = f"Дата: {r.planned_date}"

            rows.append([
                str(r.id),
                r.category,
                r.priority,
                r.applicant,
                extra_info
            ])

        draw_table(headers, rows, col_widths=col_widths, title="НОВЫЕ ЗАЯВКИ")

        req_id_input = input("\n| Введите ID заявки для взятия в работу (или '0' для выхода) >> ").strip()

        if req_id_input == '0':
            print("| Возврат в главное меню.")
            break

        try:
            req_id = int(req_id_input)
            found = False
            for r in requests:
                if r.id == req_id:
                    if r.status != 'Новая':
                        print(f"| Заявка ID {req_id} уже в статусе '{r.status}'. Берём в работу только 'Новые'.")
                        found = True
                        break
                    r.status = "В работе"
                    r.executor = executor_name
                    save_data(requests)
                    print(f"\n| Заявка ID {req_id} взята в работу!")
                    print(f"| Исполнитель: {executor_name}")
                    found = True
                    break

            if not found:
                print(f"| Заявка с ID {req_id} не найдена или она не новая.")

        except ValueError:
            print("| Ошибка! Введите целое число (ID заявки) или '0'.")


# Закрытие заявки (перевод в статус 'Выполнена') в цикле (табличный формат)
def change_status_to_done(requests):
    while True:
        in_work = [r for r in requests if r.status == 'В работе']

        if not in_work:
            print("\n| Нет заявок в работе для закрытия.")
            break

        headers = ["ID", "Категория", "Приоритет", "Доп. инфо", "Исполнитель"]
        col_widths = [5, 32, 11, 20, 22]
        rows = []

        for r in in_work:
            extra_info = ""
            if isinstance(r, UrgentRequest):
                extra_info = f"СРОЧНО: {r.response_hours} ч."
            elif isinstance(r, ScheduledRequest):
                extra_info = f"Дата: {r.planned_date}"

            rows.append([str(r.id), r.category, r.priority, extra_info, r.executor])

        draw_table(headers, rows, col_widths=col_widths, title="ЗАЯВКИ В РАБОТЕ")

        req_id_input = input("\n| Введите ID выполненной заявки (или '0' для выхода) >> ").strip()

        if req_id_input == '0':
            print("| Возврат в главное меню.")
            break

        try:
            req_id = int(req_id_input)
            found = False
            for r in requests:
                if r.id == req_id:
                    if r.status != 'В работе':
                        print(f"| Заявка ID {req_id} имеет статус '{r.status}'. Закрываем только 'В работе'.")
                        found = True
                        break
                    r.status = "Выполнена"
                    save_data(requests)
                    print(f"\n| Заявка ID {req_id} закрыта. Проблема решена!")
                    found = True
                    break

            if not found:
                print(f"| Заявка с ID {req_id} не найдена или она не в работе.")

        except ValueError:
            print("| Ошибка! Введите целое число (ID заявки) или '0'.")


# Вывод списка заявок, отсортированных по категории (табличный формат)
def show_sorted_by_category(requests):
    from AlgoritmamTutNeMesto import sort_by_category
    if not requests:
        print("| Список пуст")
        return

    sorted_reqs = sort_by_category(requests)

    headers = ["ID", "Категория", "Приоритет", "Часы", "Тип"]
    col_widths = [5, 32, 11, 10, 18]
    rows = []

    for r in sorted_reqs:
        rows.append([str(r.id), r.category, r.priority, str(r.hours), r.get_type_name()])

    draw_table(headers, rows, col_widths=col_widths, title="СОРТИРОВКА ПО КАТЕГОРИИ")


# Вывод списка заявок, отсортированных по времени (табличный формат)
def show_sorted_by_hours(requests):
    from AlgoritmamTutNeMesto import bubble_sort_hours
    if not requests:
        print("| Список пуст")
        return

    sorted_reqs, comparisons, swaps = bubble_sort_hours(requests)

    headers = ["ID", "Категория", "Приоритет", "Часы", "Тип"]
    col_widths = [5, 32, 11, 10, 18]
    rows = []

    for r in sorted_reqs:
        rows.append([str(r.id), r.category, r.priority, str(r.hours), r.get_type_name()])

    draw_table(headers, rows, col_widths=col_widths, title="СОРТИРОВКА ПО ВРЕМЕНИ (Bubble Sort)")

    width = 90
    print(f"""
{"-" * width}
| {'Сравнений: ' + str(comparisons):<{width-4}} |
| {'Перестановок: ' + str(swaps):<{width-4}} |
{"-" * width}""")


# Сравнение встроенной sorted() и пузырьковой сортировки (табличный формат)
def compare_sorting(requests):
    from AlgoritmamTutNeMesto import sort_by_hours, bubble_sort_hours
    if not requests:
        print("| Список пуст")
        return

    built_in = sort_by_hours(requests)
    bubble, comparisons, swaps = bubble_sort_hours(requests)

    headers = ["ID", "Категория", "Часы", "Тип"]
    col_widths = [5, 32, 10, 18]
    rows = []

    for r in built_in:
        rows.append([str(r.id), r.category, str(r.hours), r.get_type_name()])

    draw_table(headers, rows, col_widths=col_widths, title="СРАВНЕНИЕ АЛГОРИТМОВ СОРТИРОВКИ")

    width = 90
    print(f"""
{"-" * width}
| {'Встроенная sorted() и Bubble Sort дают одинаковый результат: ' + str(built_in == bubble):<{width-4}} |
| {'Статистика Bubble Sort:':<{width-4}} |
| {'Сравнений: ' + str(comparisons):<{width-4}} |
| {'Перестановок: ' + str(swaps):<{width-4}} |
{"-" * width}""")


# Редактирование существующей заявки в цикле (табличный формат в начале)
def edit_request(requests):
    active_requests = [r for r in requests if r.status != 'Выполнена']

    if not active_requests:
        print("| Нет активных заявок для редактирования.")
        return

    headers = ["ID", "Категория", "Приоритет", "Статус", "Доп. инфо"]
    col_widths = [5, 32, 11, 12, 20]
    rows = []

    for r in active_requests:
        extra_info = ""
        if isinstance(r, UrgentRequest):
            extra_info = f"СРОЧНО: {r.response_hours} ч."
        elif isinstance(r, ScheduledRequest):
            extra_info = f"Дата: {r.planned_date}"

        rows.append([str(r.id), r.category, r.priority, r.status, extra_info])

    draw_table(headers, rows, col_widths=col_widths, title="РЕДАКТИРОВАНИЕ ЗАЯВКИ")

    req_id_input = input("\n| Введите ID заявки для редактирования >> ").strip()

    try:
        req_id = int(req_id_input)
    except ValueError:
        print("| Ошибка! Введите целое число.")
        return

    target_req = None
    for r in requests:
        if r.id == req_id:
            target_req = r
            break

    if not target_req:
        print(f"| Заявка с ID {req_id} не найдена.")
        return

    print(f"\n| Выбрана заявка: {target_req.get_short_info()}")

    # --- ЦИКЛ РЕДАКТИРОВАНИЯ ---
    while True:
        menu_items = [
            "1. Изменить категорию",
            "2. Изменить описание",
            "3. Изменить приоритет",
            "4. Изменить статус",
            "5. Изменить время на решение (часы)",
        ]

        if isinstance(target_req, UrgentRequest):
            menu_items.append("6. Изменить время реакции (срочная)")
        elif isinstance(target_req, ScheduledRequest):
            menu_items.append("6. Изменить дату выполнения (запланированная)")

        menu_items.append("0. Завершить редактирование")

        print(f"\n| Доступные действия:")
        for item in menu_items:
            print(f"| {item}")
        print(f"{'-' * 90}")

        choice = input("| Ваш выбор >> ").strip()

        if choice == "0":
            print("| Редактирование завершено. Возврат в меню.")
            break

        success = False

        if choice == "1":
            new_cat = input("| Новая категория >> ").strip()
            if new_cat:
                target_req.category = new_cat
                success = True

        elif choice == "2":
            new_desc = input("| Новое описание >> ").strip()
            if new_desc:
                target_req.description = new_desc
                success = True

        elif choice == "3":
            new_pri = input("| Новый приоритет (A/B/C/D/FBI) >> ").strip().upper()
            success = target_req.change_priority(new_pri)
            if not success:
                print("| Ошибка: недопустимый приоритет.")

        elif choice == "4":
            new_stat = input("| Новый статус (Новая/В работе/Выполнена) >> ").strip()
            success = target_req.change_status(new_stat)
            if not success:
                print("| Ошибка: недопустимый статус.")

        elif choice == "5":
            new_hours_raw = input("| Новое время на решение (в часах) >> ").strip()
            try:
                new_hours = float(new_hours_raw)
                if new_hours > 0:
                    target_req.hours = new_hours
                    target_req.minutes = int(new_hours * 60)
                    success = True
                else:
                    print("| Время должно быть больше 0.")
            except ValueError:
                print("| Ошибка: введите число.")

        elif choice == "6":
            if isinstance(target_req, UrgentRequest):
                new_rh_raw = input("| Новое время реакции (в часах) >> ").strip()
                try:
                    new_rh = float(new_rh_raw)
                    success = target_req.change_response_hours(new_rh)
                    if not success:
                        print("| Ошибка: время реакции должно быть больше 0.")
                except ValueError:
                    print("| Ошибка: введите число.")

            elif isinstance(target_req, ScheduledRequest):
                new_pd = input("| Новая дата выполнения (ГГГГ-ММ-ДД) >> ").strip()
                success = target_req.change_planned_date(new_pd)
                if not success:
                    print("| Ошибка: неверный формат даты.")
        else:
            print("| Неверный пункт меню.")
            continue

        if success:
            save_data(requests)
            print(f"\n| ✅ Заявка ID {req_id} успешно обновлена!")
            print(f"| Текущее состояние: {target_req.get_short_info()}")
        else:
            print("| Изменения не были применены.")


# Проверка синхронизации списка категорий и маппинга приоритетов
def validate_priority_map(categories):
    missing = [cat for cat in categories if cat not in CATEGORY_PRIORITY_MAP]
    extra = [cat for cat in CATEGORY_PRIORITY_MAP if cat not in categories]

    if missing or extra:
        print("\n| ⚠ ВНИМАНИЕ: Рассинхрон категорий и приоритетов!")
        for cat in missing:
            print(f"|   Категория '{cat}' НЕ имеет приоритета в маппинге")
        for cat in extra:
            print(f"|   В маппинге есть лишний ключ '{cat}'")
        print(f"""
| Проверь точное совпадение строк (падеж, пробелы, буквы ё/е)!
| {"=" * 50}
""")
    else:
        print(f"| {'✅ Категории и приоритеты синхронизированы.':^46} |")