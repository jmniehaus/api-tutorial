from pwdlib import PasswordHash

_hasher = PasswordHash.recommended()

def hash(x:str):
    return _hasher.hash(x)

def verify(password, hashed):
    return _hasher.verify(password, hashed)