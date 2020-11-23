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
  id = request.args.get('id')
  a = Account()
  result = a.GetAccount(id)
  if result is None:
    return {"status": "account not found"}, 404
  else:
    return {"account": result}, 200
    

@AccountApi.route('/account', methods=['PUT'])
def update():
  id = request.args.get('id')
  data = request.get_json()
  a = Account()
  result = a.UpdateAccount(id, data['amount'])
  if result:
    return {"status": "account updated"}, 200
  else:
    return {"status": "update failed"}, 422

@AccountApi.route('/account', methods=['DELETE'])
def delete():
  id = request.args.get('id')
  a = Account()
  result = a.DeleteAccount(id)
  if result:
    return {"status": "account deleted"}, 200
  else:
    return {"status": "deletion failed"}, 400