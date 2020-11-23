import sqlite3
from datetime import datetime, timedelta
import json


# try:
#     db = sqlite3.connect("Bank.db")
#     sqlite3.isolation_level = None
# except sqlite3.Error:
#     print("---- FAILED TO CONNECT TO DB ----")

class BankUser():

    #BankUser TABLE CRUD Operations
    def AddBankUser(self, userId):
        try:
            db = sqlite3.connect("Bank.db")
            db_cursor = db.cursor()
            createdAt = datetime.now()
            db_cursor.execute("INSERT INTO BankUser VALUES (?,?,?,?)", (None, str(userId), str(createdAt), None))
            db.commit()
            db.close()
            if db_cursor.rowcount < 1:
              return False
            else:
              return True
        except sqlite3.Error as er:
            print("---- FAILED TO INSERT BankUser ----")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)

    def GetBankUser(self, userId):
        try:
            db = sqlite3.connect("Bank.db")
            cur = db.cursor()
            cur.execute("SELECT * FROM BankUser WHERE Id = ?;", (str(userId)))
            user = cur.fetchone()
            db.close()
            return user
        except sqlite3.Error as er:
            print("--- FAILED TO SELECT BankUser ----")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)


    def UpdateBankUser(self, userId):
        try:
            db = sqlite3.connect("Bank.db")
            modifiedAt = datetime.now()
            db.execute("UPDATE BankUser SET ModifiedAt = ? WHERE Id = ?;", (str(modifiedAt), str(userId)))
            db.commit()
            db.close()
        except sqlite3.Error as er:
            print("--- FAIlED TO UPDATE BankUser ---")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)

    def DeleteBankUser(self, userId):
        try:
            db = sqlite3.connect("Bank.db")
            db.execute("DELETE FROM BankUser WHERE Id = ?;", (str(userId)))
            db.commit()
            db.close()
            return True
        except sqlite3.Error as er:
            print("---- FAILED TO DELETE BankUser ---")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            return False


class Account():

    #Account TABLE CRUD OPERATIONS
    def AddAccount(self, bankUserId, accountNo, isStudent, amount):
        try:
            db = sqlite3.connect("Bank.db")
            createdAt = datetime.now()
            db.execute("INSERT INTO Account VALUES (?,?,?,?,?,?,?)",  (None,  str(bankUserId), str(accountNo), str(isStudent), str(createdAt), None, str(amount)))
            db.commit()
            db.close()
        except sqlite3.Error as er:
            print("---- FAILED TO ADD NEW ACCOUNT ----")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)

    def GetAccount(self, bankUserId):
        try:
            db = sqlite3.connect("Bank.db")
            cur = db.cursor()
            cur.execute("""SELECT * FROM Account WHERE BankUserId = """ + str(bankUserId))
            account = cur.fetchone()
            db.close()
            return account
        except sqlite3.Error as er:
            print("---- FAILED TO SELECT ACCOUNT ----")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)

    def UpdateAccount(self, bankUserId, amount):
        try:
            oldAmount = self.GetAccount(bankUserId)[6]
            db = sqlite3.connect("Bank.db")
            modifiedAt = datetime.now()
            newAmount = float(amount) + float(oldAmount)
            db.execute("UPDATE Account SET Amount = ?, ModifiedAt = ? WHERE BankUserId = ?", (str(newAmount), str(modifiedAt), str(bankUserId)))
            db.commit()
            db.close()
        except sqlite3.Error as er:
            print("---- FAILED TO UPDATE ACCOUNT ----")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)

    def DeleteAccount(self, accountId):
        try:
            db = sqlite3.connect("Bank.db")
            db.execute("DELETE FROM Account WHERE Id = ?;", (str(accountId)))
            db.commit()
            db.close()
            return True
        except sqlite3.Error  as er:
            print("---- FAILED TO DELETE ACCOUNT ----")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            return False

    def Withdraw(self, userId, amount):
        try:
            db = sqlite3.connect("Bank.db")
            cur = db.cursor()
            cur.execute("SELECT Amount FROM Account LEFT JOIN BankUser ON Account.BankUserId = BankUser.UserId WHERE BankUser.UserId = ?", (str(userId)))
            currentAmount = cur.fetchone()[0]
            if currentAmount != None:
                if (float(currentAmount) >= float(amount)):
                    currentAmount = float(currentAmount) - float(amount)
                    modifiedAt = datetime.now()
                    db.execute("UPDATE Account SET Amount = ?, ModifiedAt = ? WHERE BankUserId = ?", (str(currentAmount), str(modifiedAt), str(userId)))
                    db.commit()
                    db.close()
                    return "Withdrawl done"
                else:
                    return "Not enough in account"
            else:
                return "No user found"
        except sqlite3.Error as er:
            print("---- ERROR COULD NOT WITHDRAW MONEY ----")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)


class Deposit():

    def AddDeposit(self, bankUserId, amount):
        try:
            account = Account()
            db = sqlite3.connect("Bank.db")
            createdAt = datetime.now()
            db.execute("INSERT INTO Deposit VALUES (?,?,?,?)", (None, str(bankUserId), str(createdAt), str(amount)))
            db.commit()
            db.close()
            account.UpdateAccount(bankUserId, amount)
        except sqlite3.Error as er:
            print("---- FAILED TO ADD NEW DEPOSIT ----")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)

    def GetDeposits(self, bankUserId):
        try:
            db = sqlite3.connect("Bank.db")
            cur = db.cursor()
            cur.execute("SELECT amount FROM Deposit WHERE BankUserId = " + str(bankUserId))
            deposits = cur.fetchall()
            db.close()
            return deposits
        except sqlite3.Error as er:
            print("---- FAILED TO GET DEPOSITS ----")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)

class Loan():

    def CreateLoan(self, bankUserId, amount):
        try:
            db = sqlite3.connect("Bank.db")
            createdAt = datetime.now()
            db.execute("INSERT INTO Loan VALUES (?,?,?,?,?)", (None, str(bankUserId), str(createdAt), None, str(amount)))
            db.commit()
            db.close()
            account = Account()
            account.UpdateAccount(bankUserId, amount)
        except sqlite3.Error as er:
            print("---- FAILED TO CREATE LOAN ----")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
                   
    def PayLoan(self, bankUserId, loanId, amount):
        try:
            account = Account()
            currentAmount = account.GetAccount(bankUserId)[6]
            print(currentAmount)
            if (float(currentAmount) >= float(amount)):
                db = sqlite3.connect("Bank.db")
                modifiedAt = datetime.now()
                db.execute("UPDATE Loan SET Amount = 0, ModifiedAt = ? WHERE BankUserId = ? AND Id = ?", (str(modifiedAt), str(bankUserId), str(loanId)))
                db.commit()
                db.close()
                withdrawl = 0 - float(amount)
                account.UpdateAccount(bankUserId, withdrawl)
                return True
            else:
                return False
        except sqlite3.Error as er:
            print("---- FAILED TO PAY LOAN ----")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)

    def GetUnpaidLoans(self, bankUserId):
        try:
            print("sovs")
            db = sqlite3.connect("Bank.db")
            cur = db.cursor()
            cur.execute("SELECT Amount FROM Loan WHERE BankUserId = ? AND Amount > 0", (str(bankUserId)))
            loans = cur.fetchall()
            db.close()
            return loans
        except sqlite3.Error as er:
            print("---- FAILED TO LIST LOANS ----")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)

bankUser = BankUser()
account = Account()
deposit = Deposit()
loan = Loan()



# for x in range(5):
#     bankUser.AddBankUser(x+5)
#     account.AddAccount(x+5,1,True,10000)
# deposit.AddDeposit(1,14)
# d = deposit.GetDeposits(4)
# userAccount = account.GetAccount(6)
# print(account.GetAccount(6))
# deposits = deposit.GetDeposits(4)
# for x in deposits:
#     print(x[0])
# loan.CreateLoan(4, 200)
# user = bankUser.GetBankUser(1)
# bankUser.UpdateBankUser(1)
# account.UpdateAccount(1, 1)
# useraccunt = account.GetAccount(1)
# useraccunt = account.DeleteAccount(3)
# user = bankUser.DeleteBankUser(1)
# print(user)
# print(useraccunt)