import sys
import account_utils

def write_transactions(transactions):
    """Simulates writing the transaction log to a file."""
    file_path = '../../src/merged_bank_transaction.txt'
    with open(file_path, 'w') as file:
        for transaction in transactions:
            file.write(f"{transaction}\n")

        file.write('00                      00000 00000.00 NA')

class Login:
    # This class is used to hold information of the current login session S
    def __init__(self):
        self.logged_in = False
        self.admin_mode = False
        self.account_holder = ""
        self.transactions = []
        self.start_session()
    
    def start_session(self):
        while not self.logged_in:
            print("Welcome to the banking system")
            session_type = input("enter the session type: ").strip().lower()
            
            if session_type not in ["standard", "admin"]:
                print("Invalid session type. Please enter 'Standard' or 'Admin'.")
                continue
            
            if session_type == "standard":
            
                name = input("Enter account holder's name: ").strip()
                if not name:
                    print("Account holder's name is required for Standard login.")
                    continue
                found = False
                accounts = account_utils.read_bank_accounts()
                
                if account_utils.find_account_by_name(accounts,name):  
                    self.account_holder = name 
                    found = True
                    self.logged_in = True
                if not found:
                    print('error: user name does not exist')
                       
            else:
                  
                self.logged_in = True
                self.admin_mode = session_type == "admin"
                print("login success")
                # print(f"Login Successful: Welcome {self.account_holder if self.account_holder else 'Admin'} ({session_type.capitalize()})!")
    
    def logout(self):
        if not self.logged_in:
            print("Error: You are not logged in.")
            return
        
        # Write transaction file before logout (Assume write_transactions() is implemented)
        write_transactions(self.transactions)
        
        print("session terminated")
        self.logged_in = False
        self.admin_mode = False
        self.account_holder = ""
        self.transactions.clear()
