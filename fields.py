import re
from datetime import datetime


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
    PHONE_REGEX = r"^(?:\+?380|0)\d{9}$"

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
    def __init__(self, value: str):
        try:
            date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Birthday must be in format DD.MM.YYYY")
        super().__init__(date)
