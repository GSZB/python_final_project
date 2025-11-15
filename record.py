from typing import List, Optional
from fields import Name, Phone, Email, Address, Birthday


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: List[Phone] = []
        self.email: Optional[Email] = None
        self.address: Optional[Address] = None
        self.birthday: Optional[Birthday] = None

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

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

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
