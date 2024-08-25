import sys

from bookstore.model import Bookstore


class UIConsole:
    
    def __init__(self):
        self.bookstore = Bookstore()
        self.options = {
            '1': self.add_book,
            '2': self.sell_book,
            '3': self.supply_book,
            '4': self.search_by_isbn,
            '5': self.delete_book,
            '6': self.best_seller,
            '0': self.exit
        }

    def print_menu(self):
        print("====================================")
        print('Bookstore App Menu')
        print('1. Add book')
        print('2. Sell book')
        print('3. Supply book')
        print('4. Search by ISBN')
        print('5. Delete book')
        print('6. Best seller')
        print('0. Exit')
        print("====================================")
    
    def run(self):
        while True:
            self.print_menu()
            option = input('Enter option: ')
            action = self.options.get(option)
            if action:
                action()
            else:
                print('Invalid option')
    
    def add_book(self):
        print(">>> Add book ========================")
        isbn = input('Enter ISBN: ')
        title = input('Enter title: ')
        sale_price = float(input('Enter sale price: '))
        purchase_price = float(input('Enter purchase price: '))
        quantity = int(input('Enter quantity: '))
        self.bookstore.add_book(isbn, title, sale_price, purchase_price, quantity)
    
    def sell_book(self):
        print(">>> Sell book ========================")
        isbn = input('Enter ISBN: ')
        quantity = int(input('Enter quantity: '))
        if not self.bookstore.sell_book(isbn, quantity):
            print('Book not found or not enough quantity')
        else:
            print('Book sold successfully')
    
    def supply_book(self):
        print(">>> Supply book ========================")
        isbn = input('Enter ISBN: ')
        quantity = int(input('Enter quantity: '))
        if not self.bookstore.supply_book(isbn, quantity):
            print('Book not found')
        else:
            print('Book supplied successfully')
    
    def search_by_isbn(self):
        print(">>> Search by ISBN ========================")
        isbn = input('Enter ISBN: ')
        book = self.bookstore.search_by_isbn(isbn)
        if book:
            print(book)
        else:
            print('Book not found')
    
    def delete_book(self):
        print(">>> Delete book ========================")
        isbn = input('Enter ISBN: ')
        if not self.bookstore.delete_book(isbn):
            print('Book not found')
        else:
            print('Book deleted successfully')
    
    def best_seller(self):
        print(">>> Best seller ========================")
        book = self.bookstore.best_selling_book()
        if book:
            print(book)
        else:
            print('No book sold yet')
    
    def exit(self):
        print("\nGoodbye!")
        sys.exit(0)
