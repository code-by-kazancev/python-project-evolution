###########################################################
######                 РИСУЕМ ТАБЛИЦУ              ######   
###########################################################

# Рисует таблицу с полной сеткой и разделителями между строками.
def draw_table(headers, rows, col_widths=None, title=None):
    # Если ширины не указаны — вычисляем автоматически
    if col_widths is None:
        col_widths = []
        for i, header in enumerate(headers):
            max_width = len(header)
            for row in rows:
                if i < len(row):
                    max_width = max(max_width, len(str(row[i])))
            col_widths.append(max_width + 2)  # +2 для отступов

    # Создаём горизонтальную линию-разделитель
    separator = "+" + "+".join(["-" * w for w in col_widths]) + "+"

    # Вычисляем общую ширину таблицы
    total_width = sum(col_widths) + len(col_widths) + 1

    # Рисуем заголовок таблицы (если есть)
    if title:
        print(f"\n{'=' * total_width}")
        print(f"|{title.center(total_width - 2)}|")
        print(f"{'=' * total_width}")

    print(f"\n{separator}")

    # Рисуем заголовки колонок
    header_row = "|" + "|".join([str(h).center(w) for h, w in zip(headers, col_widths)]) + "|"
    print(header_row)
    print(separator)

    # Рисуем данные с разделителями МЕЖДУ КАЖДОЙ СТРОКОЙ
    for row in rows:
        # Если в строке меньше значений, чем колонок — дополняем пустыми
        while len(row) < len(headers):
            row.append("")

        # Обрезаем длинные значения
        cells = []
        for i, (value, width) in enumerate(zip(row, col_widths)):
            cell = str(value)
            if len(cell) > width - 2:
                cell = cell[:width - 2]
            cells.append(cell)

        # Рисуем строку
        row_str = "|" + "|".join([cell.center(w) for cell, w in zip(cells, col_widths)]) + "|"
        print(row_str)

        # Разделитель после каждой строки данных
        print(separator)