from hashlib import sha3_512



def encrypt_password(raw_password:str) -> str:
    hex_object = sha3_512(raw_password.encode())
    hex_data = hex_object.hexdigest()
    
    return hex_data



