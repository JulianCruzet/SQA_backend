class Accounts:
    def __init__(self, accounts):
        self.accounts = {acc['account_number']: acc for acc in accounts}

    def get_accounts(self):
        return self.accounts