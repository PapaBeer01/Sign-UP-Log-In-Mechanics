import sys
import sqlite3
import re

"""Creating that Database that would accept User's info.
Such information would be used to create a users profile 
as well as log in details.
"""

def account_DB():
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    c.execute("CREATE TABLE SignUp (Matric_No INTEGER PRIMARY KEY,Names TEXT, Level TEXT, Email TEXT, "
              "Password TEXT)")
    conn.commit()
    conn.close()
    print("DataBase Created")
"""This function enables user defined data to be passed into.
the SIGNUP_TABLE on the database
"""


def add_into_DB(MatricNo, Names, Level, Email, Password):
    try:
        conn = sqlite3.connect("accounts.db")
        if not sqlite3.OperationalError:
            pass
        else:
            raise Exception
    except Exception as e:
        print(e)
        account_DB()
        conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO SignUp VALUES (?,?,?,?,?)", (MatricNo, Names, Level, Email, Password))
        print("Data Inserted")
    except sqlite3.IntegrityError:
        print("This user already exists. Try logging in instead")
    conn.commit()
    conn.close()

""" Encrypt Password"""


""" Variables to Accept User-defined Data, as well as checks and 
error proofing the datas
"""
# Matric Number
while True:
    try:
        MatricNo = input("Matric Number: ")
        if MatricNo.isnumeric():
            if len(MatricNo) != 9:
                raise ValueError("Invalid Input! Matric Number must be 9 digits long")
        else:
            raise ValueError("Invalid Input! Enter Your 9 digits Matric Number")
        break
    except ValueError as e:
        print(e)

# Names
while True:
    try:
        Names = input("Names: ").upper()
        if not Names.isprintable():
            raise ValueError("Invalid Input! Enter your First Name in Strings")
        break
    except ValueError as e:
        print(e)

# Level
while True:
    try:
        Level = input("Level: ")
        if Level.isnumeric():
            if Level not in ["100", "200", "300", "400"]:
                raise ValueError("Invalid Input! Enter Level Between '100 - 400'")
            break
    except ValueError as e:
        print(e)

# Email
while True:
    try:
        Email = input("Email: ").lower()
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not (re.search(regex, Email)):
            raise ValueError("Invalid Input! Enter a valid Email")
        break
    except ValueError as e:
        print(e)

while True:
    try:
        Password = input("Password: ")
        if len(Password) < 8:
            raise ValueError("Password must be 8 characters and above")
        break
    except ValueError as e:
        print(e)
add_into_DB(MatricNo, Names, Level, Email, Password)
sys.exit()
