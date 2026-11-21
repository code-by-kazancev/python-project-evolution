from AlgoritmamTutNeMesto import linear_search, find_first


def view_id_requests(requests):
    # Поиск заявки по ID в цикле
    while True:
        width = 50
        print(f"""
{"=" * width}
|{"ПОИСК ЗАЯВКИ ПО ID".center(width - 2)}|
{"-" * width}""")

        active = [r for r in requests if r.status != 'Выполнена']
        if active:
            print("| Доступные ID заявок:")
            for r in active:
                print(f"|   ID: {r.id:<3} — {r.category}")

        user_choice = input("\n| Введите ID заявки для поиска (или '0' для возврата в меню) >> ").strip()

        if user_choice == '0':
            print("| Возврат в главное меню.")
            break

        try:
            search_id = int(user_choice)
            found = False
            for r in requests:
                if r.id == search_id:
                    print(f"""
| ID: {r.id}
| Заявитель: {r.applicant}
| Цех №{r.workshop}
| Категория: [{r.category}]
| Приоритет: {r.priority:<5}
| Описание: {r.description}
| Время: {r.hours} ч. ({r.minutes} мин.)
| Статус: {r.status:<10} | Исполнитель: {r.executor}
| {"-" * 60} |
""")
                    found = True
                    break

            if not found:
                print(f"\n| ❌ Заявка с ID {search_id} не найдена.")

        except ValueError:
            print("| ⚠ Ошибка! Введите целое число (ID заявки) или '0'.")

def filter_search_requests(requests, urgent):
    while True:
        width = 50
        print(f"""
{"=" * width}
|{"ФИЛЬТР / ПОИСК".center(width - 2)}|
{"=" * width}
|{"1. Показать срочные".center(width - 2)}|
|{"2. Показать по статусу".center(width - 2)}|
|{"3. Показать по категории".center(width - 2)}|
|{"0. Назад в главное меню".center(width - 2)}|
{"=" * width}
""")

        filter_choice = input("| Ваш выбор (0–3) >> ").strip()

        if filter_choice == "0":
            break

        if filter_choice not in ["1", "2", "3"]:
            print("| Неверный выбор. Введите 0–3.")
            continue

        found = False

        # --- СРОЧНЫЕ ---
        if filter_choice == "1":
            print(f"""
{"-" * width}
|{"СРОЧНЫЕ ЗАЯВКИ".center(width - 2)}|
{"-" * width}""")

            for r in requests:
                if r.urgent:
                    print(f"""
| ID: {r.id:<3} 
| Категория: {r.category:<30}
| Статус: {r.status:<10} 
| Описание: {r.description[:40]}
| Срочная: Да
|{"-" * (width - 2)}|""")
                    found = True

            if not found:
                print(f"""
| {"Срочных заявок нет. Можно прокастинировать!".center(width - 2)}
|{"-" * (width - 2)}|""")

        # --- ПО СТАТУСУ ---
        elif filter_choice == "2":
            status_filter = input("\n| Введите статус (Новая, В работе, Выполнена) >> ").lower()
            print(f"""
{"-" * width}
|{"ЗАЯВКИ СО СТАТУСОМ: " + status_filter.upper().center(width - 20)}|
{"-" * width}""")

            for r in requests:
                if status_filter in r.status.lower():
                    print(f"""
| ID: {r.id:<3} 
| Категория: {r.category:<30}
| Статус: {r.status:<10} 
| Описание: {r.description[:40]}
|{"-" * (width - 2)}|""")
                    found = True

            if not found:
                msg = f"Заявок со статусом '{status_filter}' не найдено."
                print(f"""
| {msg.center(width - 2)}
|{"-" * (width - 2)}|""")

        # --- ПО КАТЕГОРИИ ---
        elif filter_choice == "3":
            cat_filter = input("\n| Введите категорию или часть названия >> ").lower()
            print(f"""
{"-" * width}
|{"ЗАЯВКИ ПО КАТЕГОРИИ: " + cat_filter.upper().center(width - 22)}|
{"-" * width}""")

            for r in requests:
                if cat_filter in r.category.lower():
                    print(f"""
| ID: {r.id:<3} 
| Категория: {r.category:<30}
| Статус: {r.status:<10} 
| Описание: {r.description[:40]}
|{"-" * (width - 2)}|""")
                    found = True

            if not found:
                msg = f"Категорий с '{cat_filter}' не найдено."
                print(f"""
| {msg.center(width - 2)}
|{"-" * (width - 2)}|""")

        print(f"\n{'=' * width}\n")

def set_categories(requests):
    used_categories = {req.category for req in requests}

    print("\n| ========== | Используемые категории | ========== |")
    for i, cat in enumerate(sorted(used_categories), start=1):
        print(f"| {i}. {cat}")
    print(f"""
| Всего уникальных категорий: {len(used_categories)}
| {"=" * 48} |""")