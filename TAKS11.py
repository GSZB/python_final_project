"""
COMMANDS — словник, де ключі це внутрішні команди, а значення — список ключових слів, що можуть зустрітися в тексті користувача.

guess_command(user_input) — аналізує введений текст і повертає команду з найбільшою кількістю збігів.

Використовуємо prompt_toolkit.PromptSession для  CLI з підтримкою редагування рядка.

Якщо не знайдено збігів — пропонуємо "help".
"""






from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

# Словник команд і ключових слів
COMMANDS = {
    "add_note": ["додати", "нову нотатку", "записати", "створити"],
    "delete_note": ["видалити", "стерти", "прибрати"],
    "edit_note": ["редагувати", "змінити", "оновити"],
    "find_by_tag": ["тег", "ключове слово", "знайти по тегу"],
    "find_by_keyword": ["знайти", "пошук", "keyword"],
    "show_notes": ["показати", "всі нотатки", "список нотаток"],
    "exit": ["вихід", "закрити", "exit", "quit"]
}

def guess_command(user_input):
    user_input = user_input.lower()
    scores = {cmd:0 for cmd in COMMANDS}
    
    for cmd, keywords in COMMANDS.items():
        for kw in keywords:
            if kw in user_input:
                scores[cmd] += 1
    
    # Найбільший рахунок
    best_cmd = max(scores, key=scores.get)
    
    # Якщо жодне ключове слово не знайдено, пропонуємо help
    if scores[best_cmd] == 0:
        return "help"
    return best_cmd

# CLI сесія
session = PromptSession()
while True:
    user_input = session.prompt("Введіть команду або текст: ")
    cmd = guess_command(user_input)




""" або розширена версія 

Аналіз введеного тексту і пропонує найближчу команду.

Працює з NotesBook (додавати, редагувати, видаляти нотатки).

Підтримує пошук по тегам і тексту.

Має команду exit для виходу.


"""

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

class Note:
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags or []
        self.id = None

    def edit(self, new_text=None, new_tags=None):
        if new_text:
            self.text = new_text
        if new_tags is not None:
            self.tags = new_tags

    def __str__(self):
        tags_str = ", ".join(self.tags) if self.tags else "—"
        return f"[{self.id}] {self.text} (tags: {tags_str})"

from collections import UserDict

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
        return [note for note in self.data.values() if tag in note.tags]

    def find_by_keywords(self, keyword):
        keyword = keyword.lower()
        return [note for note in self.data.values() if keyword in note.text.lower()]

    def show_notes(self):
        return list(self.data.values())

# 
# CLI бот
# 

COMMANDS = {
    "add_note": ["додати", "нову нотатку", "записати", "створити"],
    "delete_note": ["видалити", "стерти", "прибрати"],
    "edit_note": ["редагувати", "змінити", "оновити"],
    "find_by_tag": ["тег", "ключове слово", "знайти по тегу"],
    "find_by_keyword": ["знайти", "пошук", "keyword", "текст"],
    "show_notes": ["показати", "всі нотатки", "список нотаток"],
    "exit": ["вихід", "закрити", "exit", "quit"]
}

def guess_command(user_input):
    user_input = user_input.lower()
    scores = {cmd:0 for cmd in COMMANDS}
    
    for cmd, keywords in COMMANDS.items():
        for kw in keywords:
            if kw in user_input:
                scores[cmd] += 1
    
    best_cmd = max(scores, key=scores.get)
    if scores[best_cmd] == 0:
        return "help"
    return best_cmd

# ----------------------------
# Інтерактивна сесія
# ----------------------------

book = NotesBook()
session = PromptSession()

print("Ласкаво просимо в NotesBot! Введіть команду або текст (exit для виходу).")

while True:
    user_input = session.prompt(">>> ")
    cmd = guess_command(user_input)
    
    if cmd == "exit":
        print("До побачення!")
        break
    
    elif cmd == "help":
        print("Не зрозумів. Спробуйте: додати, редагувати, видалити, знайти, показати, вихід")
    
    elif cmd == "add_note":
        text = session.prompt("Текст нотатки: ")
        tags = session.prompt("Теги (через кому, якщо є): ").split(",")
        tags = [t.strip() for t in tags if t.strip()]
        note = book.add_note(text, tags)
        print(f"Додано нотатку: {note}")
    
    elif cmd == "show_notes":
        notes = book.show_notes()
        if notes:
            for note in notes:
                print(note)
        else:
            print("Нотаток ще немає.")
    
    elif cmd == "delete_note":
        try:
            note_id = int(session.prompt("ID нотатки для видалення: "))
            book.delete_note(note_id)
            print(f"Нотатку {note_id} видалено.")
        except (ValueError, KeyError):
            print("Невірний ID нотатки.")
    
    elif cmd == "edit_note":
        try:
            note_id = int(session.prompt("ID нотатки для редагування: "))
            note = book.data.get(note_id)
            if not note:
                print("Нотатку не знайдено.")
                continue
            new_text = session.prompt(f"Новий текст (залиште порожнім щоб не змінювати): ")
            new_tags = session.prompt(f"Нові теги (через кому, залиште порожнім щоб не змінювати): ")
            new_tags_list = [t.strip() for t in new_tags.split(",") if t.strip()] if new_tags else None
            note.edit(new_text if new_text else None, new_tags_list)
            print(f"Оновлено: {note}")
        except ValueError:
            print("Невірний ID нотатки.")
    
    elif cmd == "find_by_tag":
        tag = session.prompt("Введіть тег для пошуку: ")
        results = book.find_by_tag(tag.strip())
        if results:
            for note in results:
                print(note)
        else:
            print("Нотаток з таким тегом немає.")
    
    elif cmd == "find_by_keyword":
        keyword = session.prompt("Введіть слово для пошуку у тексті: ")
        results = book.find_by_keywords(keyword.strip())
        if results:
            for note in results:
                print(note)
        else:
            print("Нотаток з таким словом немає.")

    
    print(f"Пропонована команда: {cmd}")
    
    if cmd == "exit":
        break
