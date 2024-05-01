"""Module providing a function """

import os
import re
import pickle
import shutil
from abc import ABC, abstractmethod
from collections import UserDict
from datetime import datetime
from dateutil.parser import parse


class Field:
    """Class representing a default class"""
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """Class representing a Name"""

class Phone(Field):
    """Class representing a Phone"""

    @property
    def value(self):
        """Getter"""
        return self.__value

    @value.setter
    def value(self, value):
        """Setter"""
        if len(str(value)) != 10:
            raise Exception ("The number does not have 10 digits")
        elif not value.isdigit():
            raise Exception ("There are extra characters in the number")
        else:
            self.__value = value

class Address(Field):
    """Class representing a Address """

    @property
    def value(self):
        """Getter"""
        return self.__value

    @value.setter
    def value(self, value):
        """Setter"""
        self.__value = value

class Email(Field):
    """Class representing a Email """

    @property
    def value(self):
        """Getter"""
        return self.__value

    @value.setter
    def value(self, value):
        """Setter"""
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if (re.fullmatch(regex, value)):
            self.__value = value
        else:
            raise Exception("Invalid Email")

class Birthday(Field):
    """Class representing a Birthday """

    @property
    def valid_birthday(self):
        """Getter"""
        return self.__value

    @valid_birthday.setter
    def valid_birthday(self,value):
        """Setter"""
        correct = datetime.strptime(value, '%d.%m.%Y')
        if correct:
            self.__value = correct
        else:
            raise ValueError ("The date is incorrect")

class Record:
    """Class representing a Record"""

    def __init__(self, name):

        self.name = Name(name)
        self.phones = []
        self.birthday = " "
        self.address = []
        self.email = []
        self.note = " "
        self.tags = []

    def add_teg(self, tags):
        """Function add teg"""
        self.tags.append(tags)

    def add_note(self,value):
        """Function add note"""
        self.note = " ".join(value)

    def delete_note(self):
        """Function delete note"""
        self.note = " "

    def edit_note(self, value):
        """Function edit note"""
        self.delete_note()
        self.add_note(value)

    def add_phone(self,value):
        """function for adding phones"""
        self.phones.append(Phone(value))

    def add_address(self, value):
        """function for adding phones"""
        self.address.append(Address(" ".join(value)))

    def add_email(self, value):
        """function for adding phones"""
        self.email.append(Email(value))

    def add_birthday(self, value):
        """function for adding phones"""
        self.birthday = Birthday(value)

    def remove_phone(self,value):
        """function for remove phones"""
        if self.find_phone(value):
            self.phones.remove(self.find_phone(value))
        else:
            raise ValueError()

    def edit_phone(self, value, value_two):
        """function for edit phones"""
        if self.find_phone(value):
            self.remove_phone(value)
            self.add_phone(value_two)
        else:
            raise ValueError()

    def find_phone(self, value):
        """function for find phones"""
        for phone in self.phones:
            if str(phone) == str(value):
                return phone

    def remove_address(self, value):
        """function for remove address"""
        if self.find_address(value):
            self.address.remove(self.find_address(value))
        else:
            raise ValueError()

    def find_address(self, value):
        """function for find address"""
        for address in self.address:
            if str(address) == str(value):
                return address

    def remove_email(self, value):
        """function for remove email"""
        if self.find_email(value):
            self.email.remove(self.find_email(value))
        else:
            raise ValueError()

    def find_email(self, value):
        """function for find email"""
        for email in self.email:
            if str(email) == str(value):
                return email

    def remove_birthday(self):
        """function for remove birthday"""
        self.birthday = ' '

    def __str__(self):
        return (f"Contact name: {self.name.value}\
                \t-phones: {'; '.join(p.value for p in self.phones)}\
                \t-email: {'; '.join(p.value for p in self.email)}\
                \t-address: {'; '.join(p.value for p in self.address)} \
                \t-birthday: {self.birthday}\
                \t-note: {self.note}\
                \t-tags: {self.tags}\n")

    def days_to_birthday(self)->int:
        birthday = self.birthday.value
        current_date = datetime.now().date()
        birthday_date_this_year = (parse(birthday, fuzzy=False).
                                   replace(year = datetime.now().year).date())
        delta = birthday_date_this_year - current_date
        if delta.days>0:
            return delta.days
        else:
            return (birthday_date_this_year.replace(year=current_date.year+1) - current_date).days

class AddressBook(UserDict):
    """Class representing a AddressBook"""

    def add_record(self,Record):
        """function for add record"""
        return super().__setitem__(Record.name.value,Record)

    def find(self,Name):
        """function for find record"""
        for key in self.data:
            if str(key) == str(Name):
                return super().__getitem__(key)
        raise NameError("Contact does not exist, enter the name of an existing contact")

    def delete(self,Name):
        """function for delete record"""
        return super().__delitem__(Name)

    def iterator(self, value):
        """Iterator"""
        for contact in self.data.values():
            names = str(contact.name)
            if names.find(value) != -1:
                yield f"{contact} have word <{value}>"

            for phone in contact.phones:
                contact_phone = str(phone)
                if contact_phone.find(value) != -1:
                    yield f"{contact} have word <{value}>"

    def find_note(self, value):
        """Function find note"""
        for contact in self.data.values():
            note = str(contact.note)
            if note.find(value) != -1:
                yield f"{contact} have note <{note}>"

    def search_notes_by_tag(self, tags):
        """Function search tags"""
        for contact in self.data.values():
            for tag in contact.tags:
                if tags in tag:
                    yield f"{contact} have note <{tags}>"


class UserInterface(ABC):
    """Abstract base class for user interfaces"""

    @abstractmethod
    def display_message(self, message):
        pass

    @abstractmethod
    def display_contact(self, contact):
        pass

    @abstractmethod
    def get_user_input(self):
        pass

class ConsoleInterface(UserInterface):
    """Concrete implementation of user interface for console"""

    def display_message(self, message):
        print(message)

    def display_contact(self, contact):
        print(contact)

    def get_user_input(self):
        return input("Enter the command: ").lower().strip()



def decorator(func):
    """Decorator"""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            return "Enter the correct command"
        except ValueError:
            return "Enter correct command"
        except IndexError:
            return "Enter the correct command, name and phone number"
        except NameError as e:
            return f"{e}"
        except FileNotFoundError:
            global book
            book = AddressBook()
            with open('Data.bin', 'wb') as file:
                pickle.dump(book, file)
                return "Create Data"
        except Exception as e:
            return f"{e}"
    return wrapper

@decorator
def start():
    """Load data"""
    with open('Data.bin', 'rb') as file:
        global book
        book = pickle.load(file)
    return "Bot started"

def save():
    """Save data"""
    global book
    with open('Data.bin', 'wb') as file:
        pickle.dump(book, file)

def command_hello():
    """Function Hello"""
    return "How can I help you?"

def command_add_record(name,phone):
    """Adding a contact to the Address Book"""
    new_record = Record(name)
    new_record.add_phone(phone)
    book.add_record(new_record)
    return "Contact added successfully"

def command_find_record(value):
    """Find a contact in the Address Book"""
    for i in book.iterator(value):
        print(i)

def command_delete_record(name):
    """Deleting a contact in the Address Book"""
    if book.find(name):
        book.delete(name)
        return f"Contact {name} deleted"

def command_update_phone(name,phone):
    """Adding a phone number"""
    if book.find(name):
        new_phone = book.find(name)
        new_phone.add_phone(phone)
        return new_phone

def command_remove_phone(name, phone):
    """Deleting a phone number"""
    if book.find(name):
        record = book.find(name)
        record.remove_phone(phone)
        return record

def command_edit_phone(name,phone_one,phone_two):
    """Changing the phone number"""
    if book.find(name):
        record = book.find(name)
        record.edit_phone(phone_one,phone_two)
        return record

def command_show_all():
    """Function show all phone number"""
    for contact in book.values():
        print(f'{contact}')

def command_add_note(name,note):
    """Function add note"""
    if book.find(name):
        record = book.find(name)
        record.add_note(note)
        return "Note added successfully"

def command_delete_note(name):
    """Function delete note"""
    record = book.find(name)
    if record:
        record.delete_note()
        return "Note delete"

def command_edit_note(name,note):
    """Function edit note"""
    record = book.find(name)
    if record:
        record.edit_note(note)
        return "Note edit"

def command_find_note(value):
    """Function find note"""
    for i in book.find_note(value):
        print(i)

def command_good_bye():
    """Function close bot"""
    global ACTIVE_BOT
    ACTIVE_BOT = False
    return "Good Bye!"

def get_command(command):
    """Function command bot"""
    return command_list[command]

def command_add_address(name, address):
    """Adding a address"""
    if book.find(name):
        new_address = book.find(name)
        new_address.add_address(address)
        return "Address added successfully"

def command_add_email(name, email):
    """Adding a email"""
    if book.find(name):
        new_email = book.find(name)
        new_email.add_email(email)
        return "Email added successfully"

def command_add_birthday(name, birthday):
    """Adding a birthday"""
    if book.find(name):
        new_birthday = book.find(name)
        new_birthday.add_birthday(birthday)
        return "Birthday added successfully"

def command_show_birthday(days: int):
    """Show birthday"""
    cnt = 0
    for contact in book.values():
        if contact.days_to_birthday() - int(days) == 0:
            print(f'{contact}')
            cnt += 1
    if cnt > 0:
        return f"Contacts that have birthday in {days} days are printed above"
    else:
        return f"There are no contacts that have birthdays in {days} days in the AddressBook"


def command_help_info():
    """Help information"""
    return """Commands list:\n
        *hello - prints greeting \n
        *add <contact name> <phone number>- adds record if contact name is not present, adds phone if contact name is present and phone number differs from other \n
        *update <contact name> <old phone> <new phone>- changes contact phone by name \n
        *delete <contact name>- delete contact or delete \n
        *remove <contact name> <phone> - delete specified phone for the contact \n        
        *show all - prints entire Address Book \n
        *find <name or phone> - filter by name letters or phone number \n
        *exit, good bye, close - saves changes to database and exit \n
        *add-address <name, address> - adds address for the contact with specified name \n
        *add-email <name, email> - adds email for the specified contact \n
        *add-birthday <name, borthday> - adds birthday for the specified contact \n
        *write <name, note> - adds note for the contact with specified name \n
        *delete-note <name, note> - removes note for the contact with specified name \n
        *edit-note <name, note> - edit note \n
        *find-note <note> - find contact with specified note \n
        *show-birthdate <number of days> - shows all contacts wich have birthday on a date that will occure in specified number of days \n
        *sort <folder path> - sorts the files in the specified folder\n
        *add-tag <name, tag> - adds a tag to the specified contact\n
        *find-tag <tag> - searches for contacts by the specified tags\n"""

def command_remove_address(name, address):
    """Deleting a address"""
    if book.find(name):
        record = book.find(name)
        record.remove_address(address)
        return 'Address deleting'

def command_remove_email(name, email):
    """Deleting a email"""
    if book.find(name):
        record = book.find(name)
        record.remove_email(email)
        return 'Email deleting'

def command_remove_birthday(name):
    """Deleting a birthday"""
    if book.find(name):
        record = book.find(name)
        record.remove_birthday()
        return 'Birthda deleting'

def sort_files_by_category(folder_path):
    """Function sort files by category"""
    if not os.path.exists(folder_path):
        return "The path does not exist."

    categories = {
        'image': ['.jpg', '.jpeg', '.png', '.gif'],
        'video': ['.mp4', '.avi', '.mkv'],
        'documents': ['.pdf', '.doc', '.docx', '.txt'],
        'other': []  
    }

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            _, file_extension = os.path.splitext(file_name)
            found_category = False
            for category, extensions in categories.items():
                if file_extension.lower() in extensions:
                    found_category = True
                    category_folder = os.path.join(folder_path, category)
                    if not os.path.exists(category_folder):
                        os.makedirs(category_folder)
                    shutil.move(file_path, os.path.join(category_folder, file_name))
                    break
            if not found_category:
                other_folder = os.path.join(folder_path, 'інше')
                if not os.path.exists(other_folder):
                    os.makedirs(other_folder)
                shutil.move(file_path, os.path.join(other_folder, file_name))

    return "Sorting is complete!"

def command_add_teg(name, tags):
    """Adding a tags"""
    if book.find(name):
        new_tags = book.find(name)
        new_tags.add_teg(tags)
        return "Tags added successfully"
    
def command_find_teg(value):
    """Function find teg"""
    for i in book.search_notes_by_tag(value):
        print(i)

command_list = {
        "hello": command_hello,
        "help": command_help_info,
        "add": command_add_record,
        "find": command_find_record,
        "delete": command_delete_record,

        "update" : command_update_phone,
        "remove": command_remove_phone,
        "edit": command_edit_phone,

        "show all": command_show_all,
        "good bye": command_good_bye,
        "show-birthdate": command_show_birthday,
        "close": command_good_bye,
        "exit": command_good_bye,

        "add-address": command_add_address,
        "add-email": command_add_email,
        "add-birthday": command_add_birthday,

        "remove-address": command_remove_address,
        "remove-email": command_remove_email,
        "remove-birthday": command_remove_birthday,

        "write": command_add_note,
        "delete-note": command_delete_note,
        "edit-note": command_edit_note,
        "find-note": command_find_note,

        "sort": sort_files_by_category,
        "add-tag": command_add_teg,
        "find-tag": command_find_teg,
    }

ACTIVE_BOT = False
book = None

@decorator
def command_parser(user_input, user_interface):
    """Сommand parser"""
    if user_input in ["show all", "hello", "good bye", "close", "exit", "help"]:
        return get_command(user_input)()
    else:
        user_input = user_input.split()
        if user_input[0] in ["phone", "delete", "find", "delete-note", "find-note",
                             "show-birthdate", "remove-birthday", "sort","find-tag",]:
            return get_command(user_input[0])(user_input[1])
        elif user_input[0] in ["remove", "update", "add", "add-email", "add-birthday",
                               "remove-address", "remove-email", "add-tag"]:
            return get_command(user_input[0])(user_input[1],(user_input[2]))
        elif user_input[0] in ["write","add-address", "edit-note"]:

            return get_command(user_input[0])(user_input[1],(user_input[2:]))
        elif user_input[0] in ["edit"]:
            return get_command(user_input[0])(user_input[1],(user_input[2]),(user_input[3]))
        else:
            raise ValueError()

def main():
    """Bot"""
    user_interface = ConsoleInterface()  # Create instance of console interface
    print(start())
    global ACTIVE_BOT
    ACTIVE_BOT = True
    while ACTIVE_BOT:
        user_input = user_interface.get_user_input()
        user_interface.display_message(command_parser(user_input, user_interface))
        print("____________________________________")
        save()


if __name__ == '__main__':
    main()

#The file ends
