#Library management system
import random
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        
    def __repr__(self):
        return(f"{self.title}, {self.author}")
        
class User:
    def __init__(self, name, age, user_id):
        self.name = name
        self.age = age
        self.user_id = user_id
        self.borrowed_books = []
        
    def borrow_book(self, book_name):
        if len(self.borrowed_books) > 2:
            print("You cannot borrow more than 2 books")
        else:
            self.borrowed_books.append(book_name)
            print(f"You have successfully borrowed {book_name}")
            
    def return_book(self, book_name):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book_name)
            print(f"You have successfully returned {book_name}")
        else:
            print(f"You did not borrow {book_name}")
            
class Library:
    def __init__(self):
        self.users = {
            'Emmanuel' : User('Emmanuel', 20, 456),
            'John' : User('John', 28, 234),
            'Alice' : User('Alice', 19, 364)
        }
        self.books = {"The Great Gatsby" : "Scott F Fitzgerald", "Pachinko" : "Min Jin Lee", "A little lie" : "Max Turner", "Say you'll remember me" : "Abby Jimenez", "Vicious" : "L.J.Shen"}
        
    def create_user_account(self):
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        
        #generate a user id
        user_id = random.randint(100, 1000)
        while user_id in [user.user_id for user in self.users.values()]:
            user_id = random.randint(100, 1000)
            
        self.users[name] = User(name, age, user_id)
        print(f"Congratulations {name}! Your user ID is {user_id}")
        
    def add_book(self, book_name, author):
        if book_name in self.books.items():
            print(f"This book already exists")
        else:
            self.books[book_name] = Book(book_name, author)
            print("Book added successfully!")
            
    def remove_book(self, book_name):
        if book_name in self.books.items():
            self.books.remove(book_name)
        else:
            print("This book does not exist")
            
    def print_all_books(self):
        print("\n---All books---")
        for name, author in self.books.items():
            print(f"{name} - {author}")
            
            
        
book1 = Library()
book1.add_book("Harry Potter", "J.K.Rowling")
#book1.print_all_books()
print(book1)