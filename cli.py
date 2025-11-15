from addressbook import AddressBook
from record import Record
from notes import NotesBook


def main():
    book = AddressBook()
    notes = NotesBook()
    book.load()
    notes.load()

    while True:
        command = input("Enter command (add, find, list, add-note, exit): ").strip()

        if command == "add":
            name = input("Name: ").strip()
            phone = input("Phone: ").strip()
            record = Record(name)
            try:
                record.add_phone(phone)
                book.add_record(record)
                book.save()
                print("Added")
            except Exception as e:
                print(f"Error: {e}")

        elif command == "find":
            query = input("Search query: ").strip()
            res = book.find(query)
            for r in res.values():
                print(r)

        elif command == "list":
            for r in book.data.values():
                print(r)

        elif command == "add-note":
            text = input("Note text: ").strip()
            note = notes.add_note(text)
            notes.save()
            print(f"Added note {note.id}")

        elif command == "exit":
            print("Goodbye!")
            break

        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()