from datetime import datetime
import inspect
import math

import pytest

import bookstore.model 


module_members = [member[0] for member in inspect.getmembers(bookstore.model)]
trasaction_defined = 'Transaction' in module_members
book_defined = 'Book' in module_members
bookstore_defined = 'Bookstore' in module_members


if trasaction_defined:
    from bookstore.model import Transaction

if book_defined:
    from bookstore.model import Book

if bookstore_defined:
    from bookstore.model import Bookstore

@pytest.fixture
def transaction():
    return Transaction(Transaction.SELL, 5)

    
@pytest.fixture
def book_without_transaction():
    return Book('1234', 'Test Book', 10.0, 5.0, 10)


@pytest.fixture
def book_with_transaction():
    book = Book('1234', 'Test Book', 10.0, 5.0, 10)
    book.transactions.append(Transaction(Transaction.SELL, 5))
    return book

@pytest.fixture
def empty_bookstore():
    return Bookstore()

@pytest.fixture
def bookstore_with_books():
    bookstore = Bookstore()
    bookstore.add_book('1234', 'Test Book', 10.0, 5.0, 10)
    bookstore.add_book('5678', 'Test Book 2', 20.0, 10.0, 20)
    return bookstore




# Test the Transaction class
@pytest.mark.skipif(not trasaction_defined, reason='Transaction class is not defined')
@pytest.mark.parametrize('constant_name, constant_value', [
    ('SELL', 1),
    ('SUPPLY', 2)
])
def test_class_transaction_has_constants(constant_name, constant_value):
    assert hasattr(Transaction, constant_name)
    assert getattr(Transaction, constant_name) == constant_value

@pytest.mark.skipif(not trasaction_defined, reason='Transaction class is not defined')
@pytest.mark.parametrize('attribute_name, attribute_type', [
    ('type', int),
    ('copies', int),
    ('date', datetime)
])
def test_class_transaction_has_attributes(transaction, attribute_name, attribute_type):
    assert hasattr(transaction, attribute_name)
    assert isinstance(getattr(transaction, attribute_name), attribute_type)

@pytest.mark.skipif(not trasaction_defined, reason='Transaction class is not defined')
@pytest.mark.parametrize('transaction_type, copies', [
    (1, 5),
    (2, 10)
])   
def test_class_transaction_initilization(transaction_type, copies):
    transaction = Transaction(transaction_type, copies)
    assert transaction.type == transaction_type
    assert transaction.copies == copies
    assert isinstance(transaction.date, datetime)
    


# Test the Book class
@pytest.mark.skipif(not book_defined, reason='Book class is not defined')
@pytest.mark.parametrize('attribute_name, attribute_type', [
    ('isbn', str),
    ('title', str),
    ('sale_price', float),
    ('purchase_price', float),
    ('quantity', int),
    ('transactions', list)
])
def test_class_book_has_attributes(book_without_transaction, attribute_name, attribute_type):
    assert hasattr(book_without_transaction, attribute_name)
    assert isinstance(getattr(book_without_transaction, attribute_name), attribute_type)


@pytest.mark.skipif(not book_defined, reason='Book class is not defined')
@pytest.mark.parametrize('isbn, title, sale_price, purchase_price, quantity', [
    ('1234', 'Test Book', 10.0, 5.0, 10),
    ('5678', 'Test Book 2', 20.0, 10.0, 20),
    ('91011', 'Test Book 3', 30.0, 15.0, 30),
    ('121314', 'Test Book 4', 40.0, 20.0, 40)
])
def test_class_book_initilization(isbn, title, sale_price, purchase_price, quantity):
    book = Book(isbn, title, sale_price, purchase_price, quantity)
    assert book.isbn == isbn
    assert book.title == title
    assert book.sale_price == sale_price
    assert book.purchase_price == purchase_price
    assert book.quantity == quantity
    assert book.transactions == []


@pytest.mark.skipif(not book_defined, reason='Book class is not defined')
@pytest.mark.parametrize('method_name, signature', [
    ('sell', '(copies: int) -> bool'),
    ('supply', '(copies: int)'),
    ('copies_sold', '() -> int'),
    ('__str__', '() -> str')
])
def test_class_book_has_methods(book_without_transaction, method_name, signature):
    assert hasattr(book_without_transaction, method_name)
    method = getattr(book_without_transaction, method_name)
    assert callable(method)
    assert str(inspect.signature(method)) == signature


@pytest.mark.skipif(not book_defined, reason='Book class is not defined')
def test_class_book_sell_method_returns_false_and_does_not_add_transaction_when_copies_sold_exceed_quantity(book_with_transaction):
    assert not book_with_transaction.sell(11)
    assert book_with_transaction.quantity == 10
    assert len(book_with_transaction.transactions) == 1

@pytest.mark.skipif(not book_defined, reason='Book class is not defined')
def test_class_book_sell_method_returns_true_and_adds_transaction_when_copies_sold_does_not_exceed_quantity(book_with_transaction):
    assert book_with_transaction.sell(5)
    assert book_with_transaction.quantity == 5
    assert len(book_with_transaction.transactions) == 2

@pytest.mark.skipif(not book_defined, reason='Book class is not defined')
def test_class_book_supply_method_increases_quantity(book_with_transaction):
    book_with_transaction.supply(5)
    assert book_with_transaction.quantity == 15


@pytest.mark.skipif(not book_defined, reason='Book class is not defined')
def test_class_book_supply_method_adds_transaction(book_with_transaction):
    book_with_transaction.supply(5)
    assert len(book_with_transaction.transactions) == 2


@pytest.mark.skipif(not book_defined, reason='Book class is not defined')
@pytest.mark.parametrize('copies_supplied, copies_sold', [
    (5, (1, 2, 3)),
    (8, (2, 1)),
    (1, (1,))
])
def test_class_book_copies_sold_method_returns_total_copies_sold(book_without_transaction, copies_supplied, copies_sold):
    book_without_transaction.supply(copies_supplied)
    for copies in copies_sold:
        book_without_transaction.sell(copies)
    assert book_without_transaction.copies_sold() == sum(copies_sold)


@pytest.mark.skipif(not book_defined, reason='Book class is not defined')
def test_class_book_str_method_returns_string_representation(book_without_transaction):
    assert str(book_without_transaction) == "ISBN: 1234\n" \
                                            "Title: Test Book\n" \
                                            "Sale Price: 10.0\n" \
                                            "Purchase Price: 5.0\n" \
                                            "Quantity: 10"


# Test the Bookstore class
@pytest.mark.skipif(not bookstore_defined, reason='Bookstore class is not defined')
@pytest.mark.parametrize('attribute_name, attribute_type', [
    ('catalog', dict)
])
def test_class_bookstore_has_attributes(empty_bookstore, attribute_name, attribute_type):
    assert hasattr(empty_bookstore, attribute_name)
    assert isinstance(getattr(empty_bookstore, attribute_name), attribute_type)

@pytest.mark.skipif(not bookstore_defined, reason='Bookstore class is not defined')
def test_class_bookstore_initilization(empty_bookstore):
    assert empty_bookstore.catalog == {}


@pytest.mark.skipif(not bookstore_defined, reason='Bookstore class is not defined')
@pytest.mark.parametrize('method_name, signature', [
    ('add_book', '(isbn: str, title: str, sale_price: float, purchase_price: float, quantity: int)'),
    ('search_by_isbn', '(isbn: str) -> bookstore.model.Book | None'),
    ('delete_book', '(isbn: str)'),
    ('sell_book', '(isbn: str, copies: int) -> bool'),
    ('supply_book', '(isbn: str, copies: int) -> bool'),
    ('best_selling_book', '() -> bookstore.model.Book | None'),
])
def test_class_bookstore_has_methods(empty_bookstore, method_name, signature):
    assert hasattr(empty_bookstore, method_name)
    method = getattr(empty_bookstore, method_name)
    assert callable(method)
    assert str(inspect.signature(method)) == signature
    

@pytest.mark.skipif(not bookstore_defined, reason='Bookstore class is not defined')
def test_class_bookstore_add_book_method_adds_book_to_catalog(empty_bookstore):
    empty_bookstore.add_book('1234', 'Test Book', 10.0, 5.0, 10)
    assert '1234' in empty_bookstore.catalog
    assert isinstance(empty_bookstore.catalog['1234'], Book)


@pytest.mark.skipif(not bookstore_defined, reason='Bookstore class is not defined')
def test_class_bookstore_does_not_add_book_to_catalog_if_isbn_already_exists(bookstore_with_books):
    bookstore_with_books.add_book('1234', 'Test Book', 10.0, 5.0, 10)
    assert len(bookstore_with_books.catalog) == 2


@pytest.mark.skipif(not bookstore_defined, reason='Bookstore class is not defined')
def test_class_bookstore_delete_book_method_deletes_book_from_catalog(bookstore_with_books):
    bookstore_with_books.delete_book('1234')
    assert '1234' not in bookstore_with_books.catalog


@pytest.mark.skipif(not bookstore_defined, reason='Bookstore class is not defined')
def test_class_bookstore_search_by_isbn_method_returns_book(bookstore_with_books):
    assert bookstore_with_books.search_by_isbn('1234').isbn == '1234'

@pytest.mark.skipif(not bookstore_defined, reason='Bookstore class is not defined')
def test_class_bookstore_search_by_isbn_method_returns_none_if_isbn_not_found(bookstore_with_books):
    assert bookstore_with_books.search_by_isbn('12345') is None

@pytest.mark.skipif(not bookstore_defined, reason='Bookstore class is not defined')
def test_class_bookstore_sell_book_method_returns_false_if_book_not_found(bookstore_with_books):
    assert not bookstore_with_books.sell_book('12345', 5)

@pytest.mark.skipif(not bookstore_defined, reason='Bookstore class is not defined')
def test_class_bookstore_sell_book_method_returns_false_if_copies_sold_exceed_quantity(bookstore_with_books):
    assert not bookstore_with_books.sell_book('1234', 11)

@pytest.mark.skipif(not bookstore_defined, reason='Bookstore class is not defined')
def test_class_bookstore_sell_book_method_returns_true_if_copies_sold_does_not_exceed_quantity(bookstore_with_books):
    assert bookstore_with_books.sell_book('1234', 5)


@pytest.mark.skipif(not bookstore_defined, reason='Bookstore class is not defined')
def test_class_bookstore_supply_book_method_returns_false_if_book_not_found(bookstore_with_books):
    assert not bookstore_with_books.supply_book('12345', 5)


@pytest.mark.skipif(not bookstore_defined, reason='Bookstore class is not defined')
def test_class_bookstore_supply_book_method_increases_quantity(bookstore_with_books):
    bookstore_with_books.supply_book('1234', 5)
    assert bookstore_with_books.search_by_isbn('1234').quantity == 15


@pytest.mark.skipif(not bookstore_defined, reason='Bookstore class is not defined')
def test_class_bookstore_best_selling_book_method_returns_book_with_most_copies_sold(bookstore_with_books):
    bookstore_with_books.sell_book('1234', 5)
    bookstore_with_books.sell_book('1234', 3)
    bookstore_with_books.sell_book('5678', 10)
    assert bookstore_with_books.best_selling_book().isbn == '5678'


@pytest.mark.skipif(not bookstore_defined, reason='Bookstore class is not defined')
def test_class_bookstore_best_selling_book_method_returns_none_if_no_books_sold(bookstore_with_books):
    assert bookstore_with_books.best_selling_book() is None
    