import account_utils

class moveMoney:
    account_holder = ''
    account_number = 0
    balance = 1000.00
    
    
    
    def transfer(self):
        accounts = account_utils.read_bank_accounts()
        transferTo = 0
        transferFrom = 0
        transferAmount = 0.0
        

        amountCheck = False
    
        #Get account holder name and find the account
        self.account_holder = input("Enter account holder ")
        account = account_utils.find_account(accounts, self.account_holder)
        # if not account:
        #     print('Error: Account holder does not exist')
        #     return False,''
        

        #User enters account number whom they want money transferred to/from
        self.transferfrom = input("enter account number to transfer from ")
        if self.transferfrom != account["account_number"]:
            print("Error: Account number does not match account holder.")
            return False, ''
        self.transferto = input("enter account number to transfer to ")
        # if not account_utils.find_account_by_number(accounts,self.transferto):
        #     print("Error: Account number does not exist.")
        #     return None, ""

        print(f"balance value: {account['balance']}")

        #Checks if amount inputted is within limit
        while (not amountCheck):
            self.transferAmount = float(input("enter amount to transfer "))
            
            if (self.transferAmount > self.balance and self.transferAmount > 1000):
                print("transferred failed! Please enter transfer value less than 1000")
                transferAmount = 0.0
                amountCheck = False

            elif (self.transferAmount > self.balance or self.transferAmount > 1000):
                print("Try again!")
                transferAmount = 0.0
                amountCheck = False
            
            else:
                amountCheck = True
       
        for account in accounts:
            if account["account_number"].lower() == self.transferto.lower():
                account["balance"] = account["balance"] + float(self.transferAmount)
               
            if account["account_number"].lower() == self.transferfrom.lower():
                account["balance"] = account["balance"] - float(self.transferAmount)
                
        account_utils.update_bank_accounts(accounts)
        print("Transfer accepted")
        # Format both lines
        sender_line = f"02 {self.account_holder.ljust(20)} {self.transferfrom.zfill(5)} {format(self.transferAmount, '08.2f')} FR"
        receiver_line = f"02 {self.transferto.ljust(20)} {self.transferto.zfill(5)} {format(self.transferAmount, '08.2f')} TO"

        return True, f"{sender_line}\n{receiver_line}"

        
    def pay_bill(self):
        accounts = account_utils.read_bank_accounts()
        company = ''
        companyCheck = False
        payAmount = 0

        amountCheck = False

        #User enters account holder
        self.account_holder = input("Enter account holder ")
        account = account_utils.find_account(accounts, self.account_holder)
        if not account:
            print('Error: User name does not exist.')
            return False,""
        
        #User enters account number
        self.account_number = input("Enter account number ")
        if int(self.account_number) != int(account["account_number"]):
            print("Error: Account number does not match account holder.")
            return False,""

        #Checks if company inputted is on the list
        while (not companyCheck):
            self.company = input("enter company: ")

            if (self.company.upper() != "EC" and self.company.upper() != "CQ" and self.company.upper() != "FI"):
                print("Company initials is invalid, try again!")
                companyCheck = False

            else:
                companyCheck = True


        # print(f"balance value: {self.balance}")

        #Checks if amount inputted is within limit
        while (not amountCheck):
            self.payAmount = int(input("enter bill "))
            
            if (self.payAmount > self.balance and self.payAmount > 2000):
                print("Bill input is over 2000, it must be less than that!")
                payAmount = 0
                amountCheck = False

            elif (self.payAmount > self.balance or self.payAmount > 2000):
                print("Try again!")
                payAmount = 0
                amountCheck = False
            
            else:
                amountCheck = True
            
        
        account["balance"] = account["balance"] - float(self.payAmount)

        print(f'{self.payAmount} bill sent to account {self.company}')

        
        account_utils.update_bank_accounts(accounts)
        #f"03 {self.account_holder.ljust(20)} {self.account_number} {str(self.payAmount).zfill(8)}"

        return True, f"03 {self.account_holder.ljust(20)} {str(self.account_number).zfill(5)} {format(self.payAmount, '08.2f')} NA"


    def deposit(self):
        accounts = account_utils.read_bank_accounts()
        depositAmount = 0.0

        #User enters account holder
        self.account_holder = input("enter account holder ")
        account = account_utils.find_account(accounts, self.account_holder)
        if not account:
            print('Error: User name does not exist.')
            return False,""

        #User enters account number
        self.account_number = input("enter account number ")
        if int(self.account_number) != int(account["account_number"]):
            print("Error: Account number does not match account holder.")
            return False,""

        self.depositAmount = input("enter amount to deposit ")

        
        account["balance"] = account["balance"] + float(self.depositAmount)

        print(f'{self.depositAmount} deposited into account {self.account_number}')
        account_utils.update_bank_accounts(accounts)
        #f"04 {self.account_holder.ljust(20)} {self.account_number} {str(account['balance']).zfill(8)}"
        return True, f"04 {self.account_holder.ljust(20)} {str(self.account_number).zfill(5)} {format(account['balance'], '08.2f')} NA"


    def withdraw(self):
        accounts = account_utils.read_bank_accounts()
        withdrawAmount = 0
        amountCheck = False

        # User enters account holder
        self.account_holder = input("Enter account holder: ")
        account = account_utils.find_account(accounts, self.account_holder)
        if not account:
            print('Error: User name does not exist.')
            return False,""
        
        # User enters account number
        self.account_number = int(input("Enter account number: "))
        print(self.account_number,account['account_number'])
        
        if self.account_number != int(account["account_number"]):
            print("Error: Account number does not match account holder.")
            return False,""

        # Checks if withdrawal amount is within limit
        while not amountCheck:
            self.withdrawAmount = float(input("Enter withdrawal amount: "))
            
            if self.withdrawAmount > 2000:
                print("Withdrawal amount exceeds $2000 limit. Try again!")
                withdrawAmount = 0
                amountCheck = False
            
            elif self.withdrawAmount > account["balance"]:
                print("Insufficient balance! Try again.")
                withdrawAmount = 0
                amountCheck = False
            
            else:
                amountCheck = True
     
        account["balance"] -= self.withdrawAmount

        print(f'${self.withdrawAmount} withdrawn from account {self.account_number}.')
        
        account_utils.update_bank_accounts(accounts)
        
        return True, f"01 {self.account_holder.ljust(20)} {str(self.account_number).zfill(5)} {format(self.withdrawAmount, '08.2f')} NA"


