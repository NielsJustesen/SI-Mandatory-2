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

    
    print("1")

# o Implement /list-loans endpoint
# § GET request which will return a list of all the loans belonging to a user that
# are greater than 0 (not paid)
# § The request should have a BankUserId to retrieve the loans for a user.
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


# o Implement /withdrawl-money endpoint:
# § The body of that request should contain an amount and a UserId(Not
# BankUserId, not SkatUserId)
# § Subtract (if possible) the amount from that users account. Throw an error
# otherwise.
@app.route('/withdraw-money', methods=['POST'])
def WithdrawMoney():
    print("1")