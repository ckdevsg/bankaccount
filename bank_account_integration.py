# Notification System for integration
class NotificationSystem:
    def notify(self, message):
        """Send a notification message."""
        pass


# Create a BankAccount class with methods for depositing, withdrawing and getting balance of an account.
# This version integrates with NotificationSystem
class BankAccount:
    def __init__(self, account_holder, initial_balance=0, notification_system=None):
        self.account_holder = account_holder
        self.balance = initial_balance
        self.notification_system = notification_system

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            message = f"Deposited: ${amount:.2f}. New balance: ${self.balance:.2f}"
            if self.notification_system:
                self.notification_system.notify(f"{self.account_holder}: {message}")
            return message
        else:
            return "Deposit amount must be positive."

    def withdraw(self, amount):
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount
                return f"Withdrew: ${amount:.2f}. New balance: ${self.balance:.2f}"
            else:
                return "Insufficient funds."
        else:
            return "Withdrawal amount must be positive."

    def get_balance(self):
        return f"Current balance: ${self.balance:.2f}"

# Example usage:
if __name__ == "__main__":
    account = BankAccount("John Doe", 100)
    print(account.get_balance())
    print(account.deposit(50))
    print(account.withdraw(30))
    print(account.withdraw(150))
    print(account.get_balance())
