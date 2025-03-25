from print_error import log_constraint_error
from accounts import Accounts

class Money_manager(Accounts):
    def transfer(self,transaction,to_account):
        print("Transfer money ",10*"-")
        # print(self.accounts,"\n",transaction)
        amount = transaction['amount']
        from_account = transaction['account_number']

        if str(from_account) not  in self.accounts or str(to_account) not in self.accounts:
            log_constraint_error("Invalid account number", f'{from_account} or {to_account} not found')
            return

        from_account_final_amount = self.accounts[str(from_account)]['balance'] - amount
        if from_account_final_amount <0:
            log_constraint_error("Invalid final balance", f'{from_accountlog_constraint_error("Invalid amount","Final amount will be NEGATIVE")} or {to_account} not found')
            return
        self.accounts[str(from_account)]['balance'] = from_account_final_amount

        self.accounts[str(to_account)]['balance'] += amount


    def deposit (self,transaction):
        print("Deposit money ",10*"-")
        #print(self.accounts,"\n",transaction)

        account_number = transaction['account_number']
        #print(account_number)
        if str(account_number) not  in self.accounts:
            log_constraint_error("Invalid account number", transaction['account_number'])
            return

        self.accounts[str(account_number)]['balance'] += transaction['amount']
        #print(self.accounts,"\n",self.accounts)

    def withdraw (self,transaction):
        print("Withdraw money ",10*"-")
       # print(self.accounts,"\n",transaction)

        account_number = transaction['account_number']
        #print(account_number)
        if str(account_number) not  in self.accounts:
            log_constraint_error("Invalid account number", transaction['account_number'])
            return
        final_amount = self.accounts[str(account_number)]['balance'] - transaction['amount']
        if final_amount <0:
            log_constraint_error("Invalid amount","Final amount will be NEGATIVE")
            return
        self.accounts[str(account_number)]['balance'] = final_amount
        #print(self.accounts,"\n",self.accounts)

    def pay_bill (self,transaction):
        print("Pay Bill money ",10*"-")
        #print(self.accounts,"\n",transaction)

        account_number = transaction['account_number']
        print(account_number)
        if str(account_number) not  in self.accounts:
            log_constraint_error("Invalid account number", transaction['account_number'])
            return
        final_amount = self.accounts[str(account_number)]['balance'] - transaction['amount']
        if final_amount <0:
            log_constraint_error("Invalid amount","Final amount will be NEGATIVE")
            return
        self.accounts[str(account_number)]['balance'] = final_amount
        #print(self.accounts,"\n",self.accounts)
