from print_error import log_constraint_error
from accounts import Accounts
class AccountManager(Accounts):
    def create_account(self, account_number, name, balance=0.0, plan='SP'):
        if account_number in self.accounts:
            log_constraint_error("Account already exists.",f'{account_number}  is already part of accounts')
            return
        new_account = {
            'account_number': str(account_number),
            'name': name,
            'status': 'A',
            'balance': balance,
            'total_transactions': 0,
            'plan': plan if plan in ['NP', 'SP'] else 'SP'
        }
        self.accounts[str(account_number)] = new_account
        print("Account created successfully.")

    def delete_account(self, account_number):
        if str(account_number) in self.accounts:
            del self.accounts[str(account_number)]
            print("Account deleted successfully.")
        else:
            log_constraint_error("Invalid account number",f'{account_number}  does not exist')

    def change_plan(self, account_number):
        if str(account_number) in self.accounts:
                self.accounts[str(account_number)]['plan'] = 'NP'
                print("Plan updated successfully.")
        else:
            log_constraint_error("Invalid account number",f'{account_number}  does not exist')

    def change_status(self, account_number):
        if str(account_number) in self.accounts:
            current_status = self.accounts[str(account_number)]['status']
            self.accounts[str(account_number)]['status'] = 'D' if current_status == 'A' else 'A'
            print("Status updated successfully.")
        else:
            log_constraint_error("Invalid account number",f'{account_number}  does not exist')