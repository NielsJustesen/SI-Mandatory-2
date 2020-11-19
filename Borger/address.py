from flask import Blueprint, request
import sqlite3

address = Blueprint('address', __name__)

@address.route("/address", methods = ["POST"])
def create():
  db = conn()
  data = request.get_json()

  BorgerUserId = data['BorgerUserId']
  create_data = [data['BorgerUserId'], data['Address']]

  db_cursor = db.cursor()

  get_stmt = "SELECT * FROM BorgerUser WHERE UserId=?"
  update_stmt = """UPDATE Address SET IsValid=0 WHERE BorgerUserId=?"""
  create_stmt = """INSERT INTO Address (BorgerUserId, Address) VALUES (?, ?)"""

  try:
    db_cursor.execute(get_stmt, BorgerUserId)
    user = db_cursor.fetchone()

    if user is None:
      return {"status": "user not found"}, 404
    else:
      db_cursor.execute(update_stmt, BorgerUserId)
      db_cursor.execute(create_stmt, create_data)
      db.commit()
      db.close()
      return {"status": "address created"}, 201
  except Exception as e:
    return {"status": f"address creation failed: {e}"}, 400

@address.route("/address", methods = ["GET"])
def read():
  db = conn()

  id = request.args.get('id')

  db_cursor = db.cursor()
  get_stmt = "SELECT * FROM Address WHERE id=?"
  
  try:
    db_cursor.execute(get_stmt, id)
    address = db_cursor.fetchone()

    if address is None:
      return {"status": "address not found"}, 404
    else:
      address_json = {
        "id": address[0],
        "BorgerUserId": address[1],
        "address": address[2],
        "createdAt": address[3],
        "isValid": address[4]
      }
      return {"address": address_json}, 200
  except Exception as e:
    return {"status": f"failed getting address: {e}"}, 400

@address.route("/address", methods = ["PUT"])
# Update user with specified id
# Non-active addresses cannot be updated
# Only the "address" attribute can be updated
def update():
  db = conn()

  id = request.args.get('id')
  data = request.get_json()

  update_data = [data['address'], id]

  db_cursor = db.cursor()
  update_stmt = """UPDATE Address SET Address=? WHERE id=?"""
  get_stmt = "SELECT isvalid FROM Address WHERE id=?"

  try:
    db_cursor.execute(get_stmt, id)
    address = db_cursor.fetchone()

    if address is None:
      return {"status": "address not found"}, 404
    elif address[0] == 0:
      return {"status": "can't update non-active address"}, 200
    else:
      db_cursor.execute(update_stmt, update_data)    
      db.commit()
      db.close()
      return {"status": "address update successful"}, 201
  except Exception as e:
    return {"status": f"failed updating address: {e}"}, 400

@address.route("/address", methods = ["DELETE"])
# Delete address with specified id
def delete():
  db = conn()

  id = request.args.get('id')

  db_cursor = db.cursor()
  delete_stmt = "DELETE FROM Address WHERE id=?"

  try:
    db_cursor.execute(delete_stmt, id)
    db.commit()
    db.close()
    return {"status": "address deleted"}, 200
  except Exception as e:
    return {"status": f"deletion failed: {e}"}

def conn():
  try:
    db = sqlite3.connect('Borger.db')
    return db
  except Exception as e:
    return { "status": f"db connection failed: {e}"}