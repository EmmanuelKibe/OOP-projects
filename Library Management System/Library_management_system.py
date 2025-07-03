import random
# custom module to handle database connection
from db_config import get_connection


class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False

    def __repr__(self):
        return f"{self.title} by {self.author}"


class User:
    def __init__(self, name, age, user_id):
        self.name = name
        self.age = age
        self.user_id = user_id
        self.borrowed_books = []

    def list_borrowed_books(self):
        if not self.borrowed_books:
            return "No books currently borrowed."
        return ', '.join([book.title for book in self.borrowed_books])


class Library:
    def __init__(self):
        pass
    
    def create_user_account(self):
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))

        # Generate unique user ID
        user_id = random.randint(100, 999)
        while user_id in [user.user_id for user in self.users.values()]:
            user_id = random.randint(100, 999)

        self.users[name] = User(name, age, user_id)
        print(f"Congratulations {name}! Your user ID is {user_id}")


    def add_book(self, book_name, author):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Check if book already exists (by title and author)
            cursor.execute("SELECT * FROM books WHERE title = %s AND author = %s", (book_name, author))
            if cursor.fetchone():
                print("This book already exists.")
            else:
                cursor.execute(
                    "INSERT INTO books (title, author, is_borrowed) VALUES (%s, %s, %s)",
                    (book_name, author, False)
                )
                conn.commit()
                print("Book added successfully!")

        except Exception as e:
            print("Error adding book:", e)

        finally:
            conn.close()


    def remove_book(self, title, author):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Check if book already exists (by title and author)
            cursor.execute("SELECT * FROM books WHERE title = %s AND author = %s", (title, author))
            if cursor.fetchone():
                cursor.execute("DELETE FROM books WHERE title = %s AND author = %s", (title, author))
                conn.commit()
                print("Book removed successfuly")
            else:
                print("This book does not exist")
                

        except Exception as e:
            print("Error adding book:", e)

        finally:
            conn.close()
        
    def borrow_book(self, user_id, book_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Check if user exists
            cursor.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
            if not cursor.fetchone():
                print("User not found.")
                return

            # Check if book exists
            cursor.execute("SELECT is_borrowed FROM books WHERE book_id = %s", (book_id,))
            result = cursor.fetchone()
            if not result:
                print("Book not found.")
                return

            is_borrowed = result[0]
            if is_borrowed:
                print("Book is already borrowed.")
                return

            # Check how many books this user already borrowed
            cursor.execute("SELECT COUNT(*) FROM borrowed_books WHERE user_id = %s", (user_id,))
            borrowed_count = cursor.fetchone()[0]
            if borrowed_count >= 2:
                print("Cannot borrow more than 2 books.")
                return

            # Borrow the book
            cursor.execute("INSERT INTO borrowed_books (user_id, book_id) VALUES (%s, %s)", (user_id, book_id))
            cursor.execute("UPDATE books SET is_borrowed = TRUE WHERE book_id = %s", (book_id,))
            conn.commit()

            print("Book borrowed successfully.")

        except Exception as e:
            print("Error borrowing book:", e)

        finally:
            conn.close()

    def return_book(self, user_id, book_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Check if user exists
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            if not cursor.fetchone():
                print("User not found.")
                return

            # Check if book exists
            cursor.execute("SELECT is_borrowed FROM books WHERE book_id = %s", (book_id,))
            result = cursor.fetchone()
            if not result:
                print("Book not found.")
                return

            is_borrowed = result[0]
            if not is_borrowed:
                print("This book is not currently borrowed.")
                return

            # Check if user actually borrowed this book
            cursor.execute("SELECT * FROM borrowed_books WHERE user_id = %s AND book_id = %s", (user_id, book_id))
            if not cursor.fetchone():
                print("This user did not borrow this book.")
                return

            # Delete borrow record and mark as returned
            cursor.execute("DELETE FROM borrowed_books WHERE user_id = %s AND book_id = %s", (user_id, book_id))
            cursor.execute("UPDATE books SET is_borrowed = FALSE WHERE book_id = %s", (book_id,))

            conn.commit()
            print("Book returned successfully.")

        except Exception as e:
            print("Error returning book:", e)

        finally:
            conn.close()

    def print_all_books(self):
        try:
            print("\n--- All Books in Library ---")

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT book_id, title, author, is_borrowed FROM books;")
            all_books = cursor.fetchall()

            if not all_books:
                print("There are currently no books in the library")
                return

            for book_id, title, author, is_borrowed in all_books:
                status = "Borrowed" if is_borrowed else "Available"
                print(f"ID: {book_id}, Title: '{title}', Author: {author}, Status: {status}")

        except Exception as e:
            print("Error printing all books", e)

        finally:
            conn.close()

    def print_all_users(self):
        try:
            print("\n--All registered users--")

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Users;")
            all_users = cursor.fetchall()

            for user_id, user_name, user_age in all_users:
                print(f"{user_id} - {user_name} - {user_age}")

        except Exception as e:
            print(f"Error printing all users.\n{e}")

        finally:
            conn.close()

    def show_user_borrowed_books(self, user_id):
        try:
            print("\n--Borrowed books--")

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM borrowed_books WHERE user_id = %s",(user_id,))
            borrowed_check = cursor.fetchall()
            if not borrowed_check:
                print("This user has not borrowed any books")
                return
            
            cursor.execute("SELECT borrowed_books.book_id, books.title FROM borrowed_books INNER JOIN books ON borrowed_books.book_id = books.book_id WHERE borrowed_books.user_id = %s;", (user_id,))
            borrowed_books = cursor.fetchall()
            for book in borrowed_books:
                book_id, title = book
                print(f"{book_id} - {title}")

        except Exception as e:
            print("Error in fetching borrowed books", e)

        finally:
            conn.close()
            
        
cursor = Library()

cursor.add_book('Pachinko', 'Min Jin Lee')
