class Request:
    # Допустимые значения (константы класса)
    ALLOWED_STATUSES = ("Новая", "В работе", "Выполнена")
    ALLOWED_PRIORITIES = ("A", "B", "C", "D", "FBI")
    URGENT_PRIORITIES = ("A", "FBI")

    PRIORITY_NAMES = {
        "A": "Высокий",
        "B": "Средний",
        "C": "Низкий",
        "D": "Минимальный",
        "FBI": "Критический",
    }

    def __init__(
        self,
        id: int,                     # уникальный идентификатор заявки
        applicant: str,              # ФИО заявителя
        workshop: int,               # номер цеха
        category: str,               # категория проблемы
        description: str,            # описание проблемы
        priority: str,               # приоритет (A/B/C/D/FBI) 
        hours: float,                # оценка времени в часах
        minutes: int,                # оценка времени в минутах
        status: str = "Новая",        # статус заявки
        live_zayvki: int = 1,        # счётчик "жизни" заявки
        urgent: bool = False,        # флаг срочности
        executor: str = "Не назначен", # исполнитель заявки
    ):
        # Валидация при создании
        if priority not in self.ALLOWED_PRIORITIES:
            raise ValueError(
                f"Недопустимый приоритет: {priority}. "
                f"Допустимые: {self.ALLOWED_PRIORITIES}"
            )
        if status not in self.ALLOWED_STATUSES:
            raise ValueError(
                f"Недопустимый статус: {status}. "
                f"Допустимые: {self.ALLOWED_STATUSES}"
            )
        if hours <= 0:
            raise ValueError("Время на решение должно быть больше 0.")

        self.id = id
        self.applicant = applicant
        self.workshop = workshop
        self.category = category
        self.description = description
        self.priority = priority
        self.hours = hours
        self.minutes = minutes
        self.status = status
        self.live_zayvki = live_zayvki
        self.urgent = urgent
        self.executor = executor

    # --- Методы изменения состояния --- #

    def change_status(self, new_status: str) -> bool:
        # Изменяет статус заявки.
        if new_status not in self.ALLOWED_STATUSES:
            return False
        self.status = new_status
        return True

    def change_priority(self, new_priority: str) -> bool:
        # Изменяет приоритет заявки и автоматически пересчитывает срочность.
        if new_priority not in self.ALLOWED_PRIORITIES:
            return False
        self.priority = new_priority
        self.urgent = new_priority in self.URGENT_PRIORITIES
        return True

    def assign_executor(self, executor_name: str) -> bool:
        # Назначает исполнителя на заявку.
        if not executor_name or not isinstance(executor_name, str):
            return False
        self.executor = executor_name.strip()
        return True

    def close(self, executor_name: str = "Неизвестно") -> bool:
        # Закрывает заявку (переводит в статус 'Выполнена').
        if self.status != "В работе":
            return False
        self.status = "Выполнена"
        self.executor = executor_name
        return True

    # --- Вычисляемые свойства --- #

    def get_priority_name(self) -> str:
        # Возвращает текстовое название приоритета.
        return self.PRIORITY_NAMES.get(self.priority, "Неизвестный")

    def get_short_info(self) -> str:
        # Краткое описание заявки для вывода в списках.
        return (
            f"ID: {self.id:<3} | {self.category:<30} | "
            f"Приоритет: {self.priority:<5} | Статус: {self.status}"
        )

    # --- Сериализация --- #

    def to_dict(self) -> dict:
        # Преобразует объект в словарь для сохранения в JSON.
        return {
            "id": self.id,
            "applicant": self.applicant,
            "workshop": self.workshop,
            "category": self.category,
            "description": self.description,
            "priority": self.priority,
            "hours": self.hours,
            "minutes": self.minutes,
            "status": self.status,
            "live_zayvki": self.live_zayvki,
            "urgent": self.urgent,
            "executor": self.executor,
        }

    @classmethod # classmethod — вызывается как Request.from_dict(data).
    def from_dict(cls, data: dict) -> "Request":
        # Создаёт объект Request из словаря (при загрузке из JSON).
        return cls(
            id=data.get("id", 0),
            applicant=data.get("applicant", ""),
            workshop=data.get("workshop", 0),
            category=data.get("category", ""),
            description=data.get("description", ""),
            priority=data.get("priority", "D"),
            hours=float(data.get("hours", 0.0)),
            minutes=int(data.get("minutes", 0)),
            status=data.get("status", "Новая"),
            live_zayvki=data.get("live_zayvki", 1),
            urgent=data.get("urgent", False),
            executor=data.get("executor", "Не назначен"),
        )

    # --- Магические методы (для отладки и сравнения) ---
    def __repr__(self) -> str:
        # Строковое представление объекта для разработчика.
        return (
            f"Request(id={self.id}, applicant='{self.applicant}', "
            f"category='{self.category}', priority='{self.priority}', "
            f"status='{self.status}')"
        )

    def __eq__(self, other) -> bool:
        # Сравнение двух заявок по ID (уникальный ключ).
        if not isinstance(other, Request):
            return NotImplemented
        return self.id == other.id

    def __lt__(self, other) -> bool:
        #Сравнение по приоритету (для сортировки).
        #Позволяет использовать sorted() без lambda в простых случаях.
        if not isinstance(other, Request):
            return NotImplemented
        priority_order = {"FBI": 0, "A": 1, "B": 2, "C": 3, "D": 4}
        return priority_order.get(self.priority, 99) < priority_order.get( other.priority, 99 )

class User: # Пользователь системы (Сотрудник или IT-специалист).
    
    ALLOWED_ROLES = ("employee", "it_specialist")

    def __init__(self, login: str, name: str, role: str, workshop: int, password: str = ""):
        if role not in self.ALLOWED_ROLES:
            raise ValueError(f"Недопустимая роль: {role}. Допустимые: {self.ALLOWED_ROLES}")

        self.login = login
        self.name = name
        self.role = role
        self.workshop = workshop
        self.password = password

    def check_password(self, input_password: str) -> bool:
        # Проверяет введенный пароль. Инкапсуляция логики проверки.
        return self.password == input_password

    def to_dict(self) -> dict:
        return {
            "login": self.login,
            "name": self.name,
            "role": self.role,
            "workshop": self.workshop,
            "password": self.password
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            login=data.get("login", ""),
            name=data.get("name", ""),
            role=data.get("role", "employee"),
            workshop=data.get("workshop", 0),
            password=data.get("password", "")
        )

    def __repr__(self) -> str:
        return f"User(login='{self.login}', name='{self.name}', role='{self.role}')"