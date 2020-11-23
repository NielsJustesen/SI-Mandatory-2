from flask import Blueprint, request
from BankDB import BankUser
import sqlite3

BankUserApi = Blueprint('BankUserApi', __name__)

@BankUserApi.route('/bank-user', methods=['POST'])
def create():
  data = request.get_json()
  bu = BankUser()
  result = bu.AddBankUser(data['userId'])
  if result:
    return {"status": "user created"}, 201
  else:
    return {"status": "user creation failed"}, 422

@BankUserApi.route('/bank-user', methods=['GET'])
def read():
  data = request.args.get('id')
  bu = BankUser()
  result = bu.GetBankUser(data)
  if result is None:
    return {"status": "user not found"}, 422
  else:
    return {"user": result}, 201
    

@BankUserApi.route('/bank-user', methods=['PUT'])
def update():
  id = request.args.get('id')
  bu = BankUser()
  result = bu.UpdateBankUser(id)
  if result:
    return {"user": result}, 201
  else:
    return {"status": "user not found"}, 422

@BankUserApi.route('/bank-user', methods=['DELETE'])
def delete():
  id = request.args.get('id')
  bu = BankUser()
  result = bu.DeleteBankUser(id)
  if result:
    return {"status": "user deleted"}, 201
  else:
    return {"status": "user not found"}, 422