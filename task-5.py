class AddressBook(UserDict):

    # Модуль видалення
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    # Модуль оновлення iнформації
    def update_record(self, name, new_name=None, new_address=None, new_email=None):
        record = self.find(name)
        if not record:
            raise KeyError("Contact not found.")

        if new_name:
            self.data[new_name] = self.data.pop(name)
            record.name = Name(new_name)

        if new_address:
            record.address = new_address

        if new_email:
            if "@" not in new_email or "." not in new_email:
                raise ValueError("Invalid email format.")
            record.email = new_email

        return record


class Record:
    def __init__(self, name, address=None, email=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = address
        self.email = email

    # Редагування адреси та пошти
    def edit_address(self, new_address):
        self.address = new_address

    def edit_email(self, new_email):
        if "@" not in new_email or "." not in new_email:
            raise ValueError("Invalid email format.")
        self.email = new_email
