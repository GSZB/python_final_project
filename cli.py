from address_book import AddressBook
from record import Record
from notes import NotesBook


def main():
    book = AddressBook()
    notes = NotesBook()
    book.load()
    notes.load()

    while True:
        command = input("Enter command (add, find, list, add-note, edit-note, delete-note, find-note, find-note-tag, list-notes, exit): ").strip()

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
            tags_input = input("Tags (comma-separated, optional): ").strip()
            tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
            note = notes.add_note(text, tags)
            notes.save()
            print(f"Added note {note.id}")

        elif command == "edit-note":
            try:
                note_id = int(input("Note ID: ").strip())
                if note_id not in notes.data:
                    print("Note not found")
                    continue
                
                current_note = notes.data[note_id]
                print(f"Current note: {current_note}")
                
                new_text = input("New text (leave empty to keep current): ").strip()
                tags_input = input("New tags (comma-separated, leave empty to keep current): ").strip()
                
                new_tags = None
                if tags_input:
                    new_tags = [tag.strip() for tag in tags_input.split(",")]
                
                current_note.edit(new_text if new_text else None, new_tags)
                notes.save()
                print(f"Note {note_id} updated")
            except ValueError:
                print("Invalid note ID")
            except Exception as e:
                print(f"Error: {e}")

        elif command == "delete-note":
            try:
                note_id = int(input("Note ID: ").strip())
                notes.delete_note(note_id)
                notes.save()
                print(f"Note {note_id} deleted")
            except ValueError:
                print("Invalid note ID")
            except KeyError:
                print("Note not found")
            except Exception as e:
                print(f"Error: {e}")

        elif command == "find-note":
            keyword = input("Search keyword: ").strip()
            results = notes.find_by_keywords(keyword)
            if results:
                print(f"Found {len(results)} note(s):")
                for note in results:
                    print(note)
            else:
                print("No notes found")

        elif command == "find-note-tag":
            tag = input("Search by tag: ").strip()
            results = notes.find_by_tag(tag)
            if results:
                print(f"Found {len(results)} note(s) with tag '{tag}':")
                for note in results:
                    print(note)
            else:
                print(f"No notes found with tag '{tag}'")

        elif command == "list-notes":
            if notes.data:
                print("All notes:")
                for note in notes.data.values():
                    print(note)
            else:
                print("No notes yet")

        elif command == "exit":
            print("Goodbye!")
            break

        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()