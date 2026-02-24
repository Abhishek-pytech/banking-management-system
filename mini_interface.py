import tkinter as tk
from tkinter import messagebox
from decimal import Decimal
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Abhi",
    database="mini_banking"
)
cursor = conn.cursor()

# Functions
def deposit():
    account_id = entry_account.get()
    try:
        amount = Decimal(entry_amount.get())
    except:
        messagebox.showerror("Error", "Invalid amount")
        return

    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
    account = cursor.fetchone()
    if account is None:
        messagebox.showerror("Error", f"Account {account_id} does not exist!")
        return

    new_balance = account[0] + amount
    cursor.execute("UPDATE accounts SET balance = %s WHERE account_id = %s", (new_balance, account_id))
    cursor.execute(
        "INSERT INTO transactions (account_id, type, amount) VALUES (%s, %s, %s)",
        (account_id, 'Deposit', amount)
    )
    conn.commit()
    messagebox.showinfo("Success", f"Deposit successful! New balance: {new_balance}")

# GUI Setup
root = tk.Tk()
root.title("Mini Banking System")

tk.Label(root, text="Account ID").grid(row=0, column=0, padx=10, pady=10)
entry_account = tk.Entry(root)
entry_account.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Amount").grid(row=1, column=0, padx=10, pady=10)
entry_amount = tk.Entry(root)
entry_amount.grid(row=1, column=1, padx=10, pady=10)

tk.Button(root, text="Deposit", command=deposit).grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
    