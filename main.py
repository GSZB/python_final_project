import re
from collections import UserDict
from datetime import datetime, timedelta
from pathlib import Path
import pickle


# ==========================
# Поля
# ==========================
class Field:
    """Базовий клас для всіх полів."""
    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Address(Field):
    pass


class Phone(Field):
    """Телефонний номер контакту"""
    PHONE_REGEX = r"^(?:\+?380|0)\d{9}$"  # +380XXXXXXXXX, 380XXXXXXXXX, 0XXXXXXXXX

    @staticmethod
    def validate(phone: str) -> bool:
        return re.match(Phone.PHONE_REGEX, phone) is not None

    def __init__(self, value):
        if not self.validate(value):
            raise ValueError(
                "Phone must be in format +380XXXXXXXXX, 380XXXXXXXXX, or 0XXXXXXXXX."
            )
        super().__init__(value)


class Email(Field):
    EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    @staticmethod
    def validate(email: str) -> bool:
        return re.match(Email.EMAIL_REGEX, email) is not None

    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Incorrect email format.")
        super().__init__(value)


class Birthday(Field):
    """Дата народження контакту у форматі DD.MM.YYYY"""

    def __init__(self, value: str):
        try:
            date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Birthday must be in format DD.MM.YYYY")
        super().__init__(date)


# ==========================
# Запис контакту
# ==========================
class Record:
    """Один контакт у телефонній книзі"""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.address = None
        self.birthday = None

    def add_phone(self, phone: str):
        if any(p.value == phone for p in self.phones):
            raise ValueError("This phone number already exists.")
        self.phones.append(Phone(phone))

    def set_email(self, email: str):
        self.email = Email(email)

    def set_address(self, address: str):
        self.address = Address(address)

    def set_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def edit_phone(self, old: str, new: str):
        for p in self.phones:
            if p.value == old:
                if not Phone.validate(new):
                    raise ValueError(
                        "Phone must be in format +380XXXXXXXXX, 380XXXXXXXXX, or 0XXXXXXXXX."
                    )
                p.value = new
                return
        raise ValueError("Old phone not found.")

    def delete_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Phone not found.")

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones) if self.phones else "—"
        email = self.email.value if self.email else "—"
        address = self.address.value if self.address else "—"
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "—"
        return (
            f"Name: {self.name.value}\n"
            f"Phones: {phones}\n"
            f"Email: {email}\n"
            f"Address: {address}\n"
            f"Birthday: {birthday}"
        )


# ==========================
# Телефонна книга
# ==========================
class AddressBook(UserDict):
    """Телефонна книга користувача"""

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        """Пошук часткового або точного збігу за ім'ям"""
        return {k: v for k, v in self.data.items() if name.lower() in k.lower()}

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Record '{name}' not found.")

    def birthdays_in_days(self, days: int):
        today = datetime.today().date()
        target_date = today + timedelta(days=days)
        result = []

        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value
                next_bday = bday.replace(year=today.year)
                if next_bday < today:
                    next_bday = bday.replace(year=today.year + 1)
                if next_bday == target_date:
                    result.append({
                        "name": record.name.value,
                        "birthday": next_bday.strftime("%d.%m.%Y")
                    })
        return result

    # ======================
    # Збереження та завантаження
    # ======================
    def save(self, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.data, f)

    def load(self, filename="addressbook.pkl"):
        if Path(filename).exists():
            with open(filename, "rb") as f:
                self.data = pickle.load(f)


# ==========================
# Нотатки
# ==========================
class Note:
    """Нотатка користувача"""

    def __init__(self, text: str, tags=None):
        self.text = text
        self.tags = tags or []
        self.id = None

    def edit(self, new_text=None, new_tags=None):
        if new_text:
            self.text = new_text
        if new_tags is not None:
            self.tags = new_tags

    def __str__(self):
        tags_str = ", ".join(self.tags) if self.tags else "—"
        return f"[{self.id}] {self.text} (tags: {tags_str})"


class NotesBook(UserDict):
    """Збірка нотаток користувача"""

    def __init__(self):
        super().__init__()
        self.counter = 1

    def add_note(self, text: str, tags=None) -> Note:
        note = Note(text, tags)
        note.id = self.counter
        self.data[self.counter] = note
        self.counter += 1
        return note

    def delete_note(self, note_id: int):
        if note_id in self.data:
            del self.data[note_id]
        else:
            raise KeyError("Note not found")

    def find_by_tag(self, tag: str):
        return [note for note in self.data.values() if tag in note.tags]

    def find_by_keywords(self, keyword: str):
        keyword = keyword.lower()
        return [note for note in self.data.values() if keyword in note.text.lower()]

    def sort_by_tags(self):
        return sorted(self.data.values(), key=lambda note: (note.tags[0] if note.tags else ""))

    # ======================
    # Збереження та завантаження
    # ======================
    def save(self, filename="notesbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.data, f)

    def load(self, filename="notesbook.pkl"):
        if Path(filename).exists():
            with open(filename, "rb") as f:
                self.data = pickle.load(f)