import time

author = "code-by-kazancev"

VERSION = "1.3"
PRODUCT_NAME = "IT-СЕРВИС"
flag = True
requests = []
now_id = 0
categories = [
    "Не работает сетевой принтер",
    "Пропал доступ к базе 1С",
    "Завис сервер учёта продукции",
    "Не подключается рабочий VPN",
    "Сломалась учётная запись",
]
priorities = ["A", "B", "C", "D", "FBI"]

print(f"================== {PRODUCT_NAME} {VERSION} ==================")
print(f"Автор: {author}")

name = input("Введите ваше имя >> ")
print(f"Здравствуйте, {name}!\n")

while flag:
    print("""
        \n|----------| Меню  |--------| 
        \n| 1. Создать заявку  <------|
        \n| 2. Показать все заявки <--|
        \n| 3. Найти заявку по номеру |
        \n| 4. 8.  Выход <------------|
        \n|---------| Меню |----------| 
    \n""")

    user_input = input(f"{name}, выберите одно из перечисленных >> ")

    if user_input == "1":
        now_id += 1
        applicant = input("\n| ФИО сотрудника (заявителя) >> ")

        while True:
            workshop_raw = input("| Номер цеха >> ")
            if workshop_raw.isdigit() and int(workshop_raw) >= 1:
                workshop = int(workshop_raw)
                break
            else:
                print( "| Пожалуйста, введите корректный номер цеха (целое число ≥ 1).\n" )

        print("\n|---------| Выберите приоритет проблемы |---------|")
        for i, prior in enumerate(priorities, 1):
            print(f"| * {i}. {prior}")
        print("|" + "-" * 60 + "|")

        while True:
            priorit_choice = input("Введите номер приоритета (1–5) >> ")
            if priorit_choice.isdigit() and 1 <= int(priorit_choice) <= len(priorities):
                priority = priorities[int(priorit_choice) - 1]
                break
            else:
                print("| Пожалуйста, введите число от 1 до 5.\n")

        # Логика выбора категории      # Для срочных приоритетов автоматически ставим категорию «Не подключается рабочий VPN»
        if priority == "A": category = categories[3]
        elif priority == "FBI": category = categories[5]
        else:
            print("\n|---------| Выберите категорию проблемы |---------|")
            for i, cat in enumerate(categories, 1):
                print(f"| * {i}. {cat}")
            print("|" + "-" * 60 + "|")

            while True:
                categ_choice = input("| Введите номер категории (1–5) >> ")
                if categ_choice.isdigit() and 1 <= int(categ_choice) <= len(categories):
                    category = categories[int(categ_choice) - 1]
                    break
                else:
                    print("| Пожалуйста, введите число от 1 до 5.\n")

        description = input("| Описание проблемы >> ")

        # Оценка времени на решение
        print("\n|---------| Выделите время на решение проблемы |---------|")
        while True:
            hours_raw = input("| Оценка времени на решение (в часах) >> ")
            try:
                hours = float(hours_raw)
                if hours > 0: break
                else: print( "| Время должно быть больше 0.\n" )
            except ValueError:
                print( "| Пожалуйста, введите корректное число (например, 2.5).\n" )

        minutes = int(hours * 60)
        seconds = int(hours * 3600)
        status = "Новая"

        print( f"\nТип workshop: {type(workshop)}" )
        print( f"Тип hours: {type(hours)}" )

        request = {
            "id": now_id,
            "applicant": applicant,
            "workshop": workshop,
            "category": category,
            "description": description,
            "priority": priority,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
            "status": status,
        }
        requests.append(request)

        print("\n|========= ЗАЯВКА СОЗДАНА =========|")
        print(f"| ID: {now_id}")
        print(f"| Заявитель: {applicant}")
        print(f"| Цех №{workshop}")
        print(f"| Категория: {category}")
        print(f"| Описание: {description}")
        print(f"| Приоритет: {priority}")
        print(f"| Время на решение: {hours} ч. ({minutes} мин.)")
        print(f"| Статус: {status}")
        print("|" + "=" * 32 + "|\n")

    elif user_input == "2":
        if not requests:
            print("\n| Нет ни одной заявки.\n")

        else:
            print("\n| Все заявки <-----------------------------|")
            for r in requests:
                print( f"| ID:{r['id']} заявителя {r['applicant']}, от цеха №{r['workshop']}." )
                print( f"| * Категория [{r['category']}] с приоритетом {r['priority']}, статус: {r['status']}" )
                print( f"| * Описание проблемы: {r['description']}" )
                print( f"| * Время на решение: {r['hours']} ч. ({r['minutes']} мин.) " )
                print( "|" + "-" * 60 + "|" )

    elif user_input == "3":
        try:
            search_id = int(input( "Введите номер заявки (ID) для поиска >> " ))
            found = False
            for r in requests:
                if r["id"] == search_id:
                    print( f"\n| ID:{r['id']} заявителя {r['applicant']}, от цеха №{r['workshop']}." )
                    print( f"| * Категория [{r['category']}] с приоритетом {r['priority']}, статус: {r['status']}" )
                    print( f"| * Описание проблемы: {r['description']}" )
                    print( f"| * Время на решение: {r['hours']} ч. ({r['minutes']} мин.) " )
                    print( f"| " + "-" * 60 + "|" )
                    found = True
                    break

            if not found:
                print( f"\n| Заявка с ID {search_id} не найдена. Возвращаемся в меню.\n" )

        except ValueError:
            print("\n| Пожалуйста, введите корректный номер (целое число).\n")

    elif user_input == "4" or user_input == "8":
        print( f"\n| {name}, благодарю вас за использование моей программы..." )
        time.sleep(1)
        print( f"| Проект сделал: {author}" )
        time.sleep(1)
        print( f"| До свидания: {name}!" )
        flag = False

    else:
        print( "| Активирую протокол самоуничтожения: " )
        for i in range(5, 0, -1):
            print( f"| {i}" )
            time.sleep(0.4)
        flag = False

print("================== Конец программы ==================")