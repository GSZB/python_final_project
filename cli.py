from address_book import AddressBook
from record import Record
from notes import NotesBook
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

COMMANDS = [
    "help", "menu",
    "add", "add-email", "add-address", "add-birthday",
    "edit-contact", "delete-contact",
    "find", "search-contacts", "birthdays",
    "list",
    "add-note", "edit-note", "delete-note",
    "find-note", "find-note-tag", "search-notes", "sort-notes-by-tags",
    "list-notes",
    "exit",
]


def show_help():
    print("""
Available commands:
  CONTACTS:
    add                — add new contact
    add-email          — add email to contact
    add-address        — add address to contact
    add-birthday       — add birthday (DD.MM.YYYY)
    edit-contact       — edit name/address/email
    delete-contact     — remove contact
    find               — find contact by name
    search-contacts    — search by any field
    birthdays          — show birthdays in N days
    list               — list all contacts

  NOTES:
    add-note           — add a new note
    edit-note          — edit existing note
    delete-note        — delete note
    find-note          — find note by keyword
    find-note-tag      — search note by tag
    search-notes       — search in notes
    sort-notes-by-tags — show notes sorted by tags
    list-notes         — list all notes

  SYSTEM:
    help               — show this help
    menu               — show commands list
    exit               — exit program
""")


def show_menu():
    print("Commands:")
    for cmd in COMMANDS:
        print(" •", cmd)


def main():
    book = AddressBook()
    notes = NotesBook()
    book.load()
    notes.load()

    command_completer = WordCompleter(COMMANDS, ignore_case=True, sentence=True)

    print("Welcome to AddressBook! Type 'help' to see available commands.")

    while True:
        command = prompt("Command: ", completer=command_completer).strip()

        if command == "help":
            show_help()

        elif command == "menu":
            show_menu()

        elif command == "add":
            name = input("Name: ").strip()
            phone = input("Phone: ").strip()
            try:
                record = Record(name)
                record.add_phone(phone)
                book.add_record(record)
                book.save()
                print("Contact added")
            except Exception as e:
                print(f"Error: {e}")

        elif command == "add-email":
            name = input("Contact name: ").strip()
            email = input("Email: ").strip()
            try:
                record = book.data.get(name)
                if not record:
                    print("Contact not found")
                    continue
                record.set_email(email)
                book.save()
                print("Email added")
            except Exception as e:
                print(f"Error: {e}")

        elif command == "add-address":
            name = input("Contact name: ").strip()
            address = input("Address: ").strip()
            record = book.data.get(name)
            if record:
                record.set_address(address)
                book.save()
                print("Address added")
            else:
                print("Contact not found")

        elif command == "add-birthday":
            name = input("Contact name: ").strip()
            birthday = input("Birthday (DD.MM.YYYY): ").strip()
            try:
                record = book.data.get(name)
                if not record:
                    print("Contact not found")
                    continue
                record.set_birthday(birthday)
                book.save()
                print("Birthday added")
            except Exception as e:
                print(f"Error: {e}")

        elif command == "edit-contact":
            name = input("Old name: ").strip()
            new_name = input("New name (optional): ").strip() or None
            new_email = input("New email (optional): ").strip() or None
            new_address = input("New address (optional): ").strip() or None
            try:
                book.update_record(name, new_name, new_address, new_email)
                book.save()
                print("Contact updated")
            except Exception as e:
                print(f"Error: {e}")

        elif command == "delete-contact":
            name = input("Name: ").strip()
            try:
                book.delete(name)
                book.save()
                print("Contact deleted")
            except KeyError:
                print("Contact not found")

        elif command == "find":
            query = input("Search name: ").strip()
            res = book.find(query)
            for r in res.values(): print(r)

        elif command == "search-contacts":
            query = input("Search anything: ").strip()
            res = book.search(query)
            for r in res: print(r)

        elif command == "birthdays":
            try:
                days = int(input("Days ahead: ").strip())
                res = book.birthdays_in_days(days)
                if res:
                    for b in res: print(f"{b['name']} — {b['birthday']}")
                else:
                    print("No birthdays in this range")
            except ValueError:
                print("Invalid number")

        elif command == "list":
            for r in book.data.values(): print(r)

        # NOTES
        elif command == "add-note":
            text = input("Text: ").strip()
            tags = input("Tags (comma separated): ").strip()
            tags = [t.strip() for t in tags.split(',')] if tags else []
            note = notes.add_note(text, tags)
            notes.save()
            print(f"Added note {note.id}")

        elif command == "edit-note":
            try:
                note_id = int(input("Note ID: ").strip())
                note = notes.data.get(note_id)
                if not note:
                    print("Note not found")
                    continue
                new_text = input("New text: ").strip() or None
                tags_input = input("New tags (optional): ").strip()
                new_tags = [t.strip() for t in tags_input.split(',')] if tags_input else None
                note.edit(new_text, new_tags)
                notes.save()
                print("Note updated")
            except ValueError:
                print("Invalid ID")
            except Exception as e:
                print(f"Error: {e}")

        elif command == "delete-note":
            try:
                note_id = int(input("Note ID: ").strip())
                notes.delete_note(note_id)
                notes.save()
                print("Note deleted")
            except ValueError:
                print("Invalid note ID")
            except KeyError:
                print("Note not found")
            except Exception as e:
                print(f"Error: {e}")

        elif command == "find-note":
            keyword = input("Keyword: ").strip()
            for note in notes.find_by_keywords(keyword): print(note)

        elif command == "find-note-tag":
            tag = input("Tag: ").strip()
            for note in notes.find_by_tag(tag): print(note)

        elif command == "search-notes":
            keyword = input("Keyword: ").strip()
            for note in notes.find_by_keywords(keyword): print(note)

        elif command == "sort-notes-by-tags":
            for note in notes.sort_by_tags(): print(note)

        elif command == "list-notes":
            for note in notes.data.values(): print(note)

        elif command == "exit":
            print("Goodbye!")
            break

        else:
            print("Unknown command. Type 'help'.")


if __name__ == "__main__":
    main()
