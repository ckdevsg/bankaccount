import unittest
from unittest.mock import Mock, MagicMock, call, patch

from bank_account_integration import BankAccount, NotificationSystem


class TestBankAccountDepositIntegration(unittest.TestCase):

    def test_deposit_calls_notification_system(self):
        """Test that deposit calls the notification system with correct message."""
        mock_notification = Mock(spec=NotificationSystem)
        acct = BankAccount("Alice", 100, notification_system=mock_notification)
        
        result = acct.deposit(50)
        
        self.assertEqual(result, "Deposited: $50.00. New balance: $150.00")
        mock_notification.notify.assert_called_once_with("Alice: Deposited: $50.00. New balance: $150.00")

    def test_deposit_without_notification_system(self):
        """Test that deposit works without a notification system."""
        acct = BankAccount("Bob", 100)
        
        result = acct.deposit(50)
        
        self.assertEqual(result, "Deposited: $50.00. New balance: $150.00")
        self.assertEqual(acct.balance, 150)

    def test_deposit_with_notification_system_multiple_calls(self):
        """Test that notification system is called for each deposit."""
        mock_notification = Mock(spec=NotificationSystem)
        acct = BankAccount("Carol", 100, notification_system=mock_notification)
        
        acct.deposit(50)
        acct.deposit(25)
        acct.deposit(10)
        
        self.assertEqual(mock_notification.notify.call_count, 3)
        calls = [
            call("Carol: Deposited: $50.00. New balance: $150.00"),
            call("Carol: Deposited: $25.00. New balance: $175.00"),
            call("Carol: Deposited: $10.00. New balance: $185.00"),
        ]
        mock_notification.notify.assert_has_calls(calls)

    def test_deposit_invalid_amount_does_not_notify(self):
        """Test that invalid deposit does not trigger notification."""
        mock_notification = Mock(spec=NotificationSystem)
        acct = BankAccount("Dave", 100, notification_system=mock_notification)
        
        result = acct.deposit(0)
        
        self.assertEqual(result, "Deposit amount must be positive.")
        mock_notification.notify.assert_not_called()

    def test_deposit_negative_amount_does_not_notify(self):
        """Test that negative deposit does not trigger notification."""
        mock_notification = Mock(spec=NotificationSystem)
        acct = BankAccount("Eve", 100, notification_system=mock_notification)
        
        result = acct.deposit(-50)
        
        self.assertEqual(result, "Deposit amount must be positive.")
        mock_notification.notify.assert_not_called()

    def test_deposit_with_magic_mock_notification(self):
        """Test deposit with MagicMock notification system."""
        mock_notification = MagicMock()
        acct = BankAccount("Frank", 200, notification_system=mock_notification)
        
        acct.deposit(75)
        
        self.assertTrue(mock_notification.notify.called)
        args, kwargs = mock_notification.notify.call_args
        self.assertIn("Frank", args[0])
        self.assertIn("$75.00", args[0])

    def test_deposit_triggers_notification_after_balance_update(self):
        """Test that notification is triggered and balance is updated correctly."""
        mock_notification = Mock(spec=NotificationSystem)
        acct = BankAccount("Gin", 100, notification_system=mock_notification)
        
        # Perform deposit
        result = acct.deposit(50)
        
        # Verify balance was updated
        self.assertEqual(acct.balance, 150)
        # Verify notification was called
        mock_notification.notify.assert_called_once()
        # Verify returned message shows correct new balance
        self.assertIn("$150.00", result)

    def test_deposit_notification_includes_account_holder_name(self):
        """Test that notification includes the account holder's name."""
        mock_notification = Mock(spec=NotificationSystem)
        acct = BankAccount("Hannah", 100, notification_system=mock_notification)
        
        acct.deposit(100)
        
        call_args = mock_notification.notify.call_args[0][0]
        self.assertIn("Hannah", call_args)

    def test_deposit_with_patched_notification_system(self):
        """Test deposit with patched NotificationSystem class."""
        with patch('bank_account_integration.NotificationSystem') as MockedNotificationSystem:
            mock_instance = MockedNotificationSystem.return_value
            acct = BankAccount("Iris", 100, notification_system=mock_instance)
            
            acct.deposit(60)
            
            mock_instance.notify.assert_called_once()

    def test_deposit_float_amounts_with_notification(self):
        """Test deposit with float amounts calls notification with formatted value."""
        mock_notification = Mock(spec=NotificationSystem)
        acct = BankAccount("Jack", 100, notification_system=mock_notification)
        
        acct.deposit(25.5)
        
        call_args = mock_notification.notify.call_args[0][0]
        self.assertIn("$25.50", call_args)

    def test_notification_called_exactly_once_per_valid_deposit(self):
        """Test that notification is called exactly once for each valid deposit."""
        mock_notification = Mock(spec=NotificationSystem)
        acct = BankAccount("Kate", 100, notification_system=mock_notification)
        
        # Valid deposit
        acct.deposit(50)
        self.assertEqual(mock_notification.notify.call_count, 1)
        
        # Invalid deposit
        acct.deposit(-10)
        self.assertEqual(mock_notification.notify.call_count, 1)  # Still 1
        
        # Another valid deposit
        acct.deposit(25)
        self.assertEqual(mock_notification.notify.call_count, 2)

    def test_notification_message_format(self):
        """Test that notification message has the correct format."""
        mock_notification = Mock(spec=NotificationSystem)
        acct = BankAccount("Leo", 500, notification_system=mock_notification)
        
        acct.deposit(100)
        
        call_args = mock_notification.notify.call_args[0][0]
        # Format should be: "AccountHolder: Deposited: $amount. New balance: $balance"
        self.assertTrue(call_args.startswith("Leo:"))
        self.assertIn("Deposited:", call_args)
        self.assertIn("New balance:", call_args)

    def test_large_deposit_amount_with_notification(self):
        """Test large deposit amounts are correctly notified."""
        mock_notification = Mock(spec=NotificationSystem)
        acct = BankAccount("Mona", 1000, notification_system=mock_notification)
        
        large_amount = 999999.99
        acct.deposit(large_amount)
        
        call_args = mock_notification.notify.call_args[0][0]
        self.assertIn(f"${large_amount:.2f}", call_args)

    def test_deposit_balance_update_reflected_in_get_balance(self):
        """Test that deposited amount is reflected in get_balance after notification."""
        mock_notification = Mock(spec=NotificationSystem)
        acct = BankAccount("Nora", 100, notification_system=mock_notification)
        
        acct.deposit(75)
        balance = acct.get_balance()
        
        self.assertEqual(balance, "Current balance: $175.00")
        mock_notification.notify.assert_called_once()


if __name__ == "__main__":
    unittest.main()
