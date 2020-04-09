import sqlite3
from book import *

connection = sqlite3.connect("./library.db")

cursor = connection.cursor()

def set_up_table():
    cursor.execute("DROP TABLE IF EXISTS books")
    cursor.execute("""
    CREATE TABLE books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        published_year INTEGER, 
        is_loaned INTEGER)
    """)
# sqlite3 doesn't support booleans, therefore an integer 1,0 is used
    connection.commit()

def insert_book(title, author, published_year, is_loaned):
    sql = f"""
        INSERT INTO books (title, author, published_year, is_loaned)
        VALUES ("{title}", "{author}", {published_year}, {is_loaned})
    """
    cursor.execute(sql)
    connection.commit()

def get_all_books():
    sql = "SELECT * FROM books"
    rows = cursor.execute(sql)
    book_rows = rows.fetchall()
    return [Book(*book_row) for book_row in book_rows]

def book_by_title(title):
    sql = f"SELECT * FROM books WHERE title = '{title}'"
    row = cursor.execute(sql)
    book_row = row.fetchone()
    if book_row is None:
        return None
    return Book(*book_row)

def update_book(id, loaned):
    sql = f"UPDATE books SET is_loaned={loaned} WHERE id = {id}"
    cursor.execute(sql)
    connection.commit()

set_up_table()
insert_book("Hingmy", "yerda", 2020, 1)
insert_book("V for Vendetta", "Alan Moore", 1980, 0)   

choice = ""
while choice.casefold() != "q":
    print("""
    Select an option:
    1. List all books
    2. Search for a book
    3. Update loaned status of a book
    """)
    choice = input()

    if choice == "1":
        all_books = get_all_books()
        loan_status = None

        for book in all_books:
            if book.is_loaned == 0:
                loan_status = False
            else:
                loan_status = True
            print(f"Book {book.id}: {book.title} by {book.author}, published in {book.published_year}. Currently loaned: {loan_status}")
    elif choice == "2":
        print("Enter book title: ")
        book = input()
        found = book_by_title(book)
        if found is None:
            print("Book not found")
        else:
            loan_status = None
            if found.is_loaned == 0:
                loan_status = False
            else:
                loan_status = True
            print(f"Book {found.id}: {found.title} by {found.author}, published in {found.published_year}. Currently loaned: {loan_status}")
    elif choice == "3":
        print("Enter book to update: ")
        book = input()
        print("Enter loaned status - 1 for loaned, 0 for available")
        loan_status = input()
        found = book_by_title(book)
        if found is None:
            print("Book not found")
        else:
            update_book(found.id,loan_status)
            found = book_by_title(book)

            if found.is_loaned == 0:
                loan_status = False
            else:
                loan_status = True
            print(f"Book {found.id}: {found.title} by {found.author}, published in {found.published_year}. Currently loaned: {loan_status}")



