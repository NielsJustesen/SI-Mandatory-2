from flask import Flask
import json
from json import request
from Functions import InterestRate
from Bank.BankDB import BankUser, Account, Deposit
app = Flask(__name__)


@app.route('/add-deposit', methods = ['POST'])
def AddNewDeposit():
    data = request.get_json()
    amount = data["amount"]
    bankUserId = data["BankUserId"]
    if (amount <= 0 | amount == None):
        return
    else:
        amountWithInterest = request.get_json(InterestRate.main(json.dumps({"amount":amount})))["amount"]
        Account.UpdateAccount(bankUserId, amountWithInterest)
        Deposit.AddDeposit(bankUserId, amount)