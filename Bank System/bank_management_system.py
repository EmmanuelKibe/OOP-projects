import random

# Base Account class
class Account:
    def __init__(self, account_number, owner_name, _balance):
        self.account_number = account_number
        self.owner_name = owner_name
        self._balance = _balance

    # Deposit money
    def deposit(self, amount):
        self._balance += amount
        return f"Transaction successful!\nYou have deposited Ksh{amount} into account {self.account_number}. The balance is {self._balance}."

    # Withdraw money
    def withdraw(self, amount):
        if amount > self._balance:
            return "You have insufficient balance to complete this withdrawal transaction!"
        else:
            self._balance -= amount
            return f"Transaction successful!\nYou have withdrawn Ksh{amount} from account {self.account_number}. The balance is {self._balance}."

    # Get balance using property
    @property
    def balance(self):
        return f"Balance for account: {self.account_number} is Ksh{self._balance}"

    @balance.setter
    def balance(self, amount):
        self._balance = amount

    def __repr__(self):
        return f"Account('{self.account_number}', '{self.owner_name}', '{self._balance}')"

    def __str__(self):
        return f"Account No: {self.account_number} | Owner: {self.owner_name} | Balance: Ksh{self._balance}"

# Savings Account subclass
class SavingsAccount(Account):
    def __init__(self, account_number, owner_name, _balance, interest_rate):
        super().__init__(account_number, owner_name, _balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        self._balance += self._balance * self.interest_rate
        return f"Interest applied. New balance is Ksh{self._balance}"

# Checking Account subclass
class CheckingAccount(Account):
    def __init__(self, account_number, owner_name, _balance, overdraft_limit):
        super().__init__(account_number, owner_name, _balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        max_withdrawable = self._balance + self.overdraft_limit
        if amount > max_withdrawable:
            return "You have insufficient balance and credit to complete this withdrawal transaction!"
        else:
            self._balance -= amount
            return f"Transaction successful!\nYou have withdrawn Ksh{amount} from account {self.account_number}. The balance is Ksh{self._balance}."

# Bank System
class BankSystem:
    def __init__(self):
        self.bank_accounts = {
            'John Maina': Account(10029873, 'John Maina', 0),
            'Jane Doe': Account(10029874, 'Jane Doe', 0),
            'Alice Smith': Account(10029875, 'Alice Smith', 0)
        }

    def create_account(self):
        owner_name = input("Enter your name and surname: ")

        # Generate unique account number
        suffix = random.randint(1000, 9999)
        account_number = int(f"100{suffix}")
        while account_number in [acc.account_number for acc in self.bank_accounts.values()]:
            suffix = random.randint(1000, 9999)
            account_number = int(f"100{suffix}")

        self.bank_accounts[owner_name] = Account(account_number, owner_name, 0)
        print(f"Congratulations {owner_name}! Your account number is {account_number}")

    def print_all_accounts(self):
        if not self.bank_accounts:
            print("No accounts have been created yet.")
        else:
            print("All bank accounts:")
            for account in self.bank_accounts.values():
                print(account)

    def find_account(self, account_number):
        for account in self.bank_accounts.values():
            if account.account_number == account_number:
                print(f"Found: {account}")
                return account
        print("The account number does not exist.")
        return None
    
    def transfer(self, from_acc, to_acc, amount):
        sender = self.find_account(from_acc)
        receiver = self.find_account(to_acc)
        if not sender or not receiver:
            return "One or both accounts don't exist"
            
        if sender._balance < amount:
            return f"There is not enough balance to send {amount}!"
        else:
            sender.withdraw(amount)
            receiver.deposit(amount)
            return f"Transaction successful!\nSender balance: {sender._balance}, Receiver balance: {receiver._balance}"



        
""" savings_account1 = CheckingAccount(10029873, 'John Pombe', 8976, 5000)
savings_account1.balance = 10000
print(savings_account1.withdraw(11000)) """

bank = BankSystem()
#print(bank.transfer(10029873, 10029875, 100))
bank.find_account(10029875)