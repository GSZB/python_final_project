from collections import UserDict
from typing import List
import pickle
from pathlib import Path


class Note:
    def __init__(self, text: str, tags: List[str] = None):
        self.text = text
        self.tags = tags or []
        self.id = None

    def edit(self, new_text: str = None, new_tags: List[str] = None):
        if new_text:
            self.text = new_text
        if new_tags is not None:
            self.tags = new_tags

    def __str__(self):
        tags_str = ", ".join(self.tags) if self.tags else "—"
        return f"[{self.id}] {self.text} (tags: {tags_str})"


class NotesBook(UserDict):
    def __init__(self):
        super().__init__()
        self.counter = 1

    def add_note(self, text: str, tags: List[str] = None) -> Note:
        note = Note(text, tags)
        note.id = self.counter
        self.data[self.counter] = note
        self.counter += 1
        return note

    def delete_note(self, note_id: int):
        if note_id in self.data:
            del self.data[note_id]
        else:
            raise KeyError("Note not found")

    def find_by_tag(self, tag: str):
        return [note for note in self.data.values() if tag in note.tags]

    def find_by_keywords(self, keyword: str):
        keyword = keyword.lower()
        return [note for note in self.data.values() if keyword in note.text.lower()]

    def sort_by_tags(self):
        return sorted(self.data.values(), key=lambda n: (n.tags[0] if n.tags else ""))

    def save(self, filename: str = "notesbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.data, f)

    def load(self, filename: str = "notesbook.pkl"):
        if Path(filename).exists():
            with open(filename, "rb") as f:
                self.data = pickle.load(f)
