from flask import Flask, request, Blueprint
import sqlite3
import json

borger = Blueprint('borger', __name__)

@borger.route('/borger', methods = ['POST'])
def create():
  db = conn()
  data = request.get_json()

  UserId = data['UserId']

  db_cursor = db.cursor()
  create_stmt = """INSERT INTO BorgerUser (UserId) VALUES (?)"""

  try:
    db_cursor.execute(create_stmt, UserId)
    db.commit()
    db.close()
    return {"status": "user created"}, 201
  except Exception as e:
    return {"status": f"user creation failed: {e}"}, 400

@borger.route('/borger', methods = ['GET'])
# Find user with specified id
# Returns user not found error if record does not exist
def read():
  db = conn()

  id = request.args.get('id')

  db_cursor = db.cursor()
  get_stmt = "SELECT * FROM BorgerUser WHERE id=?"
  
  try:
    db_cursor.execute(get_stmt, [id])
    user = db_cursor.fetchone()

    if user is None:
      return {"status": "user not found"}, 404
    else:
      user_json = {
        "CreatedAt": user[2],
        "UserId": user[1],
        "id": user[0]
      }
      return {"user": user_json}, 200
  except Exception as e:
    return {"status": f"failed getting user: {e}"}, 400

@borger.route('/borger', methods = ['PUT'])
# What should be updated here?
# Update borger with specified id
# Only possible to update UserId
# Addresses BorgerUserId will also be updated
def update():
  db = conn()

  id = request.args.get('id')
  data = request.get_json()

  update_borger_data = [data['UserId'], id]
  

  db_cursor = db.cursor()
  update_borger_stmt = """UPDATE BorgerUser SET userId=? WHERE id=?"""
  get_stmt = "SELECT userid FROM BorgerUser WHERE id=?"
  update_addresses_stmt = """UPDATE Address SET BorgerUserId=? WHERE BorgerUserId=?"""

  try:
    db_cursor.execute(get_stmt, id)
    borger = db_cursor.fetchone()
    update_addresses_data = [data['UserId'], borger[0]]
    if borger is None:
      return {"status": "borger not found"}, 404
    else:
      db_cursor.execute(update_borger_stmt, update_borger_data)    
      db_cursor.execute(update_addresses_stmt, update_addresses_data)
      db.commit()
      db.close()
      return {"status": "borger update successful"}, 200
  except Exception as e:
    return {"status": f"failed updating borger: {e}"}, 400

@borger.route('/borger', methods = ['DELETE'])
# Delete user with specified id
# DB Schema cascade deletes all addresses of User ( PRAGMA foreign_keys=ON allows that )
def delete():
  db = conn()
  db.execute("PRAGMA foreign_keys=ON")

  id = request.args.get('id')

  db_cursor = db.cursor()
  delete_stmt = "DELETE FROM BorgerUser WHERE id=?"

  try:
    db_cursor.execute(delete_stmt, id)
    db.commit()
    db.close()
    return {"status": "user deleted"}, 200
  except Exception as e:
    return {"status": f"deletion failed: {e}"}, 400

def conn():
  try:
    db = sqlite3.connect('Borger.db')
    return db
  except Exception as e:
    return { "status": f"db connection failed: {e}"}
  
  
