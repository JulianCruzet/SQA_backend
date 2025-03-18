def read_old_bank_accounts(file_path):
    """
    Reads and validates the bank account file format
    Returns list of accounts and prints fatal errors for invalid format
    """
    accounts = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            # Remove newline but preserve other characters
            clean_line = line.rstrip('\n')
            
            # Validate line length
            if len(clean_line) != 42:
                print(f"ERROR: Fatal error - Line {line_num}: Invalid length ({len(clean_line)} chars)")
                continue

            try:
                # Extract fields with positional validation
                account_number = clean_line[0:5]
                name = clean_line[6:26]  # 20 characters
                status = clean_line[27]
                balance_str = clean_line[29:37]  # 8 characters
                transactions_str = clean_line[38:42]  # 4 characters

                # Validate account number format (5 digits)
                if not account_number.isdigit():
                    print(f"ERROR: Fatal error - Line {line_num}: Invalid account number format")
                    continue

                # Validate status
                if status not in ('A', 'D'):
                    print(f"ERROR: Fatal error - Line {line_num}: Invalid status '{status}'")
                    continue

                # Validate balance format (XXXXX.XX)
                if (len(balance_str) != 8 or 
                    balance_str[5] != '.' or 
                    not balance_str[:5].isdigit() or 
                    not balance_str[6:].isdigit()):
                    print(f"ERROR: Fatal error - Line {line_num}: Invalid balance format")
                    continue

                # Validate transaction count format
                if not transactions_str.isdigit():
                    print(f"ERROR: Fatal error - Line {line_num}: Invalid transaction count format")
                    continue

                # Convert numerical values
                balance = float(balance_str)
                transactions = int(transactions_str)

                # Validate business constraints
                if balance < 0:
                    print(f"ERROR: Fatal error - Line {line_num}: Negative balance")
                    continue
                if transactions < 0:
                    print(f"ERROR: Fatal error - Line {line_num}: Negative transaction count")
                    continue

                accounts.append({
                    'account_number': account_number.lstrip('0') or '0',
                    'name': name.strip(),
                    'status': status,
                    'balance': balance,
                    'total_transactions': transactions
                })

            except Exception as e:
                print(f"ERROR: Fatal error - Line {line_num}: Unexpected error: {str(e)}")
                continue

    return accounts


def read_merged_bank_transactions(file_path):
    transactions = []

    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            clean_line = line.rstrip('\n')

            if len(clean_line) != 40:
                print(f"ERROR: Line {line_num}: Invalid length ({len(clean_line)} chars)")
                continue

            try:
                # Extract fields
                transaction_code = clean_line[0:2]
                name = clean_line[3:23].strip()
                account_number = clean_line[24:29]
                amount_str = clean_line[30:38]
                misc_info = clean_line[39:40]

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
                if (len(amount_str) != 8 or not amount_str[:-3].isdigit() or amount_str[-3:] != ".00"):
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

