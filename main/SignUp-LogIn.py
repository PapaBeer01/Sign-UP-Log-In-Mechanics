import sys
import sqlite3
import re
from cryptography.fernet import Fernet
from decouple import config

"""Encryption Key would be used to encrypt & decrypt 
passwords during SignUp & Login"""
# key = Fernet.generate_key()
key = config('FERNET_KEY')
key = key[1:]
print(key)
fernet = Fernet(key)

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
        sqlite3.connect("accounts.db")
        # if not sqlite3.OperationalError:
        #     pass
        # else:
        #     raise Exception
    except sqlite3.OperationalError as e:
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

""" Encryption & Decryption Functions for Passwords """
def encrypt(Password):
    return fernet.encrypt(Password.encode())

def decrypt(Password):
    return fernet.decrypt(Password).decode()

""" Variables to Accept User-defined Data, as well as checks and 
error proofing the datas
"""
def Signup():
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
            i = input("Password: ")
            if len(i) < 8:
                raise ValueError("Password must be 8 characters and above")
            Password = encrypt(i)
            break
        except ValueError as e:
            print(e)
    add_into_DB(MatricNo, Names, Level, Email, Password)

"""Function for Login"""
def Login():
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
        iterable = c.fetchall()
        pwd = iterable[0][0]
        pwd = decrypt(pwd)
        if Password == pwd:
            print("Login Successful!")
        else:
            raise Exception("Incorrect Passowrd! Try again")
    except Exception as e:
        print(e)

"Homepage function to select either Login or SignUp"
def homepage():
    hmm = 0
    while hmm == 0:
        try:
            homepage = input("Signup or Login: ").upper()
            if homepage == "SIGNUP":
                Signup()
            elif homepage == "LOGIN":
                Login()
            else:
                raise ValueError("Enter Between 'Signup' or 'Login'")
            hmm = 1
        except ValueError as e:
            print(e)
            homepage = ("Signup or Login: ").upper()
h = homepage()
print(h)
sys.exit()
