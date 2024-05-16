from datetime import datetime

class Field:
    pass

class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be a 10-digit number.")
        self.value = value

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, value):
        self.phones.append(Phone(value))

    def add_birthday(self, value):
        self.birthday = Birthday(value)

class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_record(self, record):
        self.contacts.append(record)

    def find(self, name):
        for contact in self.contacts:
            if contact.name.value.lower() == name.lower():
                return contact
        return None

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {e}"
    return wrapper

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
        message += f" Phone number: {phone}"  # Додайте номер телефону до повідомлення
    return message

@input_error
def change_contact(args, book: AddressBook):
    if len(args) != 2:
        return "Invalid command. Please use 'change [name] [new_phone]'."

    name, new_phone = args
    record = book.find(name)
    if record:
        record.phones = []  # Очищаємо старі номери телефонів
        record.add_phone(new_phone)
        return f"Phone number changed for {name}."
    else:
        return f"Contact {name} not found."

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record and record.phones:
        return f"{name}'s phone number is: {', '.join([phone.value for phone in record.phones])}"
    elif record:
        return f"{name} doesn't have a phone number set."
    else:
        return f"Contact {name} not found."

@input_error
def show_all_contacts(book: AddressBook):
    if book.contacts:
        contact_info = []
        for contact in book.contacts:
            if contact.phones:
                phones = ', '.join([phone.value for phone in contact.phones])
                contact_info.append(f"{contact.name.value}: {phones}")
            else:
                contact_info.append(contact.name.value)
        return "\n".join(contact_info)
    else:
        return "Address book is empty."

@input_error
def add_birthday(args, book: AddressBook):
    name, date, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return f"Birthday added for {name}."
    else:
        return f"Contact {name} not found."

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is: {record.birthday.value.strftime('%d.%m.%Y')}"
    elif record:
        return f"{name} doesn't have a birthday set."
    else:
        return f"Contact {name} not found."

@input_error
def birthdays(book: AddressBook):
    all_birthdays = []
    for contact in book.contacts:
        if contact.birthday:
            all_birthdays.append(f"{contact.name.value}: {contact.birthday.value.strftime('%d.%m.%Y')}")
    if all_birthdays:
        return "\n".join(all_birthdays)
    else:
        return "No birthdays found."

def hello():
    return "Hello! How can I help you?"

def close():
    return "Goodbye!"

def exit():
    return "Goodbye!"

def parse_input(user_input):
    return user_input.split()

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            print("You didn't enter any command.")
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

