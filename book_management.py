from typing import List, Optional
from pydantic_models import Book, BookNotAvailable

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def log_operation(func):
    """Декоратор для логирования операций с книгами."""
    logger = logging.getLogger(__name__)

    def wrapper(*args, **kwargs):
        logger.info(f"Вызов функции: {func.__name__}")
        logger.debug(f"Аргументы: {args}, {kwargs}")

        result = func(*args, **kwargs)

        logger.info(f"Результат: {result}")
        return result

    return wrapper


class BookManagementSystem:
    def __init__(self):
        """
        Конструктор Системы Книгооборота
        """
        self.books: List[Book] = []


    @log_operation
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
    @log_operation
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
    @log_operation
    def is_book_borrow(self, name: str, author: str, year: int) -> bool:
        """
                Проверяет, взята ли книга в данный момент.
                :param name:
                :param author:
                :param year:
                :return: True, если книга находится в библиотеке и недоступна, False, если ее нет в библиотеке или она доступна.
                """
        for book in self.books:
            if (book.name == name
                    and book.author == author
                    and book.year == year):
                if not book.available:
                    return True  # Книга найдена и недоступна
                else:
                    return False  # Книга найдена, но доступна
        raise BookNotAvailable(f"Книга '{name}' автора '{author}' ({year}) не найдена.")
    @log_operation
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
    Пример использования методов, реализованных выше.
    """
    library = BookManagementSystem()

    # Добавление книг
    library.add_book(Book(name="Властелин колец", author="Дж. Р. Р. Толкин", year=1954,
                          available=True, categories=['Фэнтези', 'Художественная литература']))
    library.add_book(Book(name="Автостопом по галактике", author="Дуглас Адамс",
                          year=1979, available=True, categories=['Научная фантастика', 'Комедия']))

    # Найти и взять книгу
    book_to_borrow = "Властелин колец"
    found_book = library.find_book(book_to_borrow, "Дж. Р. Р. Толкин", 1954)
    if found_book:
        found_book.available = False
        print(f"Книга '{found_book.name}' успешно взята.")
    else:
        print(f"Книга '{book_to_borrow}' не найдена.")

    # Проверка доступности книг (включая обработку ошибок)
    books_to_check = [
        ("Автостопом по галактике", "Дуглас Адамс", 1979),
        ("Властелин колец", "Дж. Р. Р. Толкин", 1954)
    ]
    for book_name, book_author, book_year in books_to_check:
        try:
            is_borrowed = library.is_book_borrow(book_name, book_author, book_year)
            print(f"Книга '{book_name}' взята: {is_borrowed}")
        except BookNotAvailable as e:
            print(f"Ошибка: {e}")

    # Возврат книги
    book_to_return = "Властелин колец"
    if library.return_book(book_to_return, "Дж. Р. Р. Толкин", 1954):
        print(f"Книга '{book_to_return}' успешно возвращена.")
    else:
        print(f"Книга '{book_to_return}' не найдена или не была взята.")