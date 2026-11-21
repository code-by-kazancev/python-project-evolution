from DownloadAndSaveFileData import save_data
from models import Request

CATEGORY_PRIORITY_MAP = {
    "Не работает сетевой принтер": "D",
    "Не подключается рабочий VPN": "C",
    "Завис сервер учёта продукции": "B",
    "Пропал доступ к базе 1С": "A",
    "Сломалась учётная запись": "FBI",
}

URGENT_PRIORITIES = {"A", "FBI"}


def add_requests(now_id, colvo_zayvok, live_zayvki, requests, categories, current_user):
    now_id += 1
    colvo_zayvok += 1

    print(f"""
|-----------| Обращение от сотрудника |-----------|
| ФИО сотрудника: {current_user.name}
| Цех №{current_user.workshop}
|{"-" * 49}|""")

    # --- ВЫБОР КАТЕГОРИИ ---
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

    # --- АВТОМАТИЧЕСКОЕ ОПРЕДЕЛЕНИЕ ПРИОРИТЕТА И СРОЧНОСТИ ---
    priority = CATEGORY_PRIORITY_MAP.get(category, "D")
    urgent = priority in URGENT_PRIORITIES
    urgent_line = "\n| ⚠ ВНИМАНИЕ: Заявка помечена как СРОЧНАЯ!" if urgent else ""

    print(f"""
| Выбранная категория: {category}
| Автоматически установлен приоритет: {priority}{urgent_line}
|{"-" * 49}|""")

    # --- ОПИСАНИЕ ---
    description = input("| Описание проблемы >> ")
    print(f"|{'-' * 49}|")

    # --- ВРЕМЯ НА РЕШЕНИЕ ---
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

    # Создаём объект Request вместо словаря
    new_request = Request(
        id=now_id,
        applicant=current_user.name,
        workshop=current_user.workshop,
        category=category,
        description=description,
        priority=priority,
        hours=hours,
        minutes=minutes,
        status="Новая",
        live_zayvki=live_zayvki,
        urgent=urgent,
        executor="Не назначен"
    )

    requests.append(new_request)
    save_data(requests)

    print(f"""
| ================= ЗАЯВКА СОЗДАНА ================= |
| ID: {new_request.id}
| Заявитель: {new_request.applicant}
| Цех №{new_request.workshop}
| Категория: {new_request.category}
| Описание: {new_request.description}
| Приоритет: {new_request.priority}
| Время на решение: {new_request.hours} ч. ({new_request.minutes} мин.)
| Статус: {new_request.status}
| Срочная: {'Да ⚠' if new_request.urgent else 'Нет'}
| Исполнитель: {new_request.executor}
| {"=" * 50} |
""")

    return now_id, colvo_zayvok


def view_all_requests(requests, only_active=True):
    # Показывает активные заявки или все вместе с архивом
    if only_active:
        filtered = [r for r in requests if r.status != 'Выполнена']
        print("\n| Активные заявки <-----------------------------|")
    else:
        filtered = requests
        print("\n| Все заявки (включая архив) <------------------|")

    if not filtered:
        print("| Пусто.")
        return

    for r in filtered:
        print(f"""
| ID: {r.id:<3} | Заявитель: {r.applicant:<15} | Цех №{r.workshop}
| Категория: [{r.category:<30}] | Приоритет: {r.priority:<5}
| Описание: {r.description}
| Время: {r.hours} ч. ({r.minutes} мин.)
| Статус: {r.status:<10} | Исполнитель: {r.executor}
| {"-" * 60} |
""")


def view_archive_requests(requests):
    # Показывает только выполненные заявки (архив)
    archive = [r for r in requests if r.status == 'Выполнена']
    print("\n| Архив выполненных заявок <----------------------|")

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

    for r in archive:
        print(f"""
| ID: {r.id:<3} | Заявитель: {r.applicant:<15} | Цех №{r.workshop}
| Категория: [{r.category:<30}] | Приоритет: {r.priority:<5}
| Описание: {r.description}
| Статус: {r.status:<10} | Исполнитель: {r.executor}
| {"-" * 60} |
""")


def statistika_requests(requests):
    total = len(requests)
    urgent_count = sum(1 for r in requests if r.urgent)
    completed_count = sum(1 for r in requests if r.status == "Выполнена")
    active_count = total - completed_count
    cat_counts = {}

    for r in requests:
        cat = r.category
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    width = 50

    # Заголовок
    print(f"""
{"=" * width}
|{"СТАТИСТИКА".center(width - 2)}|
{"=" * width}""")

    # Основная статистика
    print(f"""
| {"Всего заявок:".ljust(25)} {total}
| {"Активных:".ljust(25)} {active_count}
| {"Выполненных:".ljust(25)} {completed_count}
| {"Срочных (urgent):".ljust(25)} {urgent_count}
|{"-" * (width - 2)}|""")

    # Распределение по категориям
    print(f"""
| {"Распределение по категориям:".ljust(25)}
|{"-" * (width - 2)}|""")
    for cat, count in cat_counts.items():
        print(f"| {cat:<30} {count}")
    print(f"|{'-' * (width - 2)}|")

    # Первая и последняя заявка
    if requests:
        first_req = requests[0]
        last_req = requests[-1]
        print(f"""
| {"Первая заявка:".ljust(25)} ID {first_req.id}, '{first_req.category}'
| {"Последняя заявка:".ljust(25)} ID {last_req.id}, '{last_req.category}'
{"=" * width}""")
    else:
        print(f"""
| {"Нет заявок для анализа".center(width - 2)}
{"=" * width}""")


def delete_id_requests(colvo_zayvok, requests):
    # Удаление по реальному ID заявки в цикле, пока админ не введет '0'
    while True:
        width = 50
        print(f"""
|{"=" * width}|
|{"СПИСОК ЗАЯВОК".center(width - 2)}|
|{"-" * width}|""")

        # Показываем только активные заявки для удаления
        active_requests = [r for r in requests if r.status != 'Выполнена']

        if not active_requests:
            print("| Нет активных заявок для удаления. |")
            break

        for r in active_requests:
            print(f"| ID: {r.id:<3} | Категория: {r.category:<30} | Статус: {r.status} |")

        id_to_delete_input = input("\n| Введите ID заявки для удаления (или '0' для выхода) >> ").strip()

        if id_to_delete_input == '0':
            print("| Возврат в главное меню. |")
            break

        try:
            id_to_delete = int(id_to_delete_input)
            found = False
            for i, r in enumerate(requests):
                if r.id == id_to_delete:
                    if r.status == 'Выполнена':
                        print("| Нельзя удалить уже выполненную заявку (она в архиве). |")
                        found = True
                        break

                    removed = requests.pop(i)
                    colvo_zayvok -= 1
                    save_data(requests)
                    print(f"\n| Удалено: Заявка ID {removed.id}, категория: {removed.category} |")
                    found = True
                    break

            if not found:
                print(f"| Заявка с ID {id_to_delete} не найдена! |")

        except ValueError:
            print("| Ошибка! Введите целое число (ID заявки) или '0'. |")

    return colvo_zayvok


def change_status_to_work(requests, executor_name):
    # Сисадмин берет заявки в работу в цикле
    while True:
        width = 50
        print(f"""
|{"=" * width}|
|{"НОВЫЕ ЗАЯВКИ".center(width - 2)}|
|{"-" * width}|""")
        new_requests = [r for r in requests if r.status == 'Новая']

        if not new_requests:
            print("| Нет новых заявок для взятия в работу. |")
            break

        for r in new_requests:
            print(f"| ID: {r.id:<3} | Категория: {r.category:<30} | От: {r.applicant} |")

        req_id_input = input("\n| Введите ID заявки для взятия в работу (или '0' для выхода) >> ").strip()

        if req_id_input == '0':
            print("| Возврат в главное меню. |")
            break

        try:
            req_id = int(req_id_input)
            found = False
            for r in requests:
                if r.id == req_id:
                    if r.status != 'Новая':
                        print(f"| Заявка ID {req_id} уже в статусе '{r.status}'. Берём в работу только 'Новые'. |")
                        found = True
                        break
                    r.status = "В работе"
                    r.executor = executor_name
                    save_data(requests)
                    print(f"""
| Заявка ID {req_id} взята в работу! |
| Исполнитель: {executor_name} |""")
                    found = True
                    break

            if not found:
                print(f"| Заявка с ID {req_id} не найдена или она не новая. |")

        except ValueError:
            print("| Ошибка! Введите целое число (ID заявки) или '0'. |")


def change_status_to_done(requests):
    # Сисадмин закрывает заявки в цикле
    while True:
        width = 50
        print(f"""
|{"=" * width}|
|{"ЗАЯВКИ В РАБОТЕ".center(width - 2)}|
|{"-" * width}|""")

        in_work = [r for r in requests if r.status == 'В работе']

        if not in_work:
            print("| Нет заявок в работе для закрытия. |")
            break

        for r in in_work:
            print(f"| ID: {r.id:<3} | Категория: {r.category:<30} | Исполнитель: {r.executor} |")

        req_id_input = input("\n| Введите ID выполненной заявки (или '0' для выхода) >> ").strip()

        if req_id_input == '0':
            print("| Возврат в главное меню. |")
            break

        try:
            req_id = int(req_id_input)
            found = False
            for r in requests:
                if r.id == req_id:
                    if r.status != 'В работе':
                        print(f"| Заявка ID {req_id} имеет статус '{r.status}'. Закрываем только 'В работе'. |")
                        found = True
                        break
                    r.status = "Выполнена"
                    save_data(requests)
                    print(f"\n| Заявка ID {req_id} закрыта. Проблема решена! |")
                    found = True
                    break

            if not found:
                print(f"| Заявка с ID {req_id} не найдена или она не в работе. |")

        except ValueError:
            print("| Ошибка! Введите целое число (ID заявки) или '0'. |")


def show_sorted_by_category(requests):
    # Сортировка по категории (текстовое поле)
    from AlgoritmamTutNeMesto import sort_by_category
    if not requests:
        print("| Список пуст |")
        return

    sorted_reqs = sort_by_category(requests)
    width = 70

    print(f"""
{"=" * width}
|{"СОРТИРОВКА ПО КАТЕГОРИИ".center(width - 2)}|
{"=" * width}
|{"ID".center(5)}|{"Категория".center(40)}|{"Часы".center(10)}|{"Приоритет".center(10)}|
{"-" * width}""")

    for r in sorted_reqs:
        print(f"|{str(r.id).center(5)}|{r.category.center(40)}|{str(r.hours).center(10)}|{r.priority.center(10)}|")

    print("=" * width)


def show_sorted_by_hours(requests):
    # Сортировка по времени (числовое поле) через Bubble Sort
    from AlgoritmamTutNeMesto import bubble_sort_hours
    if not requests:
        print("| Список пуст |")
        return

    sorted_reqs, comparisons, swaps = bubble_sort_hours(requests)
    width = 70

    print(f"""
{"=" * width}
|{"СОРТИРОВКА ПО ВРЕМЕНИ (Bubble Sort)".center(width - 2)}|
{"=" * width}
|{"ID".center(5)}|{"Категория".center(40)}|{"Часы".center(10)}|{"Приоритет".center(10)}|
{"-" * width}""")

    for r in sorted_reqs:
        print(f"|{str(r.id).center(5)}|{r.category.center(40)}|{str(r.hours).center(10)}|{r.priority.center(10)}|")

    print(f"""
{"=" * width}
| {'Сравнений: ' + str(comparisons):<{width-2}} |
| {'Перестановок: ' + str(swaps):<{width-2}} |
{"=" * width}""")


def compare_sorting(requests):
    # Сравнение встроенной и пузырьковой сортировки
    from AlgoritmamTutNeMesto import sort_by_hours, bubble_sort_hours
    if not requests:
        print("| Список пуст |")
        return

    built_in = sort_by_hours(requests)
    bubble, comparisons, swaps = bubble_sort_hours(requests)
    width = 70

    print(f"""
{"=" * width}
|{"СРАВНЕНИЕ АЛГОРИТМОВ".center(width - 2)}|
{"=" * width}
| {'Встроенная sorted() и Bubble Sort дают одинаковый результат:':<{width-2}} |
| {str(built_in == bubble).center(width-2)} |
{"-" * width}
| {'Статистика Bubble Sort:':<{width-2}} |
| {'Сравнений: ' + str(comparisons):<{width-2}} |
| {'Перестановок: ' + str(swaps):<{width-2}} |
{"=" * width}""")


def validate_priority_map(categories):
    # Проверяет, что для каждой категории есть приоритет в маппинге
    missing = [cat for cat in categories if cat not in CATEGORY_PRIORITY_MAP]
    extra = [cat for cat in CATEGORY_PRIORITY_MAP if cat not in categories]

    if missing or extra:
        print("\n| ⚠ ВНИМАНИЕ: Рассинхрон категорий и приоритетов! |")
        for cat in missing:
            print(f"|   Категория '{cat}' НЕ имеет приоритета в маппинге |")
        for cat in extra:
            print(f"|   В маппинге есть лишний ключ '{cat}' |")
        print(f"""
| Проверь точное совпадение строк (падеж, пробелы, буквы ё/е)!
| {"=" * 50}
""")
    else:
        print("| ✅ Категории и приоритеты синхронизированы. |")