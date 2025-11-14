class AddressBook:

    def search(self, query: str):
        query = query.lower()
        result = []

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
