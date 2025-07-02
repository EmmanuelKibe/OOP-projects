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
        self.users = {
            'Emmanuel': User('Emmanuel', 20, 456),
            'John': User('John', 28, 234),
            'Alice': User('Alice', 19, 364)
        }

        self.books = {
            "The Great Gatsby": Book("The Great Gatsby", "Scott F Fitzgerald"),
            "Pachinko": Book("Pachinko", "Min Jin Lee"),
            "A Little Lie": Book("A Little Lie", "Max Turner"),
            "Say You'll Remember Me": Book("Say You'll Remember Me", "Abby Jimenez"),
            "Vicious": Book("Vicious", "L.J. Shen")
        }

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


    def remove_book(self, book_name):
        if book_name in self.books:
            del self.books[book_name]
            print(f"'{book_name}' removed from the library.")
        else:
            print("This book does not exist.")


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
        print("\n--- All Books in Library ---")
        for book in self.books.values():
            print(book)

    def print_all_users(self):
        print("\n--- Registered Users ---")
        for user in self.users.values():
            print(f"{user.name} (ID: {user.user_id}, Age: {user.age})")

    def show_user_borrowed_books(self, user_name):
        user = self.users.get(user_name)
        if not user:
            print("User not found.")
            return
        print(f"{user.name}'s borrowed books: {user.list_borrowed_books()}")

            
            
        
cursor = Library()
""" cursor.borrow_book(456, 1)  
cursor.borrow_book(456, 3)  """
cursor.return_book(456, 1) 
