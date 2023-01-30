import random
import paypalrestsdk

class BankAccount:
    def __init__(self):
        self.account_number = self.generate_account_number()
        self.balance = 0.0
        paypalrestsdk.configure({
            "mode": "sandbox",
            "client_id": "YOUR_CLIENT_ID",
            "client_secret": "YOUR_CLIENT_SECRET"
        })

    def generate_account_number(self):
        return random.randint(100000000, 999999999)

    def check_balance(self):
        return self.balance

    def deposit(self, amount):
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://localhost:3000/payment/execute",
                "cancel_url": "http://localhost:3000/payment/cancel"
            },
            "transactions": [{
                "amount": {"total": str(amount), "currency": "USD"},
                "description": "Deposit to Bank Account {}".format(self.account_number)
            }]
        })
        if payment.create():
            self.balance += amount
        else:
            print(payment.error)

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient balance"
        self.balance -= amount
        return "Withdrawal successful"

    def show_account_details(self):
        print(f"Account Number: {self.account_number}\nBalance: {self.balance}")

def main():
    account = BankAccount()
    print("Account created\n", account.show_account_details())
    while True:
        choice = int(input("\nOptions:\n1. Deposit\n2. Withdraw\n3. Check balance\n4. Quit\nEnter choice: "))
        if choice == 1:
            deposit_amount = float(input("Enter amount to deposit: "))
            account.deposit(deposit_amount)
        elif choice == 2:
            withdraw_amount = float(input("Enter amount to withdraw: "))
            print(account.withdraw(withdraw_amount))
        elif choice == 3:
            print(f"Balance: {account.check_balance()}")
        elif choice == 4:
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    main()
