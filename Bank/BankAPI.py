from flask import Flask, request, Response
import sqlite3
import json
# from Functions import InterestRate, CreateLoan
# from Bank.BankDB import BankUser, Account, Deposit, Loan
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
    if 'BankUserId' in request.args:
        bankUserId = request.args["BankUserId"]
    else:
        return Response({"Bad Request": "Bad Request"}, status=400)
    db = sqlite3.connect("Bank.db")
    cur = db.cursor()
    cur.execute("""SELECT amount FROM Deposit WHERE BankUserId = """ + str(bankUserId))
    deposits = cur.fetchall()
    db.close()
    returnObj = []
    if deposits:
        for x in deposits:
            returnObj.append(x[0])
    else:
        return Response(json.dumps({"error": "Bad Request"}), status=400)
    if deposits:
        return Response(json.dumps({"deposits":returnObj}), status=200, mimetype='application/json')

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