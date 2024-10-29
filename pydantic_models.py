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
        return value

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





if __name__ == '__main__':
    user = User(name='John', email='Gwqa@a.com', membership_id='123456')
    print("This is user's info: ")
    print(user.name)
    print(user.email)
    print(user.membership_id)

    book = Book(name='The Great Gatsby', author='F. Scott Fitzgerald', year=1925, available=True)
    print("This is book's info: ")
    print(book.name)
    print(book.author)
    print(book.year)
    print(book.available)