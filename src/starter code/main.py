from read import read_merged_bank_transactions
from read import read_old_bank_accounts
from write import write_new_current_accounts
from print_error import log_constraint_error
from change_account import AccountManager




def main():
    accounts = read_old_bank_accounts('master_accounts.txt')
    transactions = read_merged_bank_transactions('merged_bank_transaction.txt')
    print(accounts)
    print(transactions)
    for tra in transactions:
        if tra["transaction_code"] == "01":
            print(1)


        elif  tra["transaction_code"] == "02":
            print(2)
        elif tra["transaction_code"] == "03":
            print(3)
        elif tra["transaction_code"] == "04":
            print(4)
        elif tra["transaction_code"] == "05":
            create_transaction=AccountManager(accounts)
            create_transaction.create_account(tra['account_number'],tra['name'],tra['amount'])
            accounts=create_transaction.get_accounts()
            print(accounts)
        elif tra["transaction_code"] == "06":
            print(6)
        elif tra["transaction_code"] == "07":
            print(7)
        elif tra["transaction_code"] == "08":
            print(8)
        elif tra["transaction_code"] == "00":
            break
        else:
            log_constraint_error("Invalid transaction code", tra["transaction_code"])

if __name__ == "__main__":
    main()
