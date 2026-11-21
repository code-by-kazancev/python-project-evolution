import json, os

DATA_FILE = "data.json"

# --- Функции для работы с JSON ---

def save_data(requests):
    """Сохраняет список заявок в JSON-файл"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(requests, file, ensure_ascii=False, indent=4)
        print("| Данные успешно сохранены в файл.")
    except Exception as e:
        print(f"| Ошибка при сохранении данных: {e}")

def load_data(DATA_FILE):
    """Загружает список заявок из JSON-файла"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                print("| Данные успешно загружены из файла.")
                return data
        except json.JSONDecodeError:
            print("| Ошибка чтения файла. Будет создан новый список.")
            return []
        except Exception as e:
            print(f"| Ошибка чтения файла: {e}. Будет создан новый список.")
            return []
    else:
        print("| Файл данных не найден. Создан новый список.")
        return []