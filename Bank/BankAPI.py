from flask import Flask, request
import json
# from Functions import InterestRate, CreateLoan
from Bank.BankDB import BankUser, Account, Deposit, Loan
app = Flask(__name__)


# @app.route('/add-deposit', methods = ['POST'])
# def AddNewDeposit():
#     data = request.get_json()
#     amount = data["amount"]
#     bankUserId = data["BankUserId"]
#     if (amount <= 0 | amount == None):
#         return
#     else:
#         amountWithInterest = request.get_json(InterestRate.main(json.dumps({"amount":amount})))["amount"]
#         Account.UpdateAccount(bankUserId, amountWithInterest)
#         Deposit.AddDeposit(bankUserId, amount)

@app.route('/list-deposits', methods = ['GET'])
def ListDeposits():
    data = request.get_json()
    bankUserId = data["BankUserId"]
    deposit = Deposit()
    deposists = deposit.GetDeposits(bankUserId)
    if deposists:
        return { "deposits": deposists }, 200

# @app.route('/create-loan', methods = ['POST'])
# def CreateLoan():
#     loan = Loan()
#     data = request.get_json()
#     bankUserId = data["BankUserId"]
#     newAmount = data["NewAmount"]
#     currentAmount = data["CurrentAmount"]
#     validation = CreateLoan.main(json.dumps({"CurrentAmount": currentAmount, "NewAmount": newAmount}))
#     if (bankUserId == ""):
#         return 400
#     elif (validation["status code"] == 200):
#         loan.CreateLoan(bankUserId, newAmount)
#         return 201
#     else:
#         return { "Error Message": "insufficiant funds"}, 403

app.run(port=4545)