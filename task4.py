class Contact:

    def __init__(self, name: str, phone: str | None = None, email: str | None = None):
        self.name = name
        self.phone = phone
        self.email = email


class AddressBook:
    def __init__(self):
        self.contacts: list[Contact] = []

    def search(self, query: str) -> list[Contact]:
        """
        Здійснює пошук серед контактів книги.

        Пошук виконується за ім'ям, номером телефону або email.
        Пошук нечутливий до регістру.

        :param query: Рядок для пошуку.
        :return: Список знайдених контактів.
        """
        query = query.lower()
        results: list[Contact] = []

        for contact in self.contacts:
            if (
                    query in contact.name.lower()
                    or (contact.phone and query in contact.phone.lower())
                    or (contact.email and query in contact.email.lower())
            ):
                results.append(contact)

        return results
