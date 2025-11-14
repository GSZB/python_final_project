class Phone(Field):
    @staticmethod
    def validate(phone):
        return phone.isdigit() and len(phone) == 10

    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone must contain exactly 10 digits.")
        super().__init__(value)


class Email(Field):
    EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    @staticmethod
    def validate(email):
        return re.match(Email.EMAIL_REGEX, email)

    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Incorrect email format.")
        super().__init__(value)
