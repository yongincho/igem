import base64
import hashlib
from Crypto.Cipher import AES


BS = 16
pad = (lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode())
unpad = (lambda s: s[:-ord(s[len(s)-1:])])


class AESCipher(object):
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, message):
        message = message.encode()
        raw = pad(message)
        cipher = AES.new(self.key, AES.MODE_CBC, self.__iv())
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.__iv())
        dec = cipher.decrypt(enc)
        return unpad(dec).decode('utf-8')

    def __iv(self):
        return chr(0) * 16


if __name__ == "__main__":
    key = 'secretkey'
    message = '택스트'
    
    aes = AESCipher(key)
    encrypt = aes.encrypt(message)
    decrypt = aes.decrypt(encrypt)
    
    print(encrypt)
    print(decrypt)
