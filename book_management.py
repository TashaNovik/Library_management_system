from typing import List, Optional

class Book:
    def __init__(self, name: str, author: str, year: int, available: bool):
        """
        Книга Конструктор
        :param name:
        :param author:
        :param year:
        :param available:
        """
        self.name = name
        self.author = author
        self.year = year
        self.available = available

class BookManagementSystem:
    def __init__(self):
        """
        Конструктор Системы Книгооборота
        """
        self.books: List[Book] = []

    def add_book(self, book: Book) -> bool:
        """
        Добавляет книгу в библиотеку
        :param book:
        :return: true - если книга добавлена, false - если книга уже есть в библиотеке
        """
        if any (b.name == book.name and
                b.author == book.author and
                b.year == book.year for b in self.books ):
            return False # book already exists
        self.books.append(book)
        return True

    def find_book(self, name: str, author: str, year: int) -> Optional[Book]:
        """
        Ищет книгу в библиотеке
        :param name:
        :param author:
        :param year:
        :return: книга или None если книга не найдена
        """
        for book in self.books:
            if (book.name == name
                    and book.author == author
                    and book.year == year
                    and book.available):  # Ищем доступную книгу по названию
                return book
        return None

    def is_book_borrow(self ,name: str, author: str, year: int) -> bool:
        """
        Проверяет наличие книги в библиотеке
        :param name:
        :param author:
        :param year:
        :return: True если книга есть в библиотеке, False если нет
        """
        for book in self.books:
            if (book.name == name
                    and book.author == author
                    and book.year == year
                    and not book.available):
                return True
        return False

    def return_book(self, name: str, author: str, year: int) -> bool:
        """
        Возвращает книгу в библиотеку
        :param name:
        :param author:
        :param year:
        :return: True если книга возвращена, False если книга не найдена
        """
        for book in self.books:
            if (book.name == name
                    and book.author == author
                    and book.year == year
                    and not book.available):
                book.available = True
                return True
        return False

if __name__ == '__main__':
    """
    Пример использования методов, реализованных выше
    """
    library = BookManagementSystem()
    book1 = Book("The Lord of the Rings", "J. R. R. Tolkien", 1954, True)
    book2 = Book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", 1979, True)

    library.add_book(book1)
    library.add_book(book2)

    found_book = library.find_book("The Lord of the Rings", "J. R. R. Tolkien", 1954)
    if found_book:
        book1.available = False
        print(f"Found book: {found_book.name} by {found_book.author} ({found_book.year})")

    print(f"Is 'The Hitchhiker's Guide to the Galaxy' borrowed?"
          f" {library.is_book_borrow('The Hitchhiker\'s Guide to the Galaxy',
          'Douglas Adams', 1979)}"
          f"\nIs 'The Lord of the Rings' borrowed? {library.is_book_borrow('The Lord of the Rings', 
                                                                           "J. R. R. Tolkien", 1954)}")





