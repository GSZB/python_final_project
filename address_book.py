import pickle
from collections import UserDict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
from record import Record
from fields import Name, Address, Email


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Dict[str, Record]:
        return {k: v for k, v in self.data.items() if name.lower() in k.lower()}

    def search(self, query: str) -> List[Record]:
        query = query.lower()
        result: List[Record] = []
        for record in self.data.values():
            if query in record.name.value.lower():
                result.append(record)
                continue
            if any(query in phone.value for phone in record.phones):
                result.append(record)
                continue
            if record.email and query in record.email.value.lower():
                result.append(record)
                continue
        return result

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Record '{name}' not found.")

    def update_record(self, name: str, new_name: str = None, new_address: str = None,
                      new_email: str = None) -> Record:
        record = self.data.get(name)
        if not record:
            raise KeyError("Contact not found.")
        if new_name:
            self.data[new_name] = self.data.pop(name)
            record.name = Name(new_name)
        if new_address:
            record.address = Address(new_address)
        if new_email:
            if not Email.validate(new_email):
                raise ValueError("Incorrect email format.")
            record.email = Email(new_email)
        return record

    def birthdays_in_days(self, days: int) -> List[dict]:
        today = datetime.today().date()
        target_date = today + timedelta(days=days)
        result: List[dict] = []

        for record in self.data.values():
            if not record.birthday:
                continue

            bday = record.birthday.value  
            next_bday = bday.replace(year=today.year)

            if next_bday < today:
                next_bday = bday.replace(year=today.year + 1)

            if today <= next_bday <= target_date:
                result.append({
                    "name": record.name.value,
                    "birthday": next_bday.strftime("%d.%m.%Y")
                })

        return result

    def save(self, filename: str = "addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.data, f)

    def load(self, filename: str = "addressbook.pkl"):
        if Path(filename).exists():
            with open(filename, "rb") as f:
                self.data = pickle.load(f)
