from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self.validate(value):
            self._value = value
        else:
            raise ValueError(f"Invalid value: {value}")

    def validate(self, value):
        # Реалізуйте валідацію для конкретного поля у підкласах
        return True  # Тимчасова заглушка

class Name(Field):
    def validate(self, value):
        # Перевірка імені, може вимагати спеціфічних умов
        return True  # Тимчасова заглушка

class Phone(Field):
    def validate(self, value):
        # Перевірка номера телефону, наприклад, на формат
        return True  # Тимчасова заглушка

class Birthday(Field):
    def validate(self, value):
        try:
            # Перетворюємо рядок у дату
            value = datetime.strptime(value, "%Y-%m-%d").date()
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        if isinstance(phone, Phone):
            self.phones.append(phone)
        else:
            raise ValueError("Invalid phone format")

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise ValueError("Phone not found in record")

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone
        else:
            raise ValueError("Phone not found in record")

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()
            delta = next_birthday - today
            return delta.days
        else:
            return None

    def __str__(self):
        phone_str = ", ".join([str(phone.value) for phone in self.phones])
        return f"Name: {self.name.value}, Phones: {phone_str}, Birthday: {self.birthday.value if self.birthday else 'N/A'}"

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record):
        if isinstance(record, Record):
            self.data[record.name.value] = record
        else:
            raise ValueError("Invalid record format")

    def find_records(self, criteria):
        found_records = []
        for record in self.data.values():
            if criteria in record.name.value:
                found_records.append(record)
        return found_records

    def iterator(self, n=1):
        items = list(self.data.values())
        for i in range(0, len(items), n):
            yield items[i:i + n]

# Приклад використання:

# Створення адресної книги
address_book = AddressBook()

# Створення записів
record1 = Record("John", birthday="1990-05-15")
phone1 = Phone("123-456-7890")
record1.add_phone(phone1)

record2 = Record("Alice", birthday="1985-10-25")
phone2 = Phone("987-654-3210")
record2.add_phone(phone2)

# Додавання записів до адресної книги
address_book.add_record(record1)
address_book.add_record(record2)

# Пошук записів за іменем
found_records = address_book.find_records("John")
for record in found_records:
    print(record)

# Вивід кількості днів до наступного дня народження
for record in address_book.data.values():
    days = record.days_to_birthday()
    if days is not None:
        print(f"Days to Birthday for {record.name.value}: {days}")
    else:
        print(f"No Birthday information for {record.name.value}")
