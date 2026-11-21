def view_id_requests(requests):
  try:
      search_id = int(input(" | Введите номер заявки (ID) для поиска >> "))
      found = False
      for r in requests:
          if r.get("id") == search_id:
              print(f"""\n
| ID:{r.get('id')} заявителя {r.get('applicant')}, от цеха №{r.get('workshop')}
| * Категория [{r.get('category')}] с приоритетом {r.get('priority')}
| * Описание проблемы: {r.get('description')}
| * Время на решение: {r.get('hours')} ч. ({r.get('minutes')} мин.)
| * Статус: {r.get('status')}
| {"-" * 50} |
              """)
              found = True
              break

      if not found: print(f"\n| Заявка с ID {search_id} не найдена. Возвращаемся в меню.\n")

  except ValueError: print("\n| Пожалуйста, введите корректный номер (целое число).\n")


def filter_search_requests(requests, urgent):
  while True:
      print("""
  | --- Фильтр (пункт 6) --- |
  |   1. Показать  срочные   |
  |  2. Показать по статусу  |
  | 3. Показать по категории |
  |  0. Назад в главное меню |
  | --- Фильтр (пункт 6) --- |
      """)
      filter_choice = input("\n | Ваш выбор (0–3) >> ").strip()

      if filter_choice == "0": break

      found = False

      if filter_choice == "1":
          for r in requests:
              if r.get('urgent', False):
                  print(f"""
| ID:{r.get('id')} 
| Категория: {r.get('category')} 
| Статус: {r.get('status')}
| Описание: {str(r.get('description', ''))[:40]}...
| Срочная: Да
                  """)
                  found = True

          if not found: print(" | Радуйся, можно прокастинировать!")

      elif filter_choice == "2":
          status_filter = input(" | Введите статус (например: Новая, В обороте, Выполнена) >> ").lower()
          for r in requests:
              if status_filter in str(r.get('status', '')).lower():
                  print(f"""
| ID:{r.get('id')} 
| Категория: {r.get('category')} 
| Статус: {r.get('status')}
| Описание: {str(r.get('description', ''))[:40]}...
                  """)
                  found = True

          if not found: print(f" | Заявок со статусом, содержащим '{status_filter}', не найдено.")

      elif filter_choice == "3":
          cat_filter = input(" | Введите категорию или часть названия категории >> ").lower()
          for r in requests:
              if cat_filter in str(r.get('category', '')).lower():
                  print(f"""
| ID:{r.get('id')} 
| Категория: {r.get('category')} 
| Статус: {r.get('status')}
| Описание: {str(r.get('description', ''))[:40]}...
                  """)
                  found = True

          if not found: print(f" | Категорий, содержащих '{cat_filter}', не найдено.")

      else: print(" | Неверный выбор. Введите 0–3.")


def set_categories(requests):
  used_categories = {str(req.get("category", "Неизвестно")) for req in requests}

  print("\n| ========== | Используемые  Категории | ========== |")
  for i, cat in enumerate(sorted(used_categories), start=1): 
      print(f"| {i}. {cat}")
  print(f"""| {"-" * 50} |
| Всего уникальных категорий: {len(used_categories)}
| {"-" * 50} |
  """)