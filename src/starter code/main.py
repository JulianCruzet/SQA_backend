from read import read_old_bank_accounts
from write import write_new_current_accounts
from print_error import log_constraint_error
from change_account import AccountManager
from move_money import Money_manager

def read_merged_bank_transactions(file_path):
    transactions = []

    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            clean_line = line.rstrip('\n')

            if len(clean_line) != 41:
                print(f"ERROR: Line {line_num}: Invalid length ({len(clean_line)} chars)")
                continue

            try:
                # Extract fields
                transaction_code = clean_line[0:2]
                name = clean_line[3:23].strip()
                account_number = clean_line[24:29]
                amount_str = clean_line[30:38]
                misc_info = clean_line[39:41]

                # Validate transaction code
                valid_transaction_codes = {"01", "02", "03", "04", "05", "06", "07", "08", "00"}
                if transaction_code not in valid_transaction_codes:
                    print(f"ERROR: Line {line_num}: Invalid transaction code '{transaction_code}'")
                    continue

                # Validate account number
                if not account_number.isdigit():
                    print(f"ERROR: Line {line_num}: Invalid account number '{account_number}'")
                    continue

                # Validate amount format
                if (len(amount_str) != 8 or not amount_str[:-3].isdigit()):
                    print(f"ERROR: Line {line_num}: Invalid amount format '{amount_str}'")
                    continue

                # Convert numeric values
                account_number = int(account_number)
                amount = float(amount_str)

                transactions.append({
                    'transaction_code': transaction_code,
                    'name': name,
                    'account_number': account_number,
                    'amount': amount,
                    'misc_info': misc_info
                })

                # Stop processing if end-of-session code is found
                if transaction_code == "00":
                    break

            except Exception as e:
                print(f"ERROR: Line {line_num}: Unexpected error: {str(e)}")
                continue

    return transactions


def main():
    accounts = read_old_bank_accounts('master_accounts.txt')
    transactions = read_merged_bank_transactions('merged_bank_transaction.txt')
    print(accounts)
    print(transactions)
    money_manager  =Money_manager (accounts)
    account_manager = AccountManager(accounts)
    with_draw_fail = False

    for tra in transactions:
        if tra["transaction_code"] == "01":

            money_manager.withdraw(tra)

        elif  tra["transaction_code"] == "02":
            #money_manager.transfer(tra,to_account=1)
            if tra['misc_info'] == "FR":
                if not  money_manager.withdraw(tra):
                    with_draw_fail = True
            elif tra['misc_info'] == "TO" and not with_draw_fail:
                with_draw_fail = True
                money_manager.deposit(tra)

            # I just put a random account for now because the
            # transaction line does not contain the destination account
        elif tra["transaction_code"] == "03":

            money_manager.pay_bill(tra)

        elif tra["transaction_code"] == "04":

            money_manager.deposit(tra)

        elif tra["transaction_code"] == "05":
            account_manager.create_account(tra['account_number'],tra['name'],tra['amount'])
        elif tra["transaction_code"] == "06":
            account_manager.delete_account(tra['account_number'])
        elif tra["transaction_code"] == "07":
            account_manager.change_status(tra['account_number'])
        elif tra["transaction_code"] == "08":
            account_manager.change_plan(tra['account_number'])
        elif tra["transaction_code"] == "00":
            accounts=account_manager.get_accounts()
            final_accounts = list(accounts.values())
            #write_new_current_accounts(final_accounts,'master_accounts.txt')
            write_new_current_accounts(final_accounts,'current_accounts.txt')
            break
        else:
            log_constraint_error("Invalid transaction code", tra["transaction_code"])

if __name__ == "__main__":
    main()
