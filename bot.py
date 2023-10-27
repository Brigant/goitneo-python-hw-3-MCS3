"""
Module providing a service for bot assistan.
This bot can store the contact in RAM using command "add [name] [phone]". 
There is a possibilyty to change existen user using command "change [name] [phone]". 
You can show a number of specified user by the command "phone [name]" and you can see all 
contacs using command "all".
"""

import shlex
import internal.book as book



def input_error(func):
    """The function handle the user inputs error"""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Caught the ValueError exception: {e}"
        except KeyError as e:
            return f"Caught the KeyError exception: {e}"
        except IndexError as e:
            return f"Caught the IndexError exception: {e}"
        except AttributeError as e:
            return f"Caught the AttributeError exception: {e}"

    return inner


def parse_input(user_input):
    """The function parse user input and return command and arguments"""
    lexer = shlex.shlex(user_input, posix=True)
    lexer.quotes = "'"
    lexer.whitespace_split = True
    cmd, *args = list(lexer)

    return cmd, *args


@input_error
def add_contact(args, a_book: book.AddressBook):
    """
    The function add new contact to the contacts list.
    Use 'add <name> <phone>' command.
    """

    if len(args) != 2:
        raise ValueError("Input please: 'add <name> <phone>")
    name, phone = args

    contact = a_book.find(name)
    if contact is None :
        contact = book.Record(name)
        a_book.add_record(contact)
    contact.add_phone(phone)

    return "Contact added."


@input_error
def change_contact(args, a_book: book.AddressBook):
    """
    The function change existen contact.
    Use 'change <name> <old_phone> <new_phone>'.
    """

    if len(args) != 3:
        raise ValueError("Input please: 'change <name> <old_phone> <new_phone>")
    name, old_phone, new_phone = args
    print(name, old_phone, new_phone)
    contact = a_book.find(name)
    contact.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, a_book: book.AddressBook):
    """
    The function shows all phone numbers of the contact.
    Use 'phone <contact_name>'.
    """

    if len(args) == 1:
        name = args[0]
    else:
        raise ValueError("Input please: 'phone <contact_name>'")

    return  a_book.find(name)


@input_error
def show_all(a_book: book.AddressBook):
    """
    The function show all contacts.
    Use 'all' command.
    """
    for record in a_book.items():
        print(record[1])


@input_error
def add_birthday(args, a_book: book.AddressBook):
    """
    The function adds borthday to the contac.
    Use 'add-birthday <contact name> <DD.MM.YYYY>'.
    """
    if len(args) != 2:
        raise ValueError("Input please: 'add-birthday <contact name> <DD.MM.YYYY>'")
    name, str_date = args
    contact = a_book.find(name)
    if not contact:
        raise ValueError("Contact not found")
    contact.add_birhday(str_date)

    return  "Contact got the birthday date"

@input_error
def show_birthday(args, a_book: book.AddressBook):
    """
    The function adds borthday to the contac.
    Use 'show-birthday <contact name>'.
    """
    if len(args) != 1:
        raise ValueError("Input please: 'show-birthday <contact name>'")
    name, = args
    contact = a_book.find(name)
    if not contact:
        raise ValueError("Contact not found")

    return  contact.get_birhday()

@input_error
def birthdays(a_book: book.AddressBook):
    """
    The function returns the next birthdays for a week from since.
    It grouping it by weekday. Days off are excluded for result.
    Use 'birthdays'.
    """
    a_book.get_birthdays_per_week()

@input_error
def show_info():
    """
    Show help info.
    """
    print(
"""
________________________! Important !___________________________________
You can use single quotes to specify full name: 'Jhon Snow'

Commone usage <command> <other_args>
input -> add <'name secondname'> <phone>: Add a new contact with name and phone number.
input -> change <'name'> <old_phone> <new phone>: Change the phone number
         for the specified contact.
input -> phone <'name'>: Show the phone number for the specified contact.
input -> all: Show all contacts in the address book.
input -> add-birthday <'name'> <birthday>: Add a birthday for the specified contact.
input -> show-birthday <'name'>: Show birthday for the specified contact.
input -> birthdays: Show birthdays that will occur in the next week.
input -> hello: Receive a greeting from the bot.
input -> close or exit: Close the program.
"""
    )


def main():
    """The main function"""
    a_book = book.AddressBook().new_book()

    print("""
    |-------------------------------------------|
    |      Welcome to the assistant bot!        |
    |      To see all command enter ? or help.  |
    |-------------------------------------------|
          """)
    while True:
        user_input = input("Enter a command: ") 
        if len(user_input)>0:
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                a_book.save_book()
                print("Good bye!")
                break

            if command == "hello":
                print("How can I help you?")

            elif command == "save":
                a_book.save_book()
                print('book saved')

            elif command == "add":
                print(add_contact(args, a_book))

            elif command == "change":
                print(change_contact(args, a_book))

            elif command == "phone":
                print(show_phone(args, a_book))

            elif command == "all":
                show_all(a_book)

            elif command == "add-birthday" or command == "ab":
                print(add_birthday(args, a_book))

            elif command == "show-birthday" or command == "sb":
                print(show_birthday(args, a_book))

            elif command == "birthdays" or command == "b":
                birthdays(a_book)

            elif command in ["?", "help"]:
                show_info()


            else:
                print("Invalid command.")
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
