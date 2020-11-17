from flask import Flask, request, Response
import sqlite3
import json
import sys
# from Functions import InterestRate, CreateLoan
from datetime import datetime
from BankDB import Account, BankUser, Loan, Deposit
app = Flask(__name__)


@app.route('/add-deposit', methods = ['POST'])
def AddNewDeposit():
    bankUserId = ""
    amount = ""
    if 'BankUserId' in request.args and 'Amount' in request.args:
        bankUserId = request.args["BankUserId"]
        amount = request.args["Amount"]
    if (float(amount) <= 0 or amount == None and bankUserId == None):
        return Response(json.dumps({"Message":"Bad Request"}), status=400)
    else:
        d = Deposit()
         #######################################
         # MISSING Interestrate cloud function!#
         #######################################
        d.AddDeposit(bankUserId, amount)
        return Response(json.dumps({"Message":"Deposit was succesful", "Deposited": float(amount)}),status=201)

@app.route('/list-deposits', methods = ['GET'])
def ListDeposits():
    if 'BankUserId' in request.args:
        bankUserId = request.args["BankUserId"]
    else:
        return Response({"Bad Request": "Bad Request"}, status=400)
    d = Deposit()
    deposits = d.GetDeposits(bankUserId)
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

    if 'BankUserId' in request.args and 'LoanAmount' in request.args:
        bankUserId = request.args["BankUserId"]
        loanAmount = request.args["LoanAmount"]
        ###################################
        # MISSING Validate cloud function!#
        ###################################
    else:
        return Response(json.dumps({"Message": "Bad Request"}), status=400)

    if (bankUserId == ""):
        return Response(json.dumps({"Message":"Unacceptable: Loan is to big"}), status=406)
    elif (1 == 1 and float(loanAmount) > 0):
        l = Loan()
        l.CreateLoan(bankUserId, loanAmount)
        return Response(json.dumps({"Message":"Loan was created"}), status=201)

@app.route('/pay-loan', methods=['POST'])
def PayLoan():

    bankUserId = ""
    loanId = ""
    amount = ""

    if 'BankUserId' in request.args and 'LoanId' in request.args and 'Amount':
        bankUserId = request.args['BankUserId']
        loanId = request.args['LoanId']
        amount = request.args['Amount']

        loan = Loan()
        if (loan.PayLoan(bankUserId, loanId, amount)):
            return Response(json.dumps({"Message":"Succesfully paid load", "Amount":str(amount)}))
        else:
            return Response(json.dumps({"Message":"Not enought money to pay loan"}), status=406)
        
    else:
        return Response(json.dumps({"Message":"Bad Request"}), status=400)

    
@app.route('/list-loans', methods=['GET'])
def ListLoans():

    bankUserId = ""

    if 'BankUserId' in request.args:
        bankUserId = request.args['BankUserId']
        loan = Loan()
        loans = loan.GetUnpaidLoans(bankUserId)
        returnObj = []
    
        if loans:
            for x in loans:
                returnObj.append(x[0])
        else:
            return Response(json.dumps({"Message":"No loans found for the user"}), status=204)

        return Response(json.dumps({"Loans":returnObj}))
    else:
        return Response(json.dumps({"Message":"Bad Request"}), status=400)



@app.route('/withdraw-money', methods=['GET'])
def WithdrawMoney():

    amount = ""
    userId = ""
    
    if 'Amount' in request.args and 'UserId' in request.args:
        amount = request.args['Amount']
        userId = request.args['UserId']
        account = Account()
        try:
            db = sqlite3.connect("Bank.db")
            cur = db.cursor()
            cur.execute("SELECT Amount FROM Account LEFT JOIN BankUser ON Account.BankUserId = BankUser.UserId WHERE BankUser.UserId = ?", (str(userId)))
            currentAmount = cur.fetchone()[0]
            print(f"Current Amount: {currentAmount}. Amount to withdraw: {amount}")
            if currentAmount != None:
                if (int(currentAmount) >= int(amount)):
                    currentAmount = int(currentAmount) - int(amount)
                    db.execute("UPDATE Account SET Amount = ? WHERE BankUserId = ?", (str(currentAmount), str(userId)))
                    db.commit()
                    db.close()
                    return Response(json.dumps({"Message":"Withdrawl was succesful", "Amount withdrewn": float(amount)}))
                else:
                    return Response(json.dumps({"Message":"Not enough money in account"}), status=400)
            else:
                return Response(json.dumps({"Message":"No account found"}), status=400)
        except sqlite3.Error as er:
            return Response(json.dumps({"Message":"No user found"}), status=400)
            print("---- ERROR COULD NOT WITHDRAW MONEY ----")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
    else:
        return Response(json.dumps({"Message":"Bag Request"}), status=400)
   