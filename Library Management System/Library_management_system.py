import random

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
        if book_name in self.books:
            print("This book already exists.")
        else:
            self.books[book_name] = Book(book_name, author)
            print("Book added successfully!")

    def remove_book(self, book_name):
        if book_name in self.books:
            del self.books[book_name]
            print(f"'{book_name}' removed from the library.")
        else:
            print("This book does not exist.")

    def borrow_book(self, user_name, book_title):
        user = self.users.get(user_name)
        book = self.books.get(book_title)

        if not user:
            print("User not found.")
            return
        if not book:
            print("Book not found.")
            return
        if book.is_borrowed:
            print(f"'{book.title}' is already borrowed.")
            return
        if len(user.borrowed_books) >= 2:
            print("You cannot borrow more than 2 books.")
            return

        user.borrowed_books.append(book)
        book.is_borrowed = True
        print(f"{user.name} has borrowed '{book.title}'.")

    def return_book(self, user_name, book_title):
        user = self.users.get(user_name)
        book = self.books.get(book_title)

        if not user:
            print("User not found.")
            return
        if not book:
            print("Book not found in the library catalog.")
            return
        if book not in user.borrowed_books:
            print(f"{user.name} didn't borrow this book.")
            return

        user.borrowed_books.remove(book)
        book.is_borrowed = False
        print(f"{user.name} has returned '{book.title}'.")

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
cursor.show_user_borrowed_books('Emmanuel')