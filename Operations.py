from DownloadAndSaveFileData import save_data

def add_requests(now_id, colvo_zayvok, live_zayvki, requests, priorities, categories):
    for r in requests: 
        current_live = int(r.get('live_zayvki', 0)) + 1
        r['live_zayvki'] = current_live
        r['status'] = f"В обороте: {current_live} ход"     
        if current_live > 3: 
            r['status'] = 'Выполнена'  

    save_data(requests)

    now_id += 1
    colvo_zayvok += 1

    print("\n|-----------| Обращение от сотрудника |-----------|")
    applicant = input("| ФИО сотрудника >> ")
    print("|" + "-" * 49 + "|")

    print("\n|---------| Введите номер цеха |---------|")
    while True:
        workshop_raw = input("| Номер цеха >> ")
        if workshop_raw.isdigit() and int(workshop_raw) >= 1:
            workshop = int(workshop_raw)
            print("|" + "-" * 40 + "|")
            break
        else:
            print("| Пожалуйста, введите корректный номер цеха (целое число ≥ 1).")
            print("|" + "-" * 40 + "|")

    print("\n|---------| Выберите приоритет проблемы |---------|")
    for i, prior in enumerate(priorities, 1):
        print(f"| * {i}. {prior}")
    print("|" + "-" * 49 + "|")

    urgent = False

    while True:
        priorit_choice = input("| Введите номер приоритета (1–5) >> ")
        if priorit_choice.isdigit() and 1 <= int(priorit_choice) <= len(priorities):
            priority = priorities[int(priorit_choice) - 1]
            break
        else:
            print("| Пожалуйста, введите число от 1 до 5.")
            print("|" + "-" * 49 + "|")

    print("|" + "-" * 49 + "|")

    if priority == "A": 
        category = categories[3]
        urgent = True
    elif priority == "FBI": 
        category = categories[4]
        urgent = True
    else:
        print("\n|---------| Выберите категорию проблемы |---------|")
        for i, cat in enumerate(categories, 1):
            print(f"| * {i}. {cat}")
        print("|" + "-" * 49 + "|")
        urgent = False
        while True:
            categ_choice = input("| Введите номер категории (1–5) >> ")
            if categ_choice.isdigit() and 1 <= int(categ_choice) <= len(categories):
                category = categories[int(categ_choice) - 1]
                print("|" + "-" * 49 + "|")
                break
            else:
                print("| Пожалуйста, введите число от 1 до 5.")
                print("|" + "-" * 49 + "|")

    description = input("| Описание проблемы >> ")
    print("|" + "-" * 49 + "|")

    print("\n|---------| Выделите время на решение проблемы |---------|")
    while True:
        hours_raw = input("| Оценка времени на решение (в часах) >> ")
        try:
            hours = float(hours_raw)
            if hours > 0: 
                print("|" + "-" * 56 + "|")
                break
            else: print("| Время должно быть больше 0. \n| " + "-" * 56 + " |")

        except ValueError: print("| Пожалуйста, введите корректное число (например, 2.5).\n| " + "-" * 56 + " |")

    minutes = int(hours * 60)
    status = "Новая"

    request = {
        "id": now_id,
        "applicant": applicant,
        "workshop": workshop,
        "category": category,
        "description": description,
        "priority": priority,
        "hours": hours,
        "minutes": minutes,
        "status": status,
        "live_zayvki": live_zayvki,
        "urgent": urgent
    }
    requests.append(request)
    save_data(requests)

    print(f"| ================= ЗАЯВКА СОЗДАНА ================= |")
    print(f"| ID: {now_id}")
    print(f"| Заявитель: {applicant}")
    print(f"| Цех №{workshop}")
    print(f"| Категория: {category}")
    print(f"| Описание: {description}")
    print(f"| Приоритет: {priority}")
    print(f"| Время на решение: {hours} ч. ({minutes} мин.)")
    print(f"| Статус: {status}")
    print("| " + "=" * 50 + " |\n")

    return now_id, colvo_zayvok


def view_all_requests(requests):
    print("\n | Все заявки <-----------------------------|")
    for r in requests:
        print(f"""
| ID:{r.get('id')} заявителя {r.get('applicant')}, от цеха №{r.get('workshop')}.
| * Категория [{r.get('category')}] с приоритетом {r.get('priority')} 
| * Описание проблемы: {r.get('description')}
| * Время на решение: {r.get('hours')} ч. ({r.get('minutes')} мин.)
| * Статус: {r.get('status')}
| {"-" * 50} |
    """)


def statistika_requests(requests):
    total = len(requests)
    urgent_count = sum(1 for r in requests if r.get("urgent", False))

    completed_count = sum(1 for r in requests if str(r.get("status", "")).lower() == "выполнена")
    cat_counts = {}

    for r in requests:
        cat = str(r.get("category", "Неизвестно"))
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    print(f"""
  \t| ============ Статистика ============ |
  \t| ======== Всего заявок: {total} ======== |
  \t| Срочных (urgent): {urgent_count}
  \t| Выполненных: {completed_count}
  \t|
  \t| Распределение по категориям:
  """)
    for cat, count in cat_counts.items(): 
        print(f"    | {cat}: {count} ")

    first_req = requests[0]
    last_req = requests[-1]
    print(f"""
  \t| Первая заявка: ID {first_req.get('id')}, категория '{first_req.get('category')}'|
  \t| Последняя заявка: ID {last_req.get('id')}, категория '{last_req.get('category')}'|
  """)


def delete_id_requests(colvo_zayvok, requests):
    print("\n|-------------|\n| СПИСОК ЗАЯВОК:")
    for number, r in enumerate(requests, start=1):
        print(f"\t| {number}. Заявка №{r.get('id')} ({r.get('category')}) |")

    try: 
        num_to_delete = int(input("\n| Введите №-id заявки из списка для удаления >> "))
    except ValueError: 
        print("| Error #Int! Введите целое число!")
        return colvo_zayvok

    if 1 <= num_to_delete <= len(requests):
        index = num_to_delete - 1
        removed = requests.pop(index)
        colvo_zayvok -= 1
        save_data(requests)
        print(f"\n| Удалено: Заявка №-id {removed.get('id')}, категория: {removed.get('category')}")
    else: print("| Error! Такого номера в списке нет! Пошёл вон!")

    return colvo_zayvok