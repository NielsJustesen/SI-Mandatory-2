from flask import Flask, request, Response
import sqlite3
import json
import sys
# from Functions import InterestRate, CreateLoan
from datetime import datetime
app = Flask(__name__)


@app.route('/add-deposit', methods = ['POST'])
def AddNewDeposit():
    bankUserId = ""
    amount = ""
    if 'BankUserId' in request.args and 'amount' in request.args:
        bankUserId = request.args["BankUserId"]
        amount = request.args["amount"]
    if (amount <= str(0) or amount == None and bankUserId == None):
        return Response(json.dumps({"Message":"Bad Request"}), status=400)
    else:
        db = sqlite3.connect("Bank.db")
        # amountWithInterest = request.get_json(InterestRate.main(json.dumps({"amount":amount})))["amount"]
        cur = db.cursor()
        cur.execute("SELECT * FROM Account WHERE BankUserId = ?",  str(bankUserId))
        account = cur.fetchone()
        oldamount = account[6]
        newAmount = oldamount + int(amount)#+ amountWithInterest
        modifiedAt = datetime.now()
        db.execute("UPDATE Account SET Amount = ?, ModifiedAt = ? WHERE BankUserId = ?", (str(newAmount), str(modifiedAt), str(bankUserId)))
        cur = db.cursor()
        createdAt = datetime.now()
        cur.execute("INSERT INTO Deposit VALUES (?,?,?,?)", (None, str(bankUserId), str(createdAt), str(amount)))
        cur.execute("commit")
        db.close()
        return Response(json.dumps({}),status=201)

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

@app.route('/create-loan', methods = ['POST'])
def CreateLoan():
    bankUserId = ""
    loanAmount = ""
    currentAmount = ""
    if 'BankUserId' in request.args and 'LoanAmount' in request.args and 'CurrentAmount' in request.args:
        bankUserId = request.args["BankUserId"]
        loanAmount = request.args["LoanAmount"]
        currentAmount = request.args["CurrentAmount"]
        # print(str(bankUserId), str(loanAmount), str(currentAmount))
    else:
        return Response(json.dumps({"Message": "Bad Request"}), status=400)
    # validation = CreateLoan.main(json.dumps({"CurrentAmount": currentAmount, "LoanAmount": loanAmount}))
    if (bankUserId == ""):
        return Response(json.dumps({"Message":"Unacceptable: Loan is to big"}), status=406)
    elif (1 == 1 and float(loanAmount) > 0):
        #validation["status code"] == 200
        db = sqlite3.connect("Bank.db")
        createdAt = datetime.now()
        db.execute("INSERT INTO Loan VALUES (?,?,?,?,?)", (None, str(bankUserId), str(createdAt), None, str(loanAmount)))
        cur = db.cursor()
        cur.execute("SELECT * FROM Account WHERE BankUserId = ?",  str(bankUserId))
        account = cur.fetchone()
        oldAmount = account[6]
        modifiedAt = datetime.now()
        newAmount = float(loanAmount) + float(oldAmount)
        db.execute("UPDATE Account SET Amount = ?, ModifiedAt = ? WHERE BankUserId = ?", (str(newAmount), str(modifiedAt), str(bankUserId)))
        db.commit()
        db.close()
        return Response(json.dumps({"Message":"Loan was created"}), status=201)
    else:
        return { "Error Message": "insufficiant funds"}, 403
if __name__=="BankAPI":
    app.run(port=4545)