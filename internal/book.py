"""
Address book
"""

import datetime
import pickle
from collections import UserDict, UserList


class Field:
    """Class representing a field"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class representing a Name field of the record"""


class Phone(Field):
    """
    Class representing an element Phone 
    of the record phone list
    """

    def __init__(self, value):
        self.__value = None
        super().__init__(value)

    @property
    def value(self):
        """Property of the Phone class."""
        return self.__value

    @value.setter
    def value(self, value: str):
        """Setter for property"""
        if self.is_valid(value):
            self.__value = value
        else:
            raise ValueError("Wrong format of phone number")

    def __eq__(self, another):
        return self.value == another.value

    @staticmethod
    def is_valid(value: str):
        """Validation Phone method"""
        return len(value) == 10 and value.isdigit()


class PhoneList(UserList):
    """ Class representing a Phone list"""
    def __init__(self, data: list):
        super().__init__()
        temp = []
        for phone in data:
            if Phone.is_valid(phone):
                temp.append(phone)
            else:
                raise ValueError(ValueError(f"Wrong format of phone number: '{phone}'"))
        self.data = temp

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, key, value):
        if not Phone.is_valid(value):
            raise ValueError(ValueError(f"Wrong format of phone number: '{value}'"))
        self.data[key] = value


class Birthday():
    """Class represents the birhd day field of the record"""

    date_format = "%d.%m.%Y"

    def __init__(self, value = None):
        self.__value = None
        self.value = value

    @property
    def value(self):
        """Property of the Birthday class"""
        return self.__value

    @value.setter
    def value(self, value = None):
        if value is not None:
            self.__value = datetime.datetime.strptime(value, Birthday.date_format)

    def __str__(self) -> str:
        return self.__value.strftime(Birthday.date_format)


class Record:
    """Class representing a record of address book"""

    def __init__(self, new_name):
        self.__name = None
        self.name = new_name
        self.phones = PhoneList([])
        self.__birthday = None

    @property
    def name(self):
        """Property name."""
        return self.__name

    @name.setter
    def name(self, new_name: str):
        """Setter for property"""
        if isinstance(new_name, str) and len(new_name) > 0:
            self.__name = Name(new_name)

    @property
    def birthday(self):
        """Poroperty Birthday of the record class"""
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday_str):
        self.__birthday = Birthday(birthday_str)

    def add_birhday(self, birthday_str):
        """Add birhday value to record"""
        self.__birthday = Birthday(birthday_str)

    def get_birhday(self):
        """Add birhday value to record"""
        if self.__birthday is not None:
            return self.__birthday.value.strftime(Birthday.date_format)
        else:
            raise ValueError("The record has no birthday value")

    def find_phone(self,  phone: str) -> Phone:
        """Return phone list and return it."""
        for p in self.phones.data:
            if p.value == phone:
                return p

    def add_phone(self, str_phone):
        """Add phone to phone list"""
        new_phone = Phone(str_phone)
        if new_phone in self.phones:
            raise ValueError(f"the number: '{str_phone}' is already exist")
        self.phones.append(new_phone)

    def remove_phone(self, str_phone):
        """Remove phone from phone list"""
        phone = Phone(str_phone)
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        """Edit phone in the phone list."""
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones.data[i] = Phone(new_phone)
                return
            else:
                raise ValueError(f"Contact hasn't such nomer: {old_phone}")

    def __str__(self):
        if self.birthday is not None:
            return (
                f"Contact name: {self.name.value}, "
                f"birthday: {self.birthday},"
                f"phones: {'; '.join(str(p) for p in self.phones)}"
            )
        else:
            return (
                f"Contact name: {self.name.value}, "
                f"phones: {'; '.join(str(p) for p in self.phones)}"
            )


class AddressBook(UserDict):
    """ Class representing an address book. """
    data_file_name = './internal/data.dat'

    @staticmethod
    def new_book():
        """ Initialise the address book. """
        try:
            with open(AddressBook.data_file_name, 'rb') as fs:
                data = pickle.load(fs)
                return AddressBook(data)
        except FileNotFoundError:
            return AddressBook()

    def save_book(self):
        """ Store the address book to file. """
        with open(AddressBook.data_file_name, 'wb') as fs:
            pickle.dump(self, fs)

    def add_record(self, new_record: Record):
        """ AddressBook method that allows to add record"""
        self.data[new_record.name.value] = new_record

    def find(self, search_name: str) -> Record:
        """ Finds the record by name. """
        return self.data.get(search_name)

    def delete(self, search_name: str):
        """ Removes the record by name from the book. """
        if search_name in self.data:
            del self.data[search_name]

    def get_birthdays_per_week(self):
        """ Shows the birthdays for the week rather. """
        temp = []
        for r in self.data.items():
            if r[1].birthday is not None:
                temp.append({'name': r[0], 'birthday': r[1].birthday.value})
        return show_birthdays(temp)


if __name__ == "__main__":
    from service_congratulate import get_birthdays_per_week as show_birthdays

    print("------------Normal tryes------------------------------")
    # Створення нової адресної книги
    book = AddressBook()

    # # Створення запису для John
    john_record = Record("John")
    john_record.add_birhday("02.11.2002")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    print(john_record.birthday)
    print(book.get_birthdays_per_week())
    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")

    # Спроба порушити логікуprint(self.value)
    print("------------Bad tryes------------------------------")
    try:
        john.add_phone("bad-phone-number")
    except ValueError as e:
        print(f"Намагались добавити неправельний номер: {e}")

    try:
        john.phones[0] = "bad-phone-number"
    except ValueError as e:
        print(f"Намагались добавити неправельний номер по індексу: {e}")

    # # Пошук не існуючого номера
    print(john.find_phone("5555555552"))

    try:
        d = Birthday(None)
    except TypeError as e:
        print(f"Неправельний тип для Birthday класу: {e}")

    try:
        d = Birthday("01-01-2001")
    except ValueError as e:
        print(f"Неправельний формат для Birthday класу: {e}")

else:
    from internal.service_congratulate import get_birthdays_per_week as show_birthdays
    