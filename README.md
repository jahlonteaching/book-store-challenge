# Book Store [![es](https://img.shields.io/badge/lang-es-green)](README.es.md "Versión en español")

Book store is an application used to asses the knowledge of OOP concepts in python. The application is a simple book store that allows users to add, remove, list and search for books. The application is implemented using classes and objects in python.

The model of the application is as follows:

![Book Store Model](assets/book-store-model.png)

The application code is incomplete, the idea is to complete it taking into account the following steps.

1. Complete de class `Transaction` taking into account the following requirements:
    - The class should have a constant `SELL` of type `int` with value `1`.
    - The class should have a constant `SUPPLY` of type `int` with value `2`.
    - The class should have an `__init__` method that receives the following parameters:
        - `type` of type `int`.
        - `copies` of type `int`.

        In the `__init__` method the class should initialize the attributes `type` and `copies` with the values received as parameters.
    - The class should have an attribute `date` of type `datetime` that should be initialized with the current date and time (you can use the `datetime.now()` function to get the current date an time).

2. Complete the `Book` class taking into account the following requirements:
    - The class should have an `__init__` method that receives the following parameters:
        - `isbn` of type `str`.
        - `title` of type `str`.
        - `sale_price` of type `float`.
        - `purchase_price` of type `float`.
        - `quantity` of type `int`.

        In the `__init__` method the class should initialize the attributes `isbn`, `title`, `sale_price`, `purchase_price` and `quantity` with the values received as parameters.
    - The class should have an attribute `transactions` of type `list[Transaction]` that should be initialized as an empty list.
    - The class should have an instance method `sell` that receives a parameter `copies` of type `int` and does the following:
        - If the parameter `copies` is greater than the `quantity` attribute of the book, the method should return `False`.
        - Otherwise, the method decreases the `quantity` attribute of the book by the value of the parameter `copies` and adds a new `Transaction` object to the `transactions` list with the type `Transaction.SELL` and the number of `copies` sold.
        - The method should return `True`.
    - The class should have an instance method `supply` that receives a parameter `copies` of type `int` and does the following:
        - Increases the `quantity` attribute of the book by the value of the parameter `copies`
        - Adds a new `Transaction` object to the `transactions` list with the type `Transaction.SUPPLY` and the number of `copies` supplied.
    - The class should have an instance method `copies_sold` that returns an `int` with the total number of copies sold. 
        > **Hint:** you could add the number of copies of each transaction of type `Transaction.SELL`.
    - The class should have an instance method `__str__` that return a `str` with the following format:
        ```
        ISBN: {isbn}
        Title: {title}
        Sale Price: {sale_price}
        Purchase Price: {purchase_price}
        Quantity: {quantity}
        ```

        Where `{isbn}`, `{title}`, `{sale_price}`, `{purchase_price}` and `{quantity}` should be replaced with the values of the attributes of the book.

        > **Hint:** you could use an f-string (`f""`) to format the string and `\n` within the string for a new line.

3. Complete the `Bookstore` class taking into account the following requirements:
    - The class should have an `__init__` method that initializes the `catalog` attribute of type `dict[str, Book]` as an empty dictionary.

    - The class should have an instance method `add_book` that receives the parameters `isbn` of type `str`, `title` of type `str`, `sale_price` of type `float` and `purchase_price` of type `float` and `quantity` of type `int` and does the following:
        - Checks if the `isbn` is not already in the `catalog` dictionary.
        - If the `isbn` is not in the `catalog` dictionary, the method creates a new `Book` object with the received parameters and adds it to the `catalog` dictionary using the `isbn` as the key.

    - The class should have an instance method `delete_book` that receives the parameter `isbn` of type `str` and does the following:
        - Checks if the `isbn` is in the `catalog` dictionary.
        - If the `isbn` is in the `catalog` dictionary, the method removes the book from the `catalog` dictionary.
    - The class should have an instance method `search_by_isbn` that receives the parameter `isbn` of type `str` and returns `Book | None` with the book that has the received `isbn` or `None` if the book is not in the `catalog` dictionary.
    
    - The class should have the instance methods `sell_book` and `supply_book` that receives the parameters `isbn` of type `str` and `copies` of type `int`. Copy the following code to the `Bookstore` class to complete the methods:
        ```python
        def sell_book(self, isbn: str, copies: int) -> bool:
            book = self.search_by_isbn(isbn)
            if book is None:
                return False
            return book.sell(copies)

        def supply_book(self, isbn: str, copies: int) -> bool:
            book = self.search_by_isbn(isbn)
            if book is None:
                return False
            book.supply(copies)
            return True
        ```
    - The class should have an instance method `best_selling_book` that returns `Book | None` with the book that has sold the most copies or `None` if there are no books sold .
        
        
    