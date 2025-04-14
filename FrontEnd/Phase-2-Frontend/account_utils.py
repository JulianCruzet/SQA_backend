def read_bank_accounts():
    """Simulates reading the current bank accounts file."""
    # print("Reading bank accounts file...")
    accounts = []

    with open('accounts.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line == "END_OF_FILE":
                break  # Stop reading when we reach the END_OF_FILE marker
            
            parts = line.split()
            if len(parts) != 4:
                print(f"Skipping malformed line: {line}")
                continue

            account_info = {
                "account_number": parts[0],
                "account_name": parts[1],
                "status": parts[2],  # 'A' for Active, 'D' for Disabled
                "balance": float(parts[3])  # Convert balance to a float
            }

            accounts.append(account_info)
    
    return accounts

def find_account_by_name(accounts, name):
    for account in accounts:
        if account["account_name"].lower() == name.lower():  # Case-insensitive comparison
            return True # Return the account details if found
    return False

def find_account_by_number(accounts, number):
    for account in accounts:
        if account["account_number"] == number:  # Case-insensitive comparison
            return True # Return the account details if found
    return False

def find_account(accounts, name):
    for account in accounts:
        if account["account_name"].lower() == name.lower():  # Case-insensitive comparison
            return account  # Return the account details if found
    return None  # Return None if not found

def update_bank_accounts(accounts):
    """Rewrites the 'accounts.txt' file with the updated accounts list."""
    with open('accounts.txt', 'w') as file:
        for account in accounts:
            line = f"{account['account_number']} {account['account_name']} {account['status']} {str(account['balance']).zfill(8)}\n"
            file.write(line)
        file.write("END_OF_FILE\n")  