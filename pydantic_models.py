from typing import List
from pydantic import BaseModel, field_validator


class Book(BaseModel):
    name: str
    author: str
    year: int
    available: bool
    categories: List[str]

    @field_validator('categories')
    def validate_categories(cls, value):
        if not all(isinstance(cat, str) for cat in value):
            raise ValueError("Categories must be a list of strings")
        if not value:  # Проверка на пустой список
            raise ValueError("Categories list cannot be empty")
        return value

    def validate_available(self):  # Изменено на обычный метод
        if not self.available:
            raise BookNotAvailable(book=self, reason="Книга не доступна.")

class User(BaseModel):
    name: str
    email: str
    membership_id: str

    @field_validator('email')
    def validate_email(cls, value):
        if '@' not in value:
            raise ValueError
        value = value.lower().strip()
        return value

class Library(BaseModel):
    books: List[Book]
    users: List[User]

    def total_books(self) -> int:
        return len(self.books)

class BookNotAvailable(Exception):
    """
    Исключение, которое выбрасывается, когда книга не доступна
    """

    def __init__(self, book: Book, reason: str = "Книга временно недоступна."):
        """
        Инициализирует исключение.

        Args:
            book: Объект книги, который не доступен.
            Reason: Причина недоступности книги (по умолчанию - "Книга временно недоступна.").
        """
        super().__init__(reason)
        self.book = book
        self.reason = reason

    def __str__(self):
        """Возвращает строковое представление исключения."""
        return f"Книга '{self.book.name}' ({self.book.author}, {self.book.year}) не доступна: {self.reason}"


if __name__ == '__main__':
    user = User(name='John', email='Gwqa@a.com', membership_id='123456')
    print("This is user's info: ")
    print(user.name)
    print(user.email)
    print(user.membership_id)

    try:
        book = Book(name='The Great Gatsby', author='F. Scott Fitzgerald', year=1925, available=False,
                categories=['Classic', 'Fiction', '20th Century'])
        book.validate_available()  # Теперь вызываем метод экземпляра
        print("This is book's info: ")
        print(book.name)
        print(book.author)
        print(book.year)
        print(book.available)
        print(book.categories)
    except BookNotAvailable as e:
        print(f"Ошибка: {e}")