from requests import get
from pydantic import BaseModel
from typing import Optional
from typing import List


GBOOKS_URL = 'https://www.googleapis.com/books/v1/volumes?q={}'
# rating path = <id>/volumeInfo/readingModes/averageRating


# book class for parsing json
class Book(BaseModel):
    title: Optional[str]
    authors: Optional[List[str]]
    averageRating: Optional[float]


# turn " " into "+"
def format_book_name(book_name: str) -> str:
    return ''.join([letter if letter != " " else "+" for letter in book_name])


# send request to google books api
def get_book_by_name(book_name: str) -> dict:
    return get(GBOOKS_URL.format(book_name)).json()


# return all found books as Book classes
def get_book_info(book_name: str) -> List[Book]:
    formatted_book_name = format_book_name(book_name)
    books_json = get_book_by_name(formatted_book_name)
    hit_count = len(books_json["items"])
    for hit in range(hit_count):
        yield Book(**books_json["items"][hit]["volumeInfo"])

    




def main():
    for book in get_book_info("harry potter"):
        if book.averageRating:
            print(f'title: {book.title}, rating: {book.averageRating}, authors: {book.authors}')



if __name__ == '__main__':
    main()