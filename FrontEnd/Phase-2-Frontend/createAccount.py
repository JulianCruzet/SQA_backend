import account_utils

class CreateAccount:
    def __init__(self, account_file='accounts.txt'):
        # Initialize with a specified account file and calculate the next account number.
        self.account_file = account_file
        self.next_account_number = self.get_next_account_number()

    def get_next_account_number(self):
        """Retrieve the next account number by reading the last entry in the account file."""
        accounts = account_utils.read_bank_accounts()
        if len(accounts)<1:
            return 1
        
        lastAccount = int(accounts[-1]["account_number"])
        return lastAccount +1
        
        

    def create(self):
        """Create a new bank account by prompting the user for account details and appending to the account file."""
        account_holder = input("Enter account holder: ").ljust(20)
        initial_balance = float(input("Enter an initial balance: "))  
        formatted_balance = f"{initial_balance:08.1f}"  

        account_number = str(self.next_account_number).zfill(5)  
        account_info = f"{account_number} {account_holder} A {formatted_balance}"  

        
        with open(self.account_file, 'r+') as file:
            lines = file.readlines()
            if lines and lines[-1].strip() == 'END_OF_FILE':
                lines = lines[:-1]  

            file.seek(0)  
            file.writelines(lines)  
            file.truncate()  
            
            file.write(account_info + '\n') 
            file.write("END_OF_FILE\n")  

        #  account created successfully 
        print(f'Account {account_number} was created with initial balance {formatted_balance}')
        self.next_account_number += 1  
        self.transaction_file_line = "05 " + str(account_holder).ljust(20) + " " + account_number + " " + str(initial_balance).zfill(8) 
        self.account_info = account_number + ' ' + account_holder + ' A ' + str(initial_balance)
        
        return account_info
    
    def change_plan(self):
        accounts = account_utils.read_bank_accounts()
        
        # Get account holder name and find the account
        self.account_holder = input("Enter account holder: ").strip()
        account = account_utils.find_account(accounts, self.account_holder)
        
        if not account:
            print('Error: User name does not exist.')
            return None

        # Get account number and validate it matches the found account
        self.account_number = input("Enter account number: ").strip()
        if self.account_number != account["account_number"]:
            print("Error: Account number does not match account holder.")
            return None
        self.payment_plan = 'NP'

        #get balance from account file
        #update to current account file
        #add transaction line to file
        self.transaction_file_line = "08 " + str(self.account_holder).ljust(20) + " " + self.account_number + " " + str(account['balance']).zfill(8) + " " + self.payment_plan
        self.account_info = self.account_number + ' ' + self.account_holder + ' A ' + str(account['balance'])
        
        print(f'account {self.account_number} status has been change to NP')
        return self.transaction_file_line
    

#create a new account
# account_create = CreateAccount()
# account_create.create()
