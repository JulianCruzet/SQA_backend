import account_utils

class removeAccount:
    def __init__(self):
        self.account_holder = ''
        self.account_number = ''
        self.balance = 0
        self.active = True
        self.transaction_file_line = ''

    def delete(self):
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

        # Check if the account is already disabled
        if account["status"] == "D":
            print("Error: Cannot delete a disabled account.")
            return None

        # Set balance and remove account from the list
        self.balance = account["balance"]
        accounts.remove(account)

        # Update accounts.txt
        account_utils.update_bank_accounts(accounts)

        self.transaction_file_line = self.transaction_file_line = f"06 {self.account_holder.ljust(20)} {str(self.account_number).zfill(5)} {format(self.balance, '08.2f')} NA"

        print(f'Account {self.account_number} deleted successfully.')

        return self.transaction_file_line

    def disable(self):
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

        # Check if the account is already disabled
        if account["status"] == "D":
            print("Error: Account is already disabled.")
            return None

        # Update status to disabled
        account["status"] = "D"
        account_utils.update_bank_accounts(accounts)

        self.transaction_file_line = f"07 {self.account_holder.ljust(20)} {str(self.account_number).zfill(5)} {format(account['balance'], '08.2f')} NA"

        print(f'Account {self.account_number} disabled successfully.')

        return self.transaction_file_line

