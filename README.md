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

Файли address_book.py, fields.py, record.py, notes.py містять відповідні класи. main.py — запускає інтерактивну консоль.

2. Встановлення

Клонувати або скопіювати проект на локальний комп’ютер.

Створити віртуальне середовище (рекомендовано для ізоляції залежностей):

python -m venv venv


Активувати віртуальне середовище:

Windows:

venv\Scripts\activate


macOS/Linux:

source venv/bin/activate


Встановити залежності з requirements.txt:

pip install -r requirements.txt

3. Файл requirements.txt

Для твого проекту необхідна тільки бібліотека prompt_toolkit для інтерактивного CLI:

prompt_toolkit>=3.0.39


Інші бібліотеки (pickle, pathlib, datetime, re) входять в стандартну бібліотеку Python.

4. Запуск програми

У терміналі, перебуваючи в папці з main.py:

python main.py


Після запуску з’явиться підказка:

Welcome to AddressBook! Type 'help' to see available commands.
Command:

5. Інтерактивне використання
Додавання контактів
Command: add
Name: Ivan Ivanov
Phone: +380501234567
Contact added

Додавання email
Command: add-email
Contact name: Ivan Ivanov
Email: ivan@example.com
Email added

Додавання адреси
Command: add-address
Contact name: Ivan Ivanov
Address: Kyiv, Ukraine
Address added

Додавання дня народження
Command: add-birthday
Contact name: Ivan Ivanov
Birthday (DD.MM.YYYY): 15.12.1990
Birthday added

Редагування контакту
Command: edit-contact
Old name: Ivan Ivanov
New name (optional): Ivan Petrov
New email (optional): ivan.petrov@example.com
New address (optional): Lviv, Ukraine
Contact updated

Видалення контакту
Command: delete-contact
Name: Ivan Petrov
Contact deleted

Пошук контактів

За іменем:

Command: find
Search name: Ivan
Name: Ivan Ivanov
Phones: +380501234567
Email: ivan@example.com
Address: Kyiv, Ukraine
Birthday: 15.12.1990


За будь-яким полем:

Command: search-contacts
Search anything: Kyiv

Перегляд днів народжень
Command: birthdays
Days ahead: 7
Ivan Ivanov — 15.12.1990

Список контактів
Command: list

Робота з нотатками

Додавання нотатки:

Command: add-note
Text: Buy milk
Tags (comma separated): shopping,home
Added note 1


Редагування нотатки:

Command: edit-note
Note ID: 1
New text: Buy milk and bread
New tags (optional): shopping,urgent
Note updated


Пошук нотатки по тегу:

Command: find-note-tag
Tag: urgent
[1] Buy milk and bread (tags: shopping, urgent)


Вивід всіх нотаток:

Command: list-notes
[1] Buy milk and bread (tags: shopping, urgent)


Видалення нотатки:

Command: delete-note
Note ID: 1
Note deleted

6. Збереження даних

Контакти та нотатки автоматично зберігаються у файли addressbook.pkl та notesbook.pkl після кожної зміни. При наступному запуску програми вони завантажуються автоматично.






