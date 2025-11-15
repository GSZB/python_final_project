# python_final_project: PythonNoobs
Simple address book and notes manager.
**Team: PythonNoobs**
Alexandra Bond - Dev
Mykyta Malevanets - Dev
Gönczy Szabolcs - Team Lead
Oleh Shtembuliak - Dev

## Structure

- fields.py
- record.py
- addressbook.py
- notes.py
- storage.py
- cli.py

## Installation and Usage

1. Ensure you have Python 3.8+ installed.
2. Run the following commands:

python cli.py add “John Jackson” “+380501234567”
python cli.py find John
python cli.py list
python cli.py add-note “Buy milk”

Презентація коду: Телефонна книга та нотатки

Основна ідея
Цей код реалізує дві основні функціональні системи:

Телефонна книга (AddressBook)

Зберігає контакти з іменами, телефонами, email, адресою та датою народження.

Нотатки (NotesBook)

Зберігає нотатки з тегами.

Підтримує пошук за тегами або ключовими словами.

Обидві системи підтримують збереження та завантаження даних з файлу за допомогою pickle.

Структура коду
Код поділено на блоки:

Базові класи для полів: Field

Класи для конкретних полів: Name, Phone, Email, Address, Birthday

Клас запису контакту: Record

Клас телефонної книги: AddressBook

Класи нотаток: Note, NotesBook

Базові поля
Клас Field

class Field: def init(self, value): self.value = value def str(self): return str(self.value)

Базовий клас для всіх даних: імені, телефону, email, адреси, дня народження.

Всі інші класи наслідують його: Name, Phone, Email, Address, Birthday.

Особливості полів:

Phone: перевірка на 10 цифр

Email: перевірка формату через регулярний вираз

Birthday: рядок у форматі DD.MM.YYYY → datetime.date

Клас Record – контакт class Record: def init(self, name: str): self.name = Name(name) self.phones = [] self.email = None self.address = None self.birthday = None
Особливості контакту:

Ім’я (Name)

Список телефонів (Phone)

Email (Email)

Адреса (Address)

День народження (Birthday)

Методи:

add_phone(phone) – додати телефон

edit_phone(old, new) – редагувати телефон

delete_phone(phone) – видалити телефон

set_email(email) – додати або змінити email

set_address(address) – додати або змінити адресу

set_birthday(birthday) – додати день народження

Клас AddressBook – телефонна книга class AddressBook(UserDict): def add_record(self, record: Record): self.data[record.name.value] = record
Особливості:

Наслідує UserDict → працює як словник {ім'я: Record}

Методи:

find(name) – знайти контакт

delete(name) – видалити контакт

birthdays_in_days(days) – список контактів, у яких день народження через days днів

save(file) / load(file) – збереження та завантаження через pickle

Класи нотаток 6.1. Note class Note: def init(self, text: str, tags=None): self.text = text self.tags = tags or [] self.id = None
Кожна нотатка має: текст, список тегів, унікальний ID

Методи:

edit(new_text, new_tags) – змінює текст або теги

6.2. NotesBook class NotesBook(UserDict): def add_note(self, text, tags=None) -> Note: ...

Контейнер для нотаток → словник {id: Note}

Методи:

delete_note(note_id) – видалити нотатку за ID

find_by_tag(tag) – пошук нотаток за тегом

find_by_keywords(keyword) – пошук за текстом

sort_by_tags() – сортування нотаток по першому тегу

Валідація даних
Phone: тільки 10 цифр

Email: перевірка через регулярний вираз

Birthday: формат DD.MM.YYYY

Це гарантує, що користувач не зможе додати некоректні дані.

Збереження та завантаження
Використовується модуль pickle

Приклад:

ab.save("my_addressbook.pkl") ab.load("my_addressbook.pkl")

nb.save("my_notes.pkl") nb.load("my_notes.pkl")

Приклад використання
Створення контакту:

rec = Record("Ivan Ivanov") rec.add_phone("0501234567") rec.set_email("ivan@example.com") rec.set_birthday("15.11.1990")

Додавання у телефонну книгу:

ab = AddressBook() ab.add_record(rec)

Створення нотатки:

nb = NotesBook() nb.add_note("Buy milk", tags=["shopping", "urgent"])

Переваги та можливості
Модульність – кожне поле окремий клас

Легке розширення – можна додати нові типи полів

Валідація даних – неможливо ввести неправильний email або телефон

Пошук та сортування – по тегах, ключових словах і днях народження

Збереження та завантаження – зручно для зберігання даних
