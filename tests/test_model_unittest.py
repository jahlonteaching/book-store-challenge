import unittest
from datetime import datetime
import inspect

import bookstore.model

module_members = [member[0] for member in inspect.getmembers(bookstore.model)]
transaction_defined = 'Transaction' in module_members
book_defined = 'Book' in module_members
bookstore_defined = 'Bookstore' in module_members

if transaction_defined:
    from bookstore.model import Transaction

if book_defined:
    from bookstore.model import Book

if bookstore_defined:
    from bookstore.model import Bookstore


class TestModel(unittest.TestCase):

    def setUp(self):
        if transaction_defined:
            self.transaction = Transaction(Transaction.SELL, 5)
        if book_defined:
            self.book_without_transaction = Book('1234', 'Test Book', 10.0, 5.0, 10)
            self.book_with_transaction = Book('1234', 'Test Book', 10.0, 5.0, 10)
            self.book_with_transaction.transactions.append(Transaction(Transaction.SELL, 5))
        if bookstore_defined:
            self.empty_bookstore = Bookstore()
            self.bookstore_with_books = Bookstore()
            self.bookstore_with_books.add_book('1234', 'Test Book', 10.0, 5.0, 10)
            self.bookstore_with_books.add_book('5678', 'Test Book 2', 20.0, 10.0, 20)

    @unittest.skipUnless(transaction_defined, 'Transaction class is not defined')
    def test_class_transaction_has_constants(self):
        for constant_name, constant_value in [('SELL', 1), ('SUPPLY', 2)]:
            with self.subTest(constant_name=constant_name, constant_value=constant_value):
                self.assertTrue(hasattr(Transaction, constant_name))
                self.assertEqual(getattr(Transaction, constant_name), constant_value)

    @unittest.skipUnless(transaction_defined, 'Transaction class is not defined')
    def test_class_transaction_has_attributes(self):
        for attribute_name, attribute_type in [('type', int), ('copies', int), ('date', datetime)]:
            with self.subTest(attribute_name=attribute_name, attribute_type=attribute_type):
                self.assertTrue(hasattr(self.transaction, attribute_name))
                self.assertIsInstance(getattr(self.transaction, attribute_name), attribute_type)

    @unittest.skipUnless(transaction_defined, 'Transaction class is not defined')
    def test_class_transaction_initialization(self):
        for transaction_type, copies in [(1, 5), (2, 10)]:
            with self.subTest(transaction_type=transaction_type, copies=copies):
                transaction = Transaction(transaction_type, copies)
                self.assertEqual(transaction.type, transaction_type)
                self.assertEqual(transaction.copies, copies)
                self.assertIsInstance(transaction.date, datetime)

    @unittest.skipUnless(book_defined, 'Book class is not defined')
    def test_class_book_has_attributes(self):
        for attribute_name, attribute_type in [('isbn', str), ('title', str), ('sale_price', float), ('purchase_price', float), ('quantity', int), ('transactions', list)]:
            with self.subTest(attribute_name=attribute_name, attribute_type=attribute_type):
                self.assertTrue(hasattr(self.book_without_transaction, attribute_name))
                self.assertIsInstance(getattr(self.book_without_transaction, attribute_name), attribute_type)

    @unittest.skipUnless(book_defined, 'Book class is not defined')
    def test_class_book_initialization(self):
        for isbn, title, sale_price, purchase_price, quantity in [('1234', 'Test Book', 10.0, 5.0, 10), ('5678', 'Test Book 2', 20.0, 10.0, 20), ('91011', 'Test Book 3', 30.0, 15.0, 30), ('121314', 'Test Book 4', 40.0, 20.0, 40)]:
            with self.subTest(isbn=isbn, title=title, sale_price=sale_price, purchase_price=purchase_price, quantity=quantity):
                book = Book(isbn, title, sale_price, purchase_price, quantity)
                self.assertEqual(book.isbn, isbn)
                self.assertEqual(book.title, title)
                self.assertEqual(book.sale_price, sale_price)
                self.assertEqual(book.purchase_price, purchase_price)
                self.assertEqual(book.quantity, quantity)
                self.assertEqual(book.transactions, [])

    @unittest.skipUnless(book_defined, 'Book class is not defined')
    def test_class_book_has_methods(self):
        for method_name, signature in [('sell', '(copies: int) -> bool'), ('supply', '(copies: int)'), ('copies_sold', '() -> int'), ('__str__', '() -> str')]:
            with self.subTest(method_name=method_name, signature=signature):
                self.assertTrue(hasattr(self.book_without_transaction, method_name))
                method = getattr(self.book_without_transaction, method_name)
                self.assertTrue(callable(method))
                self.assertEqual(str(inspect.signature(method)), signature)

    @unittest.skipUnless(book_defined, 'Book class is not defined')
    def test_class_book_sell_method_returns_false_and_does_not_add_transaction_when_copies_sold_exceed_quantity(self):
        self.assertFalse(self.book_with_transaction.sell(11))
        self.assertEqual(self.book_with_transaction.quantity, 10)
        self.assertEqual(len(self.book_with_transaction.transactions), 1)

    @unittest.skipUnless(book_defined, 'Book class is not defined')
    def test_class_book_sell_method_returns_true_and_adds_transaction_when_copies_sold_does_not_exceed_quantity(self):
        self.assertTrue(self.book_with_transaction.sell(5))
        self.assertEqual(self.book_with_transaction.quantity, 5)
        self.assertEqual(len(self.book_with_transaction.transactions), 2)

    @unittest.skipUnless(book_defined, 'Book class is not defined')
    def test_class_book_supply_method_increases_quantity(self):
        self.book_with_transaction.supply(5)
        self.assertEqual(self.book_with_transaction.quantity, 15)

    @unittest.skipUnless(book_defined, 'Book class is not defined')
    def test_class_book_supply_method_adds_transaction(self):
        self.book_with_transaction.supply(5)
        self.assertEqual(len(self.book_with_transaction.transactions), 2)

    @unittest.skipUnless(book_defined, 'Book class is not defined')
    def test_class_book_copies_sold_method_returns_total_copies_sold(self):
        for copies_supplied, copies_sold in [(5, (1, 2, 3)), (8, (2, 1)), (1, (1,))]:
            with self.subTest(copies_supplied=copies_supplied, copies_sold=copies_sold):
                self.book_without_transaction.supply(copies_supplied)
                for copies in copies_sold:
                    self.book_without_transaction.sell(copies)
                self.assertEqual(self.book_without_transaction.copies_sold(), sum(copies_sold))

    @unittest.skipUnless(book_defined, 'Book class is not defined')
    def test_class_book_str_method_returns_string_representation(self):
        self.assertEqual(str(self.book_without_transaction), "ISBN: 1234\nTitle: Test Book\nSale Price: 10.0\nPurchase Price: 5.0\nQuantity: 10")

    @unittest.skipUnless(bookstore_defined, 'Bookstore class is not defined')
    def test_class_bookstore_has_attributes(self):
        for attribute_name, attribute_type in [('catalog', dict)]:
            with self.subTest(attribute_name=attribute_name, attribute_type=attribute_type):
                self.assertTrue(hasattr(self.empty_bookstore, attribute_name))
                self.assertIsInstance(getattr(self.empty_bookstore, attribute_name), attribute_type)

    @unittest.skipUnless(bookstore_defined, 'Bookstore class is not defined')
    def test_class_bookstore_initialization(self):
        self.assertEqual(self.empty_bookstore.catalog, {})

    @unittest.skipUnless(bookstore_defined, 'Bookstore class is not defined')
    def test_class_bookstore_has_methods(self):
        for method_name, signature in [('add_book', '(isbn: str, title: str, sale_price: float, purchase_price: float, quantity: int)'), ('search_by_isbn', '(isbn: str) -> bookstore.model.Book | None'), ('delete_book', '(isbn: str)'), ('sell_book', '(isbn: str, copies: int) -> bool'), ('supply_book', '(isbn: str, copies: int) -> bool'), ('best_selling_book', '() -> bookstore.model.Book | None')]:
            with self.subTest(method_name=method_name, signature=signature):
                self.assertTrue(hasattr(self.empty_bookstore, method_name))
                method = getattr(self.empty_bookstore, method_name)
                self.assertTrue(callable(method))
                self.assertEqual(str(inspect.signature(method)), signature)

    @unittest.skipUnless(bookstore_defined, 'Bookstore class is not defined')
    def test_class_bookstore_add_book_method_adds_book_to_catalog(self):
        for isbn, title, sale_price, purchase_price, quantity in [('1234', 'Test Book', 10.0, 5.0, 10), ('5678', 'Test Book 2', 20.0, 10.0, 20), ('91011', 'Test Book 3', 30.0, 15.0, 30)]:
            with self.subTest(isbn=isbn, title=title, sale_price=sale_price, purchase_price=purchase_price, quantity=quantity):
                self.empty_bookstore.add_book(isbn, title, sale_price, purchase_price, quantity)
                self.assertIn(isbn, self.empty_bookstore.catalog)
                self.assertIsInstance(self.empty_bookstore.catalog[isbn], Book)

    @unittest.skipUnless(bookstore_defined, 'Bookstore class is not defined')
    def test_class_bookstore_does_not_add_book_to_catalog_if_isbn_already_exists(self):
        for isbn, title, sale_price, purchase_price, quantity in [('1234', 'Test Book', 10.0, 5.0, 10), ('5678', 'Test Book 2', 20.0, 10.0, 20)]:
            with self.subTest(isbn=isbn, title=title, sale_price=sale_price, purchase_price=purchase_price, quantity=quantity):
                self.bookstore_with_books.add_book(isbn, title, sale_price, purchase_price, quantity)
                self.assertEqual(len(self.bookstore_with_books.catalog), 2)

    @unittest.skipUnless(bookstore_defined, 'Bookstore class is not defined')
    def test_class_bookstore_delete_book_method_deletes_book_from_catalog(self):
        self.bookstore_with_books.delete_book('1234')
        self.assertNotIn('1234', self.bookstore_with_books.catalog)

    @unittest.skipUnless(bookstore_defined, 'Bookstore class is not defined')
    def test_class_bookstore_search_by_isbn_method_returns_book(self):
        for isbn in ['1234', '5678']:
            with self.subTest(isbn=isbn):
                self.assertEqual(self.bookstore_with_books.search_by_isbn(isbn).isbn, isbn)

    @unittest.skipUnless(bookstore_defined, 'Bookstore class is not defined')
    def test_class_bookstore_search_by_isbn_method_returns_none_if_isbn_not_found(self):
        self.assertIsNone(self.bookstore_with_books.search_by_isbn('12345'))

    @unittest.skipUnless(bookstore_defined, 'Bookstore class is not defined')
    def test_class_bookstore_sell_book_method_returns_false_if_book_not_found(self):
        self.assertFalse(self.bookstore_with_books.sell_book('12345', 5))

    @unittest.skipUnless(bookstore_defined, 'Bookstore class is not defined')
    def test_class_bookstore_sell_book_method_returns_false_if_copies_sold_exceed_quantity(self):
        for isbn, quantity in [('1234', 11), ('5678', 21)]:
            with self.subTest(isbn=isbn, quantity=quantity):
                self.assertFalse(self.bookstore_with_books.sell_book(isbn, quantity))

    @unittest.skipUnless(bookstore_defined, 'Bookstore class is not defined')
    def test_class_bookstore_sell_book_method_returns_true_if_copies_sold_does_not_exceed_quantity(self):
        for isbn, quantity in [('1234', 5), ('5678', 10)]:
            with self.subTest(isbn=isbn, quantity=quantity):
                self.assertTrue(self.bookstore_with_books.sell_book(isbn, quantity))

    @unittest.skipUnless(bookstore_defined, 'Bookstore class is not defined')
    def test_class_bookstore_supply_book_method_returns_false_if_book_not_found(self):
        self.assertFalse(self.bookstore_with_books.supply_book('12345', 5))

    @unittest.skipUnless(bookstore_defined, 'Bookstore class is not defined')
    def test_class_bookstore_supply_book_method_increases_quantity(self):
        for isbn, total in [('1234', 15), ('5678', 25)]:
            with self.subTest(isbn=isbn, total=total):
                self.bookstore_with_books.supply_book(isbn, 5)
                self.assertEqual(self.bookstore_with_books.search_by_isbn(isbn).quantity, total)

    @unittest.skipUnless(bookstore_defined, 'Bookstore class is not defined')
    def test_class_bookstore_best_selling_book_method_returns_book_with_most_copies_sold(self):
        self.bookstore_with_books.sell_book('1234', 5)
        self.bookstore_with_books.sell_book('1234', 3)
        self.bookstore_with_books.sell_book('5678', 10)
        self.assertEqual(self.bookstore_with_books.best_selling_book().isbn, '5678')

    @unittest.skipUnless(bookstore_defined, 'Bookstore class is not defined')
    def test_class_bookstore_best_selling_book_method_returns_none_if_no_books_sold(self):
        self.assertIsNone(self.bookstore_with_books.best_selling_book())


if __name__ == '__main__':
    unittest.main()