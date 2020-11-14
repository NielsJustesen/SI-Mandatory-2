import sqlite3
from datetime import datetime, timedelta

try:
    db = sqlite3.connect("Bank.db")
    sqlite3.isolation_level = None
except sqlite3.Error:
    print("---- FAILED TO CONNECT TO DB ----")

class BankUser():

    #BankUser TABLE CRUD Operations
    def AddBankUser(self, userId):
        try:
            createdAt = datetime.now()
            db.execute("INSERT INTO BankUser VALUES (?,?,?,?)", (None, str(userId), str(createdAt), None))
            db.commit()
        except sqlite3.Error:
            print("---- FAILED TO INSERT BankUser ----")

    def GetBankUser(self, userId):
        try:
            db.execute("SELECT * FROM BankUser WHERE Id = ?;", (str(userId)))
            db.commit()
            return db.cursor().fetchone()
        except sqlite3.Error:
            print("--- FAILED TO SELECT BankUser ----")


    def UpdateBankUser(self, userId, modifiedAt):
        try:
            db.execute("UPDATE BankUser SET ModifiedAt = ? WHERE Id = ?;", (str(modifiedAt), str(userId)))
            db.commit()
        except sqlite3.Error:
            print("--- FAIlED TO UPDATE BankUser ---")

    def DeleteBankUser(self, userId):
        try:
            db.execute("DELETE FROM BankUser WHERE Id = ?;", (str(userId)))
            db.commit()
        except:
            print("---- FAILED TO DELETE BankUser ---")


class Account():

    #Account TABLE CRUD OPERATIONS
    def AddAccount(self, bankUserId, accountNo, isStudent, amount):
        try:
            createdAt = datetime.now()
            db.execute("INSERT INTO Account VALUES (?,?,?,?,?,?,?)",  (None,  str(bankUserId), str(accountNo), str(isStudent), str(createdAt), None, str(amount)))
            db.commit()
        except:
            print("---- FAILED TO ADD NEW ACCOUNT ----")

    def GetAccount(self, bankUserId):
        try:
            cur = db.cursor()
            cur.execute("""SELECT * FROM Account WHERE BankUserId = """ + str(bankUserId))
            account = cur.fetchone()
            return account
        except sqlite3.Error:
            print("---- FAILED TO SELECT ACCOUNT ----")

    def UpdateAccount(self, bankUserId, amount):
        try:
            oldAmount = self.GetAccount(bankUserId)[6]
            newAmount = amount + oldAmount
            db.execute("UPDATE Account SET Amount = ? WHERE BankUserId = ?", (str(newAmount), str(bankUserId)))
            db.commit()
        except sqlite3.Error:
            print("---- FAILED TO UPDATE ACCOUNT ----")

    def DeleteAccount(self, accountId):
        try:
            db.execute("DELETE FROM Account WHERE Id = ?;", (str(accountId)))
            db.commit()
        except sqlite3.Error:
            print("---- FAILED TO DELETE ACCOUNT ----")

class Deposit():

    def AddDeposit(self, bankUserId, amount):
        account = Account()
        try:
            cur = db.cursor()
            createdAt = datetime.now()
            cur.execute("INSERT INTO Deposit VALUES (?,?,?,?)", (None, str(bankUserId), str(createdAt), str(amount)))
            account.UpdateAccount(bankUserId, amount)
        except sqlite3.Error:
            print("---- FAILED TO ADD NEW DEPOSIT ----")

    def GetDeposits(self, bankUserId):
        try:
            cur = db.cursor()
            cur.execute("SELECT amount FROM Deposit WHERE BankUserId = " + str(bankUserId))
            deposits = cur.fetchall()
            return deposits
        except:
            print("---- FAILED TO GET DEPOSITS ----")

class Loan():

    def CreateLoan(self, bankUserId, amount):
        try:
            account = Account()
            createdAt = datetime.now()
            db.execute("INSERT INTO Loan VALUES (?,?,?,?,?)", (None, str(bankUserId), str(createdAt), None, str(amount)))
            db.commit()
            account.UpdateAccount(bankUserId, amount)
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
                   


bankUser = BankUser()
account = Account()
deposit = Deposit()
loan = Loan()

# bankUser.AddBankUser(1)
# account.AddAccount(1,1,True,10000)
# deposit.AddDeposit(1,1000)
# userAccount = account.GetAccount(1)
# print(account.GetAccount(1))
# deposit.GetDeposits(1)
# loan.CreateLoan(1, 200)
