from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL configuration
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='bank_system1_db'
)
cursor = db.cursor()

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# View all accounts
@app.route('/accounts')
def accounts():
    cursor.execute('SELECT * FROM accounts')
    accounts = cursor.fetchall()
    return render_template('accounts.html', accounts=accounts)

# Create a new account
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        name = request.form['name']
        balance = round((float(request.form['balance'])))
        account_number=int(request.form['Accountnumber'])
        cursor.execute('INSERT INTO accounts (name, balance, account_number) VALUES (%s, %s, %s)', (name, balance, account_number))
        db.commit()
        return redirect('/accounts')
    return render_template('create_account.html')

# Perform a transaction
@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if request.method == 'POST':
        account_number = request.form['account_number']
        amount = float(request.form['amount'])
        transaction_type = request.form['transaction_type']

        cursor.execute('SELECT balance FROM accounts WHERE account_number = %s', (account_number,))
        balance = cursor.fetchone()[0]

        if transaction_type == 'deposit':
            new_balance = balance + amount
        elif transaction_type == 'withdraw':
            new_balance = balance - amount

        cursor.execute('UPDATE accounts SET balance = %s WHERE account_number = %s', (new_balance, account_number))
        my_list = None
        try:
            print(my_list[0])
        except TypeError:
            print("The list is empty or None.")

        db.commit()
        return redirect('/accounts')

    return render_template('transaction.html')


if __name__ == '__main__':
    app.run(debug=True)


