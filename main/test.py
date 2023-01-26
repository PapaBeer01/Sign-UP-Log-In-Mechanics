import sqlite3
from Encryption import decrypt
Email = input("Email: ")
try:
    password = input("Password: ")
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    c.execute("SELECT Password FROM SignUp WHERE Email == (?)", [Email])
    pwd = c.fetchall()
    conn.close()
    if password in pwd[0]:
        print(password)
        # print("Login Successful!")
    else:
        raise ValueError("Incorrect Passowrd! Try again")
except ValueError as e:
    print(e)

# x = [('xvi',)]
# p = input("enter: ")
# if (p) in x :
#     print("Yes")
# else:
#     print("No")
