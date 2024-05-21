from datetime import datetime, date, timedelta

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
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
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
            phones = ', '.join([phone.value for phone in contact.phones])
            contact_info.append(f"{contact.name.value}: {phones}")
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

def string_to_date(date_string):
    return datetime.strptime(date_string, "%d.%m.%Y").date()

def date_to_string(date):
    return date.strftime("%d.%m.%Y")

def prepare_user_list(user_data):
    prepared_list = []
    for user in user_data:
        prepared_list.append({"name": user["name"], "birthday": user["birthday"]})
    return prepared_list

def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)

def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)
    return birthday

def get_upcoming_birthdays(users, days=7):
    upcoming_birthdays = []
    today = date.today()

    for user in users:
        birthday_this_year = user["birthday"].replace(year=today.year)


        if birthday_this_year < today:
            birthday_this_year = user["birthday"].replace(year=today.year + 1)


        birthday_this_year = adjust_for_weekend(birthday_this_year)


        if today <= birthday_this_year <= today + timedelta(days=days):
            congratulation_date_str = date_to_string(birthday_this_year)
            upcoming_birthdays.append({"name": user["name"], "congratulation_date": congratulation_date_str})
    return upcoming_birthdays

@input_error
def birthdays(book: AddressBook):
    all_contacts = prepare_user_list([{"name": contact.name.value, "birthday": contact.birthday.value} for contact in book.contacts if contact.birthday])
    upcoming_birthdays = get_upcoming_birthdays(all_contacts)
    if upcoming_birthdays:
        return "\n".join([f"{user['name']}'s birthday is on {user['congratulation_date']}" for user in upcoming_birthdays])
    else:
        return "No upcoming birthdays within the next week."

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
