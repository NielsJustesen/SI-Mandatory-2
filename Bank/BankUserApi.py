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
