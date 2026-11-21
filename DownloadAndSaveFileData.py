import json, os
from models import Request, User, request_from_dict

DATA_FILE = "data.json"
USERS_FILE = "users.json"


def save_data(requests):
    # Сохраняет список заявок в JSON-файл.
    # Утиная типизация: если объект умеет to_dict, превращаем его.
    data_to_save = []
    for item in requests:
        if hasattr(item, "to_dict"):
            data_to_save.append(item.to_dict())
        else:
            data_to_save.append(item)

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, ensure_ascii=False, indent=4)
        print("| Данные успешно сохранены в файл.")
    except Exception as e:
        print(f"| Ошибка при сохранении данных: {e}")


def save_users(users):
    # Сохраняет список пользователей в JSON.
    data_to_save = []
    for item in users:
         
        if hasattr(item, "to_dict"):
            data_to_save.append(item.to_dict())
        else:
            data_to_save.append(item)

    try:
        with open(USERS_FILE, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, ensure_ascii=False, indent=4)
        print("| Пользователи сохранены.")
    except Exception as e:
        print(f"| Ошибка при сохранении пользователей: {e}")


def load_data(filename, object_class=None):
    # Загружает данные из JSON.
    # Если передан object_class, превращает словари в объекты.
    # Для иерархии Request автоматически использует фабрику request_from_dict.
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            if object_class and isinstance(data, list):
                # Проверяем, является ли класс частью иерархии Request
                if hasattr(object_class, "request_type"):
                    # Используем фабричную функцию для восстановления правильного типа
                    return [request_from_dict(item) for item in data]
                else:
                    # Для User и других классов используем их from_dict
                    return [object_class.from_dict(item) for item in data]

            return data
        
        except json.JSONDecodeError:
            print(f"| Ошибка чтения файла {filename}. Будет создан новый список.")
            return []
        
        except Exception as e:
            print(f"| Ошибка чтения файла {filename}: {e}. Будет создан новый список.")
            return []
    else:
        return []