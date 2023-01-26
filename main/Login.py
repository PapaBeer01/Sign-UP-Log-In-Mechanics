import sqlite3
import re

""" This accepts users Email input and checks for it in the DB
A non existent account would be refered to sign up, while an existent
account would proceed to password"""
# Valid Email Check
try:
    Email = input("Email: ")
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not (re.search(regex, Email)):
        raise ValueError("Invalid Input! Enter a valid Email")
except ValueError as e:
    print(e)

# DBO Email Check
try:
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    c.execute("SELECT Email FROM SignUp WHERE Email == (?)", [Email])
    mail = c.fetchall()
    conn.close()
    if len(mail) > 0:
        pass
    else:
        raise ValueError("This Account doesn't exist, Sign up instead")
except ValueError as e:
    print(e)

# Password
try:
    Password = input("Pasword: ")
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    c.execute("SELECT Password FROM SignUp WHERE Email == (?)", [Email])
    pwd = c.fetchall()
    conn.close()
    if Password in pwd[0]:
        print("Login Successful!")
    else:
        raise Exception("Incorrect Passowrd! Try again")
except Exception as e:
    print(e)





