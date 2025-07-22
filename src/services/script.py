import secrets
import hashlib

def generate_secret_key():
    return secrets.token_hex(32)

class SecretKeyGenerator:
    def __init__(self):
        self.secret_key = generate_secret_key()

    def get_hashed_key(self):
        return hashlib.sha256(self.secret_key.encode()).hexdigest()
    
    def get_secret_key(self):
        return self.secret_key
    
    def compare_keys(self, key_to_compare):
        return self.get_hashed_key() == hashlib.sha256(key_to_compare.encode()).hexdigest()
    

sk=SecretKeyGenerator()
x=sk.get_secret_key()

print(f"Generated Secret Key: {x}")
print(sk.compare_keys(x))
