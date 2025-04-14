import pytest
from move_money import Money_manager
from print_error import log_constraint_error


@pytest.fixture
def setup_accounts():
    # this is causing issues
    accounts = {
        "12345": {"balance": 100.00},
        "67890": {"balance": 50.00}
    }
    accounts =[{'account_number': '12345', 'name': 'Alonzo Manaog', 'status': 'A', 'balance': 100, 'total_transactions': 0,
      'plan': 'SP'},]
    return Money_manager(accounts)


def test_deposit_valid(setup_accounts):
    transaction = {"account_number": "12345", "amount": 50.00}
    setup_accounts.deposit(transaction)
    assert setup_accounts.accounts["12345"]["balance"] == 150.00


def test_deposit_non_existing_account(setup_accounts, capsys):
    transaction = {"account_number": "99999", "amount": 20.00}
    setup_accounts.deposit(transaction)

    captured = capsys.readouterr()
    assert "Invalid account number" in captured.out


def test_deposit_zero_amount(setup_accounts):
    transaction = {"account_number": "12345", "amount": 0.00}
    setup_accounts.deposit(transaction)
    assert setup_accounts.accounts["12345"]["balance"] == 100.00


def test_deposit_negative_amount(setup_accounts):
    transaction = {"account_number": "12345", "amount": -10.00}
    setup_accounts.deposit(transaction)
    assert setup_accounts.accounts["12345"]["balance"] == 100.00