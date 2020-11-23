from flask import Blueprint, request
from BankDB import Account
import sqlite3

AccountApi = Blueprint('AccountApi', __name__)

@AccountApi.route('/account', methods=['POST'])
def create():
  data = request.get_json()
  a = Account()
  result = a.AddAccount(data['bankUserId'], data['accountNo'], data['isStudent'], data['amount'])
  if result:
    return {"status": "account created"}, 201
  else:
    return {"status": "failed creating account"}, 422

@AccountApi.route('/account', methods=['GET'])
def read():
  data = request.get_json()
  a = Account()
  result = a.GetAccount(data['bankUserId'])
  if result is None:
    return {"status": "account not found"}
  else:
    return {"account": result}
    

@AccountApi.route('/account', methods=['PUT'])
def update():
  data = request.get_json()
  a = Account()
  result = a.UpdateAccount(data['bankUserId'], data['amount'])
  if result:
    return {"status": "account updated"}
  else:
    return {"status": "update failed"}

@AccountApi.route('/account', methods=['DELETE'])
def delete():
  data = request.get_json()
  a = Account()
  result = a.DeleteAccount(data['account'])
  if result:
    return {"status": "account deleted"}
  else:
    return {"status": "deletion failed"}