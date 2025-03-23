class AccountManager:
    def __init__(self, accounts):
        self.accounts = {acc['account_number']: acc for acc in accounts}  # Store accounts by account_number

    def create_account(self, account_number, name, balance=0.0, plan='SP'):
        if account_number in self.accounts:
            print("Account already exists.")
            return
        new_account = {
            'account_number': account_number,
            'name': name,
            'status': 'A',
            'balance': balance,
            'total_transactions': 0,
            'plan': plan if plan in ['NP', 'SP'] else 'SP'
        }
        self.accounts[account_number] = new_account
        print("Account created successfully.")

    def delete_account(self, account_number):
        if str(account_number) in self.accounts:
            del self.accounts[str(account_number)]
            print("Account deleted successfully.")
        else:
            print("Account not found.")

    def change_plan(self, account_number):
        if str(account_number) in self.accounts:
                self.accounts[str(account_number)]['plan'] = 'NP'
                print("Plan updated successfully.")
        else:
            print("Account not found.")

    def change_status(self, account_number):
        if str(account_number) in self.accounts:
            current_status = self.accounts[str(account_number)]['status']
            self.accounts[str(account_number)]['status'] = 'D' if current_status == 'A' else 'A'
            print("Status updated successfully.")
        else:
            print("Account not found.")
    def get_accounts(self):
        return self.accounts

    def display_accounts(self):
        for acc in self.accounts.values():
            print(acc)