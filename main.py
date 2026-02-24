import mysql.connector
from mysql.connector import Error

# Connect to MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',       
            password='Abhi',  
            database='mini_banking'
        )
        return connection
    except:
        print("Error connecting to MySQL")
        return None


# Create a new account
def create_account():
    name = input("Enter account holder name: ")
    balance = float(input("Enter initial deposit: "))
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (%s, %s)", (name, balance))
    account_id = cursor.lastrowid
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (%s, %s, %s)", (account_id, 'Deposit', balance))
    conn.commit()
    print(f"Account created successfully! Your Account ID is {account_id}")
    cursor.close()
    conn.close()

# Deposit money
from decimal import Decimal

def deposit():
    account_id = input("Enter your account ID: ")
    try:
        amount = Decimal(input("Enter amount to deposit: "))
    except:
        print("Invalid amount!")
        return

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
    account = cursor.fetchone()

    if account is None:
        print(f"Account {account_id} does not exist!")
        return

    # Update account balance
    new_balance = account[0] + amount
    cursor.execute("UPDATE accounts SET balance = %s WHERE account_id = %s", (new_balance, account_id))

    # Insert transaction
    cursor.execute(
        "INSERT INTO transactions (account_id, type, amount) VALUES (%s, %s, %s)",
        (account_id, 'Deposit', amount)
    )

    conn.commit()
    print(f"Deposit successful! New balance: {new_balance}")
    cursor.close()
    conn.close()



# Withdraw money
def withdraw():
    account_id = int(input("Enter account ID: "))
    amount = float(input("Enter amount to withdraw: "))
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
    balance = cursor.fetchone()
    if balance and balance[0] >= amount:
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, account_id))
        cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (%s, %s, %s)", (account_id, 'Withdraw', amount))
        conn.commit()
        print("Amount withdrawn successfully!")
    else:
        print("Insufficient balance or invalid account ID.")
    cursor.close()
    conn.close()

# Check balance
def check_balance():
    account_id = int(input("Enter account ID: "))
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, balance FROM accounts WHERE account_id = %s", (account_id,))
    result = cursor.fetchone()
    if result:
        print(f"Account Holder: {result[0]}, Balance: {result[1]}")
    else:
        print("Account not found.")
    cursor.close()
    conn.close()

# Show transactions
def show_transactions():
    account_id = int(input("Enter account ID: "))
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT type, amount, date_time FROM transactions WHERE account_id = %s", (account_id,))
    results = cursor.fetchall()
    if results:
        print("Transactions:")
        for row in results:
            print(f"{row[2]} | {row[0]} | {row[1]}")
    else:
        print("No transactions found.")
    cursor.close()
    conn.close()

# Main Menu
def main():
    while True:
        print("\n--- Mini Banking System ---")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Show Transactions")
        print("6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            create_account()
        elif choice == '2':
            deposit()
        elif choice == '3':
            withdraw()
        elif choice == '4':
            check_balance()
        elif choice == '5':
            show_transactions()
        elif choice == '6':
            print("Exiting... Thank you!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()