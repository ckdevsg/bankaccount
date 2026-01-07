import pytest

from bank_account import BankAccount


def test_initial_balance_and_get_balance():
    acct = BankAccount("Alice", 100)
    assert acct.get_balance() == "Current balance: $100.00"


def test_deposit_positive_updates_balance_and_message():
    acct = BankAccount("Bob", 100)
    msg = acct.deposit(50)
    assert msg == "Deposited: $50.00. New balance: $150.00"
    assert acct.get_balance() == "Current balance: $150.00"


def test_deposit_zero_and_negative_no_change():
    acct = BankAccount("Carol", 20)
    msg0 = acct.deposit(0)
    assert msg0 == "Deposit amount must be positive."
    msgn = acct.deposit(-10)
    assert msgn == "Deposit amount must be positive."
    assert acct.get_balance() == "Current balance: $20.00"


def test_withdraw_within_balance_updates_and_message():
    acct = BankAccount("Dave", 100)
    msg = acct.withdraw(30)
    assert msg == "Withdrew: $30.00. New balance: $70.00"
    assert acct.get_balance() == "Current balance: $70.00"


def test_withdraw_insufficient_funds_no_change():
    acct = BankAccount("Eve", 50)
    msg = acct.withdraw(100)
    assert msg == "Insufficient funds."
    assert acct.get_balance() == "Current balance: $50.00"


def test_withdraw_zero_and_negative_rejected():
    acct = BankAccount("Frank", 40)
    msg0 = acct.withdraw(0)
    assert msg0 == "Withdrawal amount must be positive."
    msgn = acct.withdraw(-5)
    assert msgn == "Withdrawal amount must be positive."
    assert acct.get_balance() == "Current balance: $40.00"


def test_floating_point_operations_and_formatting():
    acct = BankAccount("Gin", 0.0)
    # float sums that can show FP issues should still format to 2 decimals
    acct.deposit(0.1)
    acct.deposit(0.2)
    assert acct.get_balance() == "Current balance: $0.30"
    msg = acct.withdraw(0.15)
    # new balance should be 0.15 -> formats to 0.15
    assert acct.get_balance() == "Current balance: $0.15"


def test_non_numeric_inputs_raise_type_error():
    acct = BankAccount("Hank", 10)
    with pytest.raises(TypeError):
        acct.deposit("50")
    with pytest.raises(TypeError):
        acct.withdraw("10")


def test_large_amounts_and_precision():
    acct = BankAccount("Ivy", 0)
    large = 10 ** 12
    msg = acct.deposit(large)
    assert "Deposited" in msg
    assert acct.get_balance() == f"Current balance: ${large:.2f}"


def test_negative_initial_balance_allowed_and_behaviour():
    acct = BankAccount("Jill", -50)
    # class allows negative initial balances and get_balance should reflect it
    assert acct.get_balance() == "Current balance: $-50.00"
    # withdrawing any positive amount should be rejected as insufficient funds
    assert acct.withdraw(1) == "Insufficient funds."
