from cryptography.fernet import Fernet
key = Fernet.generate_key()
fernet = Fernet(key)

def encrypt(n):
    return fernet.encrypt(n.encode())

def decrypt(password):
    return fernet.encrypt(password.encode())