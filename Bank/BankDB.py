import sqlite3
from datetime import datetime, timedelta
db = sqlite3.connect("Bank.db")

class BankUser():

    #BankUser TABLE CRUD Operations
    def AddBankUser(userId):
        createdAt = datetime.now()
        query = "INSERT INTO BankUser (?,?,?,?) VALUES (" + None + f"{userId}, {createdAt}," + None + ");"
        db.execute(query)
        db.commit()

    def GetBankUser(userId):
        query = f"SELECT * FROM BankUser WHERE Id = {userId};"
        db.execute(query)
        db.commit()
        return db.cursor().fetchone()


    def UpdateBankUser(userId, modifiedAt):
        query = f"UPDATE BankUser SET ModifiedAt = {modifiedAt} WHERE Id = {userId};"
        db.execute(query)
        db.commit()

    def DeleteBankUser(userId):
        query = f"DELETE FROM BankUser WHERE Id = {userId};"
        db.execute(query)
        db.commit()


class Account():

    #Account TABLE CRUD OPERATIONS
    def AddAccount(bankUserId, accountNo, isStudent, amount):
        createdAt = datetime.now()
        query = "INSERT INTO Account (?,?,?,?,?,?,?) VALUES (" + None + f"{bankUserId}, {accountNo}, {isStudent}, {createdAt}," + None + f", {amount});"
        db.execute(query)
        db.commit()

    def GetAccount(bankUserId):
        query = f"SELECT * FROM Account WHERE BankUserId = {bankUserId};"
        db.execute(query)
        db.commit()
        return db.cursor().fetchone()

    def UpdateAccount(bankUserId, amount):
        oldAmount = GetAccount(bankUserId)[6]
        newAmount = amount + oldAmount
        query = f"UPDATE Account SET Amount = {newAmount} WHERE BankUserId = {bankUserId};"
        db.execute(query)
        db.commit()

    def DeleteAccount(accountId):
        query = f"DELETE FROM Account WHERE Id = {accountId};"
        db.execute(query)
        db.commit()

class Deposit():

    def AddDeposit(bankUserId, amount):
        createdAt = datetime.now()
        query = f"INSERT INTO Deposit (?,?,?,?) VALUES (" + None + f", {bankUserId}, {createdAt}, {amount});"
        db.execute(query)
        db.commit()
