from read import read_merged_bank_transactions
from read import read_old_bank_accounts
from write import write_new_current_accounts
from print_error import log_constraint_error

accounts=read_old_bank_accounts('master_accounts.txt')
transactions=read_merged_bank_transactions('merged_bank_transaction.txt')
print(accounts)
print(transactions)
