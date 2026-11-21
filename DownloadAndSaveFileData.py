import json, os

DATA_FILE = "data.json"
USERS_FILE = "users.json"

def save_data(data_list):
    # Сохраняет список объектов (Request или User) в JSON
    # Утиная типизация: если объект умеет to_dict, превращаем его
    data_to_save = [item.to_dict() if hasattr(item, "to_dict") else item for item in data_list]

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, ensure_ascii=False, indent=4)
        print("| Данные успешно сохранены в файл.")
    except Exception as e:
        print(f"| Ошибка при сохранении данных: {e}")

def save_users(users_list):
    # Сохраняет список пользователей в JSON
    data_to_save = [item.to_dict() if hasattr(item, "to_dict") else item for item in users_list]

    try:
        with open(USERS_FILE, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, ensure_ascii=False, indent=4)
        print("| Пользователи сохранены.")
    except Exception as e:
        print(f"| Ошибка при сохранении пользователей: {e}")

def load_data(filename, object_class=None):
    # Если передан object_class (например, Request или User), превращает словари в объекты.
    if os.path.exists(filename):
        
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            if object_class and isinstance(data, list):
                # Превращаем каждый словарь в объект нужного класса
                return [object_class.from_dict(item) for item in data]
            return data
        
        except json.JSONDecodeError:
            print(f"| Ошибка чтения файла {filename}. Будет создан новый список.")
            return []
        
        except Exception as e:
            print(f"| Ошибка чтения файла {filename}: {e}. Будет создан новый список.")
            return []
            
    else: return []