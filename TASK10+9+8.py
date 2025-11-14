"""
Рішення для Task10: теги, пошук та сортування

Підтримує редагування тексту і тегів одночасно.

Має видалення нотаток.

Пошук не тільки по тегах, а й по тексту.

Сортування нотаток за тегами.
Код покриває функціонал редагування та видалення нотаток:

Редагування тексту і тегів — через Note.edit().

Видалення нотаток — через NotesBook.delete_note(id).

Оновлення для клас Note, додаємо теги:
"""
class Note:
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags or []   # список тегів
        self.id = None

    def edit(self, new_text=None, new_tags=None):
        if new_text:
            self.text = new_text
        if new_tags is not None:
            self.tags = new_tags

    def __str__(self):
        tags_str = ", ".join(self.tags) if self.tags else "—"
        return f"[{self.id}] {self.text} (tags: {tags_str})"

  """
  Оновлення для NOTESBOOK:
  додавання нотаток із тегами
  пошук за тегами
  сортування за тегами
  пошук за текстом
  
  """

class NotesBook(UserDict):
    def __init__(self):
        super().__init__()
        self.counter = 1

    def add_note(self, text, tags=None):
        note = Note(text, tags)
        note.id = self.counter
        self.data[self.counter] = note
        self.counter += 1
        return note

    def delete_note(self, note_id):
        if note_id in self.data:
            del self.data[note_id]
        else:
            raise KeyError("Note not found")

    def find_by_tag(self, tag):
        """Має повернути список нотаток, які містять тег."""
        return [note for note in self.data.values() if tag in note.tags]

    def find_by_keywords(self, keyword):
        """ Для пошуку по тексту нотатки """
        keyword = keyword.lower()
        return [note for note in self.data.values() if keyword in note.text.lower()]

    def sort_by_tags(self):
        """Має повертати список нотаток, відсортований за алфавітом тегів."""
        return sorted(self.data.values(), key=lambda note: (note.tags[0] if note.tags else ""))


  
