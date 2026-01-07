import unittest

from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):

    def test_initial_balance_and_get_balance(self):
        acct = BankAccount("Alice", 100)
        self.assertEqual(acct.get_balance(), "Current balance: $100.00")

    def test_deposit_positive_updates_balance_and_message(self):
        acct = BankAccount("Bob", 100)
        msg = acct.deposit(50)
        self.assertEqual(msg, "Deposited: $50.00. New balance: $150.00")
        self.assertEqual(acct.get_balance(), "Current balance: $150.00")

    def test_deposit_zero_and_negative_no_change(self):
        acct = BankAccount("Carol", 20)
        msg0 = acct.deposit(0)
        self.assertEqual(msg0, "Deposit amount must be positive.")
        msgn = acct.deposit(-10)
        self.assertEqual(msgn, "Deposit amount must be positive.")
        self.assertEqual(acct.get_balance(), "Current balance: $20.00")

    def test_withdraw_within_balance_updates_and_message(self):
        acct = BankAccount("Dave", 100)
        msg = acct.withdraw(30)
        self.assertEqual(msg, "Withdrew: $30.00. New balance: $70.00")
        self.assertEqual(acct.get_balance(), "Current balance: $70.00")

    def test_withdraw_insufficient_funds_no_change(self):
        acct = BankAccount("Eve", 50)
        msg = acct.withdraw(100)
        self.assertEqual(msg, "Insufficient funds.")
        self.assertEqual(acct.get_balance(), "Current balance: $50.00")

    def test_withdraw_zero_and_negative_rejected(self):
        acct = BankAccount("Frank", 40)
        msg0 = acct.withdraw(0)
        self.assertEqual(msg0, "Withdrawal amount must be positive.")
        msgn = acct.withdraw(-5)
        self.assertEqual(msgn, "Withdrawal amount must be positive.")
        self.assertEqual(acct.get_balance(), "Current balance: $40.00")

    def test_floating_point_operations_and_formatting(self):
        acct = BankAccount("Gin", 0.0)
        acct.deposit(0.1)
        acct.deposit(0.2)
        self.assertEqual(acct.get_balance(), "Current balance: $0.30")
        acct.withdraw(0.15)
        self.assertEqual(acct.get_balance(), "Current balance: $0.15")

    def test_non_numeric_inputs_raise_type_error(self):
        acct = BankAccount("Hank", 10)
        with self.assertRaises(TypeError):
            acct.deposit("50")
        with self.assertRaises(TypeError):
            acct.withdraw("10")

    def test_large_amounts_and_precision(self):
        acct = BankAccount("Ivy", 0)
        large = 10 ** 12
        msg = acct.deposit(large)
        self.assertIn("Deposited", msg)
        self.assertEqual(acct.get_balance(), f"Current balance: ${large:.2f}")

    def test_negative_initial_balance_allowed_and_behaviour(self):
        acct = BankAccount("Jill", -50)
        self.assertEqual(acct.get_balance(), "Current balance: $-50.00")
        self.assertEqual(acct.withdraw(1), "Insufficient funds.")


if __name__ == "__main__":
    unittest.main()
