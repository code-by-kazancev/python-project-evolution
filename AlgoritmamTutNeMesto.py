def linear_search(requests, query):
    # Линейный поиск по всем заявкам
    results = []
    checks = 0
    query = query.strip().lower()

    if not query:
        return results, checks

    for request in requests:
        checks += 1
        category = request.category.lower()
        description = request.description.lower()
        if query in category or query in description:
            results.append(request)

    return results, checks


def find_first(requests, query):
    # Поиск первого совпадения
    checks = 0
    query = query.strip().lower()

    if not query:
        return None, checks

    for request in requests:
        checks += 1
        category = request.category.lower()
        description = request.description.lower()
        if query in category or query in description:
            return request, checks

    return None, checks


def sort_by_category(requests):
    # Сортировка по категории (текстовое поле)
    return sorted(requests, key=lambda req: req.category.lower())


def sort_by_hours(requests):
    # Сортировка по времени в часах (числовое поле)
    return sorted(requests, key=lambda req: req.hours, reverse=True)


def bubble_sort_hours(requests):
    # Пузырьковая сортировка по времени (часы)
    result = requests.copy()
    comparisons = 0
    swaps = 0
    n = len(result)

    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            comparisons += 1
            # Если левый элемент меньше правого — меняем местами
            if result[j].hours < result[j + 1].hours:
                result[j], result[j + 1] = result[j + 1], result[j]
                swaps += 1
                swapped = True
        # Если за проход не было перестановок — список уже отсортирован
        if not swapped:
            break

    return result, comparisons, swaps