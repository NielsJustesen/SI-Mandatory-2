from flask import Flask, request, Response, Blueprint
import sqlite3
import json

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
def read():
  pass

@SkatUser.route('/skat-user', methods = ['PUT'])
def update():
  pass

@SkatUser.route('/skat-user', methods = ['DELETE'])
def delete():
  pass


def conn():
  try:
    db = sqlite3.connect('Skat.db')
    return db
  except Exception as e:
    return { "status": f"db connection failed: {e}"}