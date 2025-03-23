from read import read_merged_bank_transactions
from read import read_old_bank_accounts
from write import write_new_current_accounts
from print_error import log_constraint_error
from change_account import AccountManager
from move_money import Money_manager


def main():
    accounts = read_old_bank_accounts('master_accounts.txt')
    transactions = read_merged_bank_transactions('merged_bank_transaction.txt')
    print(accounts)
    print(transactions)
    money_manager  =Money_manager (accounts)
    account_manager = AccountManager(accounts)
    for tra in transactions:
        if tra["transaction_code"] == "01":

            money_manager.withdraw(tra)

        elif  tra["transaction_code"] == "02":
            money_manager.transfer(tra,to_account=1)
            # I just put a random account for now because the
            # transaction line does not contain the destination account
        elif tra["transaction_code"] == "03":

            money_manager.pay_bill(tra)

        elif tra["transaction_code"] == "04":

            money_manager.deposit(tra)

        elif tra["transaction_code"] == "05":
            account_manager.create_account(tra['account_number'],tra['name'],tra['amount'])
            print(5)
        elif tra["transaction_code"] == "06":
            account_manager.delete_account(tra['account_number'])
            print(6)
        elif tra["transaction_code"] == "07":
            account_manager.change_status(tra['account_number'])
            print(7)
        elif tra["transaction_code"] == "08":
            account_manager.change_plan(tra['account_number'])
            print(8)
        elif tra["transaction_code"] == "00":
            break
        else:
            log_constraint_error("Invalid transaction code", tra["transaction_code"])

if __name__ == "__main__":
    main()
