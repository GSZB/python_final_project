import re


class Contact:
    """
    Клас представляє один контакт з ім'ям, телефоном та електронною поштою.
    """

    def __init__(self, name: str, phone: str | None = None, email: str | None = None):
        """
        Ініціалізує об'єкт контакту.

        :param name: Ім'я контакту (обов'язкове поле).
        :param phone: Номер телефону у форматі +380XXXXXXXXX або None.
        :param email: Адреса електронної пошти або None.
        """
        self.name = name
        self.phone = phone
        self.email = email


def validate_phone(phone: str) -> bool:
    """
    Перевіряє, чи номер телефону відповідає формату українського мобільного
    номера: +380XXXXXXXXX, де X - цифра.

    Приклади коректних номерів:
    +380501234567
    +380663184455

    :param phone: Рядок з номером телефону.
    :return: True, якщо номер коректний, інакше False.
    """
    pattern = r"^\+380\d{9}$"
    return re.fullmatch(pattern, phone) is not None


def validate_email(email: str) -> bool:
    """
    Перевіряє, чи рядок схожий на коректну адресу електронної пошти.

    Просте правило:
    - має бути одна '@'
    - перед та після '@' мають бути символи (не пробіли)
    - має бути крапка в домені, наприклад: example@gmail.com

    :param email: Рядок з електронною поштою.
    :return: True, якщо email має коректний формат, інакше False.
    """
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.fullmatch(pattern, email) is not None


def create_contact() -> Contact | None:
    """
    Створює новий контакт, запитуючи дані в користувача через консоль.

    Під час введення номера телефону та email:
    - якщо формат некоректний, користувач отримує повідомлення про помилку;
    - контакт не буде створений, доки дані не будуть виправлені
      або поле не буде залишено порожнім (для необов'язкових полів).

    :return: Об'єкт Contact, якщо контакт успішно створений,
             або None, якщо створення було перервано.
    """
    print("=== Створення нового контакту ===")
    name = input("Введіть ім'я (обов'язково): ").strip()
    if not name:
        print("Ім'я не може бути порожнім. Контакт не створено.")
        return None

    phone = input("Введіть номер телефону у форматі +380XXXXXXXXX (необов'язково): ").strip()
    if phone:
        if not validate_phone(phone):
            print("Помилка: номер телефону некоректний. Контакт не створено.")
            return None

    email = input("Введіть email (необов'язково): ").strip()
    if email:
        if not validate_email(email):
            print("Помилка: email некоректний. Контакт не створено.")
            return None

    contact = Contact(name=name, phone=phone or None, email=email or None)
    print("Контакт успішно створено.")
    print(f"Ім'я: {contact.name}, телефон: {contact.phone}, email: {contact.email}")
    return contact


def edit_contact(contact: Contact) -> None:
    """
    Редагує існуючий контакт. Дозволяє змінювати телефон та email
    з перевіркою коректності введених даних.

    Користувач може:
    - натиснути Enter, щоб залишити поточне значення;
    - ввести нове значення, яке буде перевірене;
    - у разі некоректного формату зміни не будуть збережені.

    :param contact: Об'єкт Contact, який потрібно відредагувати.
    :return: Нічого не повертає. Змінює об'єкт contact за посиланням.
    """
    print(f"=== Редагування контакту: {contact.name} ===")
    print("Натисніть Enter, щоб залишити поле без змін.\n")

    # Редагування номера телефону
    new_phone = input(f"Новий телефон (поточний: {contact.phone or 'немає'}): ").strip()
    if new_phone:
        if not validate_phone(new_phone):
            print("Помилка: номер телефону некоректний. Зміни номера не збережені.")
        else:
            contact.phone = new_phone

    # Редагування email
    new_email = input(f"Новий email (поточний: {contact.email or 'немає'}): ").strip()
    if new_email:
        if not validate_email(new_email):
            print("Помилка: email некоректний. Зміни email не збережені.")
        else:
            contact.email = new_email

    print("Поточні дані контакту:")
    print(f"Ім'я: {contact.name}, телефон: {contact.phone}, email: {contact.email}")


if __name__ == "__main__":
    # Невелика демо-перевірка Task3
    c = create_contact()
    if c:
        print("\nТепер протестуємо редагування контакту.\n")
        edit_contact(c)
