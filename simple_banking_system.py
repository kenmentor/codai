import tkinter as tk
from tkinter import messagebox

class BankingSystem:
    def __init__(self, master):
        self.master = master
        master.title("Simple Banking System")

        # Initial balance
        self.balance = 0

        # Labels and buttons
        self.balance_label = tk.Label(master, text="Balance: $0")
        self.balance_label.pack()

        self.deposit_button = tk.Button(master, text="Deposit", command=self.deposit)
        self.deposit_button.pack()

        self.withdraw_button = tk.Button(master, text="Withdraw", command=self.withdraw)
        self.withdraw_button.pack()

    def update_balance_label(self):
        self.balance_label.config(text=f"Balance: ${self.balance}")

    def deposit(self):
        amount_str = tk.simpledialog.askstring("Deposit", "Enter amount to deposit:")
        try:
            amount = float(amount_str)
            if amount > 0:
                self.balance += amount
                self.update_balance_label()
                messagebox.showinfo("Success", f"Deposited ${amount}")
            else:
                messagebox.showwarning("Invalid amount", "Please enter a positive number.")
        except (ValueError, TypeError):
            messagebox.showerror("Invalid input", "Please enter a valid number.")

    def withdraw(self):
        amount_str = tk.simpledialog.askstring("Withdraw", "Enter amount to withdraw:")
        try:
            amount = float(amount_str)
            if amount > 0 and amount <= self.balance:
                self.balance -= amount
                self.update_balance_label()
                messagebox.showinfo("Success", f"Withdrew ${amount}")
            elif amount > self.balance:
                messagebox.showwarning("Insufficient funds", "You do not have enough funds.")
            else:
                messagebox.showwarning("Invalid amount", "Please enter a positive number.")
        except (ValueError, TypeError):
            messagebox.showerror("Invalid input", "Please enter a valid number.")


def main():
    root = tk.Tk()
    banking_system = BankingSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
