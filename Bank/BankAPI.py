from flask import Flask, request, Response, Blueprint
import sqlite3
import json
import sys
import requests
from datetime import datetime
from BankDB import Account, BankUser, Loan, Deposit
from BankUserApi import BankUserApi
app = Flask(__name__)

app.register_blueprint(BankUserApi)


@app.route('/bank/add-deposit', methods = ['POST'])
def AddDeposit():
    bankUserId = ""
    amount = ""
    if 'BankUserId' in request.args and 'Amount' in request.args:
        bankUserId = request.args["BankUserId"]
        amount = request.args["Amount"]
    if (float(amount) <= 0 or amount == None or bankUserId == None):
        return Response(json.dumps({"Message":"Bad Request"}), status=400)
    else:
        d = Deposit()
        parameters = {
            "Deposit": str(amount)
        }

        resp = requests.get("http://localhost:7071/api/InterestRate", params=parameters)
        newAmount = resp.json()['Deposit']
        d.AddDeposit(bankUserId, newAmount)
        return Response(json.dumps({"Message":"Deposit was succesful", "Deposited": float(amount)}),status=201)

@app.route('/bank/list-deposits', methods = ['GET'])
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

@app.route('/bank/create-loan', methods = ['POST'])
def CreateLoan():

    bankUserId = ""
    loanAmount = ""
    validation = False

    if 'BankUserId' in request.args and 'LoanAmount' in request.args:
        bankUserId = request.args["BankUserId"]
        loanAmount = request.args["LoanAmount"]
        account = Account()
        currentAmount = account.GetAccount(bankUserId)[6]
      
        parameters = {
            "currentAmount": str(currentAmount),
            "loanAmount": str(loanAmount)
        }

        resp = requests.get("http://localhost:7071/api/ValidateLoan", params=parameters)
        validation = resp.json()['Valid']

    else:
        return Response(json.dumps({"Message": "Bad Request"}), status=400)

    if (validation == "False"):
        return Response(json.dumps({"Message":"Unacceptable: Loan is to big"}), status=406)
    elif (validation == "True"):
        l = Loan()
        l.CreateLoan(bankUserId, loanAmount)
        return Response(json.dumps({"Message":"Loan was created"}), status=201)

@app.route('/bank/pay-loan', methods=['POST'])
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

    
@app.route('/bank/list-loans', methods=['GET'])
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

        return Response(json.dumps({"Loans":returnObj}), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({"Message":"Bad Request"}), status=400)



@app.route('/bank/withdraw-money', methods=['GET'])
def WithdrawMoney():

    amount = ""
    userId = ""
    
    if 'Amount' in request.args and 'UserId' in request.args:
        amount = request.args['Amount']
        userId = request.args['UserId']
        account = Account()
        success = account.Withdraw(userId, amount)

        if success == "Withdrawl done":
            return Response(json.dumps({"Message":"Withdrawl was succesful", "Amount": float(amount), "UserId":userId}))
        elif success == "Not enough in account":
            return Response(json.dumps({"Message":"Not enough money in account"}), status=400)
        else:
            return Response(json.dumps({"Message":"No user found"}), status=400)
    else:
        return Response(json.dumps({"Message":"Bag Request"}), status=400)
    