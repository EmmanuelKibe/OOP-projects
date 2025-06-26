class Account:
    def __init__(self, account_number, owner_name, _balance):
        self.account_number = account_number
        self.owner_name = owner_name
        self._balance = _balance
    
    #deposit money
    def deposit(self, amount):
        self._balance += amount
        return f"Transaction successful!\nYou have deposited Ksh{amount} into account {self.account_number}. The balance is {self._balance}."
        
    #withdraw amount
    def withdraw(self, amount):
        if amount > self._balance:
            print("You have insufficient balance to complete this withdrawal transaction!")
        else:
            self._balance -= amount
            return f"Transaction successful!\nYou have withdrawn Ksh{amount} from account {self.account_number}. The balance is {self._balance}."
    
    #get balance  
    @property
    def balance(self):
        return f"Balance for account: {self.account_number} is {self._balance}"
        
    @balance.setter
    def balance(self, amount):
        self._balance = amount
    
    def __repr__(self):
        return f"Account('{self.account_number}', '{self.owner_name}', '{self._balance}')"
        
    def __str__(self):
        return f"Account no: {self.account_number}, Recipient: {self.owner_name}, Balance: {self._balance}"
        
#Savings account
class Savings_account(Account):
    def __init__(self, account_number, owner_name, _balance, interest_rate):
        super().__init__(account_number, owner_name, _balance)
        self.interest_rate = interest_rate
        
    def apply_interest(self):
        self._balance *= self.interest_rate
        
class CheckingAccount(Account):
    def __init__(self, account_number, owner_name, _balance, overdraft_limit):
        super().__init__(account_number, owner_name, _balance)
        self.overdraft_limit = overdraft_limit
        
    #withdraw amount
    def withdraw(self, amount):
        amount_withdrawable = self._balance + self.overdraft_limit
        if amount > amount_withdrawable:
            print("You have insufficient balance and credit to complete this withdrawal transaction!")
        else:
            self._balance -= amount
            return f"Transaction successful!\nYou have withdrawn Ksh.{amount} from account {self.account_number}. The balance is Ksh.{self._balance}."    

import random

class BankSystem:
    def __init__(self):
        self.bank_accounts = {'John Maina': 10029873, 'Jane Doe': 10029874, 'Alice Smith': 10029875}

    def create_account(self):
        owner_name = input("Enter your name and surname: ")
        suffix = random.randint(1000, 9999)
        account_number = int(f"100{suffix}")
        while account_number in self.bank_accounts.values():
            suffix = random.randint(1000, 9999)
            account_number = int(f"100{suffix}")
        self.bank_accounts[owner_name] = account_number
        print(f"Congratulations {owner_name}! Your account number is {account_number}")

    def print_all_accounts(self):
        if not self.bank_accounts:
            print("No accounts have been created yet.")
        else:
            print("All bank accounts:")
            for name, number in self.bank_accounts.items():
                print(f"{name}: {number}")

    #find account
    def find_account(self, account_number):
        for name, number in self.bank_accounts.items():
            if number == account_number:
                print(f"Found: {name} — Account Number: {number}")
                return
        print("The account number does not exist.")


        
         
        
""" savings_account1 = CheckingAccount(10029873, 'John Pombe', 8976, 5000)
savings_account1.balance = 10000
print(savings_account1.withdraw(11000)) """

bank1 = BankSystem()
bank1.print_all_accounts()
bank1.find_account(10029873)