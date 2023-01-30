import psycopg2
from psycopg2 import Error
import sys
import re
from cryptography.fernet import Fernet
from decouple import config

"""Encryption Key would be used to encrypt & decrypt 
passwords during SignUp & Login"""
# key = Fernet.generate_key()
key = config('FERNET_KEY')
key = key[1:]
fernet = Fernet(key)

"""This function enables user defined data to be passed into.
the SIGNUP_TABLE on the database
"""
def add_into_DB(MatricNo, Names, Level, Email, Password):
    try:
        psycopg2.connect(user="postgres",
                         password="k0r0.day",
                         host="localhost",
                         port="5432",
                         database="accounts")
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    conn = psycopg2.connect(user="postgres",
                         password="k0r0.day",
                         host="localhost",
                         port="5432",
                         database="accounts")
    c = conn.cursor()
    try:
        insert = "INSERT INTO SignUp(MatricNo, Names, Level, Email, Password) VALUES (%s,%s,%s,%s,%s)"
        values = (MatricNo, Names, Level, Email, Password)
        c.execute(insert,values)
        print("Data Inserted")
    except psycopg2.IntegrityError:
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
            Password = str(Password)
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
    global Email
    try:
        Email = input("Email: ")
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not (re.search(regex, Email)):
            raise ValueError("Invalid Input! Enter a valid Email")
    except ValueError as e:
        print(e)

    # DBO Email Check
    try:
        conn = psycopg2.connect(user="postgres",
                         password="k0r0.day",
                         host="localhost",
                         port="5432",
                         database="accounts")
        c = conn.cursor()
        retrieve = "SELECT Email FROM SignUp WHERE Email = '{0}'".format(Email)
        c.execute(retrieve)
        mail = c.fetchone()
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
        conn = psycopg2.connect(user="postgres",
                                password="k0r0.day",
                                host="localhost",
                                port="5432",
                                database="accounts")
        c = conn.cursor()
        retrieve = "SELECT Password FROM SignUp WHERE Email = '{0}'".format(Email)
        c.execute(retrieve)
        iterable = c.fetchall()
        p1 = iterable[0][0]
        p1 = bytes(p1[2:-1], 'utf-8')
        pwd = decrypt(p1)
        print(pwd)
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
