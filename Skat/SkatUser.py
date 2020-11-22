from flask import Flask, request, Response, Blueprint
import sqlite3
import json
import requests

SkatUser = Blueprint('SkatUser', __name__)

@SkatUser.route('/skat-user', methods = ['POST'])
def create():
  db = conn()
  data = request.get_json() 

  db_cursor = db.cursor()
  create_stmt = """INSERT INTO SkatUser (UserId) VALUES (?)"""

  try:
    UserId = data['UserId']
    db_cursor.execute(create_stmt, UserId)
    db.commit()
    db.close()
    return Response(json.dumps({"status": "SkatUser created"}), status=201)
  except Exception as e:
    return {"status": f"SkatUser creation failed: {e}"}, 400

@SkatUser.route('/skat-user', methods = ['GET'])
# Find user with specified id
# Returns SkatUser not found error if record does not exist
def read():
  db = conn()

  id = request.args.get('id')

  db_cursor = db.cursor()
  get_stmt = "SELECT * FROM SkatUser WHERE id=?"
  
  try:
    db_cursor.execute(get_stmt, id)
    SkatUser = db_cursor.fetchone()

    if SkatUser is None:
      return {"status": "SkatUser not found"}, 404
    else:
      user_json = {
        "id": SkatUser[0],
        "UserId": SkatUser[1],
        "CreatdAt": SkatUser[2],
        "IsActive": SkatUser[3]
      }
      return {"SkatUser": user_json}, 200
  except Exception as e:
    return {"status": f"failed getting SkatUser: {e}"}, 400

@SkatUser.route('/skat-user', methods = ['PUT'])
def update():
  db = conn()
  id = request.args.get('id')
  isActive = request.args.get('IsActive')
  data = [isActive, id]
  try:
    update_stmt = "UPDATE SkatUser SET IsActive = ? WHERE id = ?"
    db.execute(update_stmt, data)
    db.commit()
    db.close()
    return {"status": "successfully updated SkatUser"}, 200
  except Exception as e:
    return {"status": f"failed updating SkatUser: {e}"}, 400

@SkatUser.route('/skat-user', methods = ['DELETE'])
def delete():
  db = conn()
  id = request.args.get('id')
  try:
    delete_stmt = "DELETE SkatUser WHERE id = ?"
    db.execute(delete_stmt, id)
    db.commit()
    db.close()
    return {"status": "successfully deleted skat user"}, 200
  except Exception as e:
    return {"status": f"failed deleting SkatUser: {e}"}, 400

def conn():
  try:
    db = sqlite3.connect('Skat.db')
    return db
  except Exception as e:
    return { "status": f"db connection failed: {e}"}



@SkatUser.route('/pay-taxes', methods=['POST'])
def PayTaxes():
  userId = request.args.get('UserId')
  balance = request.args.get('Balance')

  get_stmt = """SELECT IsPaid, Amount, id FROM SkatUserYear LEFT JOIN SkatUser ON SkatUserYear.SkatUserId = SkatUser.UserId WHERE SkatUser.UserId = ?"""

  try:
    db = sqlite3.connect("Skat.db")

    db_cursor = db.cursor()

    db.execute(get_stmt, userId)

    skatUserYear = db_cursor.fetchall()

    unpaidTaxes = []
    for x in skatUserYear:
      if x[0] is False or float(x[1]) > 0:
        unpaidTaxes.append(x[0])
    
    for y in unpaidTaxes:
      resp = request.get("http://localhost:7071/api/Skat_Tax_Calculator", params={"money":float(balance)})
      
      if resp.status == 200:
        id = skatUserYear[2]
        taxAmount = resp['tax_amount']
        update_stmt = """UPDATE SkatUserYear SET IsPaid = true, Amount = ? WHERE id = ?"""
    
        db_cursor.execute(update_stmt, (taxAmount, id))

        withdrawResp = requests.get("http://127.0.0.1:5000/withdraw-money", params={"UserId":userId, "Amount":taxAmount})
        amountPaid = withdrawResp['Amount']

        return Response(json.dumps({"Taxes":taxAmount}),status=200)
      elif resp['tax_amount'] < float(0):
        return Response(json.dumps({"Message":"Calculated tax was less than zero"}),status=400)



        
        
      
  except sqlite3.Error as e:
    return {"status": f"failed paying taxes: {e}"}, 400


# o Returns the calculated amount that needs to be paid.
# o An error will be thrown if the value is negative.