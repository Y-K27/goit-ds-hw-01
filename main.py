from collections import UserDict
from datetime import datetime, timedelta
import pickle

#Базовий клас для полів запису.
class Field:
    def __init__(self, value):
        self.some_value = value
        
    def __str__(self):
        return str(self.some_value)
    
# Клас для зберігання імені контакту. Обов'язкове поле.
class Name(Field):
    def __init__(self, contact_name):
        self.contact_name = contact_name      
    def check_name(self):
        if len(self.contact_name) >= 2:
            return self.contact_name
        else:
            #print("Name is too short")
            raise "Name is too short"
        
# Клас для зберігання номера телефону. Має валідацію формату (10 цифр)
class Phone(Field):
    def __init__(self, phone_number):
        self.phone = phone_number
    def check_phone_number(self):
        if len(self.phone) == 10 and self.phone.isdigit():
            return self.phone
        else:
            print("The number is incorrect. The phone number must consist of 10 digits ")
            raise ValueError
#
class Birthday(Field):
    def __init__(self, b_date):
        self.birthday = b_date
        #print("test class Bday", type(self.birthday), self.birthday )
        try:
            bday =(datetime.date(datetime.strptime(self.birthday, '%d.%m.%Y')))
            dict_BD = {
                "day": bday.day,
                "month": bday.month,
                "year": bday.year}
            self.birthday = dict_BD
            super().__init__(bday)
            #return self.birthday
        except ValueError:
            raise ValueError ("Invalid date format. Use DD.MM.YYYY")
      

# Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
class Record:
    def __init__(self, record_name, record_list):
        self.name = Name(record_name).check_name()
        self.phones = record_list
        self.birthday = None
        
    def add_phone(self, phone):
        if phone not in self.phones:
            #print(f"Phone list :{self.phones}")
            self.phones.append(phone)
            #print(f'Phone {phone} has been successfully added from contact {self.name}') 
        else:
            print(f"Phone {phone} already recorded for a contact {self.name}")
            raise "conflict of types"
    
    
    def add_birthday(self, birthday):
        self.birthday = birthday
        
#    def remove_phone(self, phone):
#        if phone in [p.value for p in self.phones]:
#            self.phones = [p for p in self.phones if p.value != phone]
#            print(f'Phone {phone} removed from contact {self.name}')
#        else:
#            print(f"Phone {phone} not found for contact {self.name}")
#    
#    def edit_phone(self, old_phone, new_pnone):
#        if old_phone in [p.value for p in self.phones]:
#            for phone in self.phones:
#                if phone.value == old_phone: 
#                    phone.value = new_pnone
#            print(f'Phone nomber has been successfully modified')
#        else:
#            print(f"Phone {old_phone} not found for contact {self.name}")
#    
#    def find_phone(self, phone:Phone):
#        if phone in [ph.value for ph in self.phones]:
#            print(f'{self.name}: {phone}')
#        else:
#            print(f"Phone {phone} not found for contact {self.name}")
#    

# Виведення всіх записів у книзі
    def __str__(self):
        return f"Contact name: {self.name}, Birthday: {self.birthday} phones: {'; '.join(p.value for p in self.phones)}"
#
 # Створення нової адресної книги
 # Додавання/видалення запису до адресної книги
class AddressBook(UserDict):
    def __init__(self, initial=None):
        if initial is None:
            self.address_book = dict()
        else:
            self.address_book = dict()
		
    def add_record(self, contact:Record, change=False):
        if contact.name not in [key for key in self.address_book]:
            self.address_book[contact.name] = {"Phone":contact.phones, "Birthday":contact.birthday}
            #print("The contact has been saved")
        else:
            if change:
                self.address_book[contact.name] = contact.phones
            elif contact.birthday != None:
                self.address_book[contact.name] = {"Phone":contact.phones, "Birthday":contact.birthday}
            else:
                print(f"A contact {contact.name} already exists in the contact book")
              
    
    def find(self, name):
        if name in [key for key in self.address_book]:
            #print(f"Contact name: {name}, phones: {self.address_book[name]}")
            return self.address_book[name]

                  
#    def delete(self, name):
#        if name in [key for key in self.address_book]:
#            self.address_book.pop(name)
#            print(f"Contact name: {name}, has been deleted")
#        else:
#            print(f"Contact: {name} are not exist)")
#        pass
    
    
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please. "
        except KeyError:
            return "Give me correct name please."
        except TypeError:
            return "Give me correct name and phone please."
        except IndexError:
            return "Give me name and phone please. Wrong index"

    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    add_contact_name, phone, *_ = args
    record = book.find(add_contact_name)
    chek_in_number=Phone(phone).check_phone_number()# перевіряємо перед записом чи номер введений правильно
    #print(f"find record: {record}")
    if record == None:
        record = Record(add_contact_name,[])
        record.add_phone(chek_in_number)
        book.add_record(record)
        message = "Contact added."
    elif phone:
        #print("cheking phone number")
        #print(type(chek_in_number), chek_in_number)
        #print(f"old record: {type(record)}, {record}")
        record_rwr = Record(add_contact_name, record['Phone'])
        record_rwr.add_phone(chek_in_number)
        message = "Contact updated."
    return message

@input_error
def check_contact(args, book: AddressBook):
        check_contact_name, *_ = args
        record = book.find(check_contact_name)
        if record == None:
            return F"The contact: {check_contact_name} hasn't a hone number/-s"
        else:
            return f"The contact: {check_contact_name} has a phone nomber/-s: {str(record)}"

@input_error
def change_contact_number(args, book: AddressBook ):            #Функйція змінює номер телефону\-ів заданого контакту
    contact_name, phone, *_ = args
    cheked_number=Phone(phone).check_phone_number()
    change = True
    record = book.find(contact_name)
    if record == None:
        return f"The contact: {contact_name} hasn't a hone number/-s"
    else:
        chenged_record = Record(contact_name,[])
        chenged_record.add_phone(cheked_number)
        book.add_record(chenged_record, change)
        return "Contakt updated."

@input_error    
def all_contacts(book: AddressBook):                            # Функція виведення всіх контактів з телефонної книги
    list=''
    book_all_contacts = dict(book.address_book)
    #print(type(book_test), book_test)
    if book_all_contacts == None:
        return "Phone book is empty"
    else:
        for key in book_all_contacts:
            if book_all_contacts[key]['Birthday'] != None:
                list+= f"Name: \"{key}\" Phone: {book_all_contacts[key]['Phone']}, Birthday: {book_all_contacts[key]['Birthday']}\n" #Записуємо в одремі радки дані для кожгоного елемента телефонної книги
            else:
                list+= f"Name: \"{key}\" Phone: {book_all_contacts[key]['Phone']}\n"
        return list                                             #Повертаємо список як результат роботи функції


@input_error                                                    #Ф-ія додавання дати народження до існуючого контакту
def add_birthdays(args, book: AddressBook):
    add_bd_name, date, *_ = args
    #print(Birthday(date))
    birthday = Birthday(date).some_value
    #b_day= '.'.join(str(birthday[k]) for k in birthday)
    #print(b_day)
    book_rekord = book.find(add_bd_name) 
    if book_rekord == None:
        return f"Contact: {add_bd_name} are not exist"
    else:
        chenged_record = Record(add_bd_name, book_rekord['Phone'])
        chenged_record.add_birthday(birthday)
        book.add_record(chenged_record)
        return "Day of birth was added"


@input_error
def show_birthdays(args, book: AddressBook):                    # Ф-ія поветає дату народження для заданого контакту
    show_bd_name, *_ = args
    book_record = book.find(show_bd_name)
    if book_record == None:
        return f"Contact: {show_bd_name} are not exist"
    else:
        if book_record['Birthday']!= None:
            return book_record['Birthday']
        else:
            return f"Contact: {show_bd_name} has no recorded birthday" 


@input_error
def birthdays(book: AddressBook):                               # Ф-ія поветає імена і дати народження для контактів у яких день народження у найближчі 7 днів
    list= ''
    interval = timedelta(days=7)
    now_day = datetime.now().date()
    day_max = now_day+interval
    book_record = book.address_book
    #print(type(book_rekord), book_rekord)
    for item in book_record:
        if book_record[item]['Birthday'] != None:
            book_record[item]['Birthday']=book_record[item]['Birthday'].replace(year=now_day.year)
            if book_record[item]['Birthday']>=now_day and book_record[item]['Birthday']<=day_max:
                list+=f"Name: \"{item}\" Birthday: {book_record[item]['Birthday']}\n"
    return list

#Функція запису контактної книги в файл
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

#Функція считування контактної книги з файлу
def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook().address_book  # Повернення нової адресної книги, якщо файл не знайдено

#Функція для обробки введених команд користувачем
def main():
    print("Welcome to the assistant bot!")
    book = AddressBook()
    book.address_book = load_data()
    #print(f"Book type: {type(book)}")
    #print(book.address_book)
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        
        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book.address_book) 
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))                      
            
        elif command == "all":
            print(all_contacts(book))                           
              
        elif command == "phone":
            print(check_contact(args, book))                        
            
        elif command == "change":    
            print(change_contact_number(args, book))            
            
        elif command == "birthdays":                            
            print(birthdays(book))
            
        elif command == "show-birthday":                        
            print(show_birthdays(args, book))
                   
        elif command == "add-birthday":                         
            print(add_birthdays(args, book))
                        
        else:
            print("Invalid command.")
    save_data(book.address_book)        
            
if __name__ == "__main__":
    main()