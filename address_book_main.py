from collections import UserDict
from datetime import datetime
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Address(Field):
    pass

class Phone(Field):
    @staticmethod
    def validate(phone):
        return phone.isdigit() and len(phone) == 10

    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone must contain exactly 10 digits.")
        super().__init__(value)

class Email(Field):
    EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    @staticmethod
    def validate(email):
        return re.match(Email.EMAIL_REGEX, email)

    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Incorrect email format.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Birthday must be in format DD.MM.YYYY")
        super().__init__(date)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.address = None
        self.birthday = None
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def set_email(self, email):
        self.email = Email(email)

    def set_address(self, address):
        self.address = Address(address)

    def set_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def edit_phone(self, old, new):
        for p in self.phones:
            if p.value == old:
                if not Phone.validate(new):
                    raise ValueError("Phone must contain exactly 10 digits.")
                p.value = new
                return
        raise ValueError("Old phone not found.")
    
    def delete_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Phone not found.")
    
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def __str__(self):
        phones = ", ".join(p.value for p in self.phones) if self.phones else "—"
        email = self.email.value if self.email else "—"
        address = self.address.value if self.address else "—"
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "—"

        return (f"Name: {self.name.value}\n"
                f"Phones: {phones}\n"
                f"Email: {email}\n"
                f"Address: {address}\n"
                f"Birthday: {birthday}")

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

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

class Note:
    def __init__(self, text):
        self.text = text
        self.id = None

    def edit(self, new_text):
        self.text = new_text

    def __str__(self):
        return f"[{self.id}] {self.text}"
    
class NotesBook(UserDict):
    def __init__(self):
        super().__init__()
        self.counter = 1

    def add_note(self, text):
        note = Note(text)
        note.id = self.counter
        self.data[self.counter] = note
        self.counter += 1
        return note
    
    def find_notes(self, query):
        query = query.lower()
        return [note for note in self.data.values() if query in note.text.lower()]

if __name__ == "__main__":
    book = AddressBook()

    r = Record("John Doe")
    r.add_phone("0501234567")
    r.set_email("john@example.com")
    r.set_address("Kyiv, Main Street 12")
    r.set_birthday("12.10.1992")

    book.add_record(r)

    print(book.find("John Doe"))
