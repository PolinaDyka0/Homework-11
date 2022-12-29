from collections import UserDict
from datetime import date, datetime
import re


class AddressBook(UserDict):
    def __init__(self, data={}):
        self.data = data
        self.index = 0
        self.__iterator = None

    def __repr__(self):
        return '\n'.join(str(record) for record in self.data.values())

    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self):
        if not self.__iterator:
            self.__iterator = iter(self)
        return self.__iterator

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            self.index = 0
            raise StopIteration
        else:
            result = list(self.data.values())[self.index]
            self.index += 1
            return result


class Record:
    def __init__(self, name, phones=[], birthday=''):
        self.name = name
        self.phones = phones
        self.birthday = birthday

    def __str__(self):
        return f'{self.name}: {self.phones} {self.birthday} {self.days_to_birthday()}'

    def __repr__(self):
        return f'{self.name}: {self.phones} {self.birthday} {self.days_to_birthday()}'

    def add_phone(self, phone):
        self.phones.append(phone)

    def delete_phone(self, phone):
        self.phones.remove(phone)

    def change_phone(self, old_phone, new_phone):
        self.phones = list(map(lambda x: x.replace(
            old_phone, new_phone), self.phones))

    def days_to_birthday(self):
        if not self.birthday:
            return ' '
        today = date.today()
        birthday_this_year = date(
            today.year, self.birthday.value.month, self.birthday.value.day)
        if birthday_this_year >= today:
            delta = birthday_this_year - today
        else:
            delta = date(today.year + 1, self.birthday.value.month,
                         self.birthday.value.day) - today
        return delta.days


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if re.search(r"\+\d{3}\(\d{2}\)\d{3}\-\d{2}\-\d{2}|\+\d{3}\(\d{2}\)\d{3}\-\d{1}\-\d{3}", new_value):
            self.__value = new_value
        else:
            raise TypeError


class Birthday(Field):

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = datetime.strptime(new_value, '%d/%m/%Y').date()


bool_var = True
address_book = AddressBook({'name': Record(Name('name'), [Phone('+380(67)444-47-74')], Birthday('2/12/1980')),
                            'Polina': Record(Name('Polina'), [Phone('+380(67)777-77-77')], Birthday('12/05/1996'))})


def input_error(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            if func.__name__ == 'add' or func.__name__ == 'change':
                return "Give me name and phone please"
            if func.__name__ == 'phone':
                return "Give me name for finding phone"
            else:
                return 'IndexError'
        except KeyError:
            if func.__name__ == 'phone':
                return 'No such phone'
            return "No such command"
        except ValueError:
            return 'There no such name'
        except TypeError:
            return 'Invalid format'
        except StopIteration:
            return 'StopIteration'
    return inner_function


def split_command_line(inp):
    if inp == 'show all' or inp == 'good bye':
        return [inp]
    return inp.split(' ')


@input_error
def hello():
    return 'How can I help you?'


@input_error
def add(inp):
    record = address_book.data.get(inp[0])
    if record == None:
        record = Record(Name(inp[0]), [Phone(inp[1])])
        address_book.add_record(record)
    else:
        record.add_phone(Phone(inp[1]))
    return 'DONE!'


@input_error
def change(inp):
    record = address_book.data.get(inp[0])
    if record != None:
        record.phones = [Phone(inp[1])]
    else:
        raise ValueError
    return 'DONE!'


@ input_error
def phone(inp):
    return (address_book.data[inp[0]]).phones


@ input_error
def show_all():
    return address_book


@input_error
def show():
    return next(address_book.iterator())


@ input_error
def close():
    global bool_var
    bool_var = False
    return 'Good bye!'


@input_error
def handler(name, arguments):
    def add_func():
        return add(arguments)

    def change_func():
        return change(arguments)

    def phone_func():
        return phone(arguments)

    commands = {'hello': hello,
                'add': add_func,
                'change': change_func,
                'phone': phone_func,
                'show all': show_all,
                'show': show,
                'close': close,
                'exit': close,
                'good bye': close,
                '.': close}

    return commands[name]


def main():
    while bool_var:
        inp = input('Type:\n')
        command, *arguments = split_command_line(inp)
        operation = handler(command.lower(), arguments)
        if isinstance(operation, str):
            print(operation)
        else:
            print(operation())


if __name__ == "__main__":
    main()
