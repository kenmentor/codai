import tkinter as tk
from tkinter import messagebox

# File to simulate shared balance
BALANCE_FILE = 'shared_balance.txt'

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking App")

        # Initialize balance from file or set to 0 if file doesn't exist
        self.balance = self.read_balance_from_file()

        self.balance_label = tk.Label(root, text=f"Current Balance: ${self.balance:.2f}")
        self.balance_label.pack()

        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack()

        self.deposit_button = tk.Button(root, text="Deposit", command=self.deposit)
        self.deposit_button.pack()

        self.withdraw_button = tk.Button(root, text="Withdraw", command=self.withdraw)
        self.withdraw_button.pack()

    def deposit(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be positive.")
            self.balance += amount
            self.update_balance()
            self.write_balance_to_file()
            messagebox.showinfo("Success", f"Deposited ${amount:.2f}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def withdraw(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be positive.")
            if amount > self.balance:
                raise ValueError("Insufficient funds.")
            self.balance -= amount
            self.update_balance()
            self.write_balance_to_file()
            messagebox.showinfo("Success", f"Withdrew ${amount:.2f}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_balance(self):
        self.balance_label.config(text=f"Current Balance: ${self.balance:.2f}")

    def read_balance_from_file(self):
        try:
            with open(BALANCE_FILE, 'r') as f:
                return float(f.read())
        except (FileNotFoundError, ValueError):
            return 0.0

    def write_balance_to_file(self):
        with open(BALANCE_FILE, 'w') as f:
            f.write(str(self.balance))

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()