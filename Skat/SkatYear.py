from flask import Flask, request, Response, Blueprint
import sqlite3
import json
from datetime import datetime
import requests

SkatYear = Blueprint('SkatYear', __name__)

@SkatYear.route('/skat-year', methods=["POST"])
def create():
  db = conn()

  data = request.get_json()

  db_cursor = db.cursor()

  create_stmt = "INSERT INTO SkatYear (Label, StartDate, EndDate) VALUES (?, ?, ?)"
  
  try:
    create_data = [data['Label'], data['StartDate'], data['EndDate']]
    db_cursor.execute(create_stmt, create_data)
    db.commit()

    get_stmt = "SELECT id FROM SkatYear WHERE id=(SELECT MAX(id) FROM SkatYear)"
    db_cursor.execute(get_stmt)
    SkatYear = db_cursor.fetchone()

    get_stmt = "SELECT id, userid FROM SkatUser"
    db_cursor.execute(get_stmt)
    SkatUsers = db_cursor.fetchall()

    create_stmt = "INSERT INTO SkatUserYear (SkatUserId, SkatYearId, UserId) VALUES (?, ?, ?)"
    for SkatUser in SkatUsers:
      insert_data = [SkatUser[0], SkatYear[0], SkatUser[1]]
      db_cursor.execute(create_stmt, insert_data)
      db.commit()
      
    db.close()
    return {"status": "SkatYear created"}, 201
  except Exception as e:
    return {"status": f"SkatYear creation failed: {e}"}, 400

@SkatYear.route('/skat-year', methods=['GET'])
def read():
  db = conn()

  id = request.args.get('id')

  db_cursor = db.cursor()
  get_stmt = "SELECT * FROM SkatYear WHERE id=?"
  
  try:
    db_cursor.execute(get_stmt, id)
    SkatYear = db_cursor.fetchone()

    if SkatYear is None:
      return {"status": "SkatYear not found"}, 404
    else:
      skat_year_json = {
        "id": SkatYear[0],
        "label": SkatYear[1],
        "CreatedAt": SkatYear[2],
        "ModifiedAt": SkatYear[3],
        "StartDate": SkatYear[4],
        "EndDate": SkatYear[5],
      }
      return {"SkatYear": skat_year_json}, 200
  except Exception as e:
    return {"status": f"failed getting SkatYear: {e}"}, 400

@SkatYear.route('/skat-year', methods=['PUT'])
def update():
  db = conn()

  id = request.args.get('id')
  data = request.get_json()

  db_cursor = db.cursor()
  update_stmt = "UPDATE SkatYear SET label=?, ModifiedAt=? WHERE id=?"
  
  update_data = [data['label'], str(datetime.now()), id]

  try:
    db_cursor.execute(update_stmt, update_data)
    db.commit()
    db.close()

    if db_cursor.rowcount < 1:
      return {"status": "Record not found"}, 404
    else:
     return {"status": "SkatYear has been updated"}, 200
  except Exception as e:
    return {"status": f"update failed: {e}"}, 400

@SkatYear.route('/skat-year', methods=['DELETE'])
def delete():
  db = conn()
  # Enable if we decide to cascade delete SkatUserYear
  # db.execute("PRAGMA foreign_keys=ON")

  id = request.args.get('id')

  db_cursor = db.cursor()
  delete_stmt = "DELETE FROM SkatYear WHERE id=?"

  try:
    db_cursor.execute(delete_stmt, id)
    db.commit()
    db.close()

    if db_cursor.rowcount < 1:
      return {"status": "record not found"}, 404
    else:
      return {"status": "SkatYear deleted"}, 200
  except Exception as e:
    return {"status": f"deletion failed: {e}"}, 400

def conn():
  try:
    db = sqlite3.connect('Skat.db')
    return db
  except Exception as e:
    return { "status": f"db connection failed: {e}"}