import binascii
from gmssl import sm4

def str_to_hexstr(s):
    data = s.encode('utf-8')
    binstr = binascii.unhexlify(data)
    return binstr.decode('utf-8')

SM4 = sm4.CryptSM4()

def enc(encrypt_key,m):
    SM4.set_key(encrypt_key.encode(),sm4.SM4_ENCRYPT)
    enc_m = SM4.crypt_ecb(m.encode())
    return enc_m.hex()

def dec(decrypt_key,c):
    SM4.set_key(decrypt_key.encode(),sm4.SM4_DECRYPT)
    dec_c = SM4.crypt_ecb(bytes.fromhex(c))
    return dec_c.decode()

key = "123454321asdfgrtjkli"
M = "bear123bear"
print("明文：",M)
C = enc(key,M)
print("加密：",C)
MM = dec(key,C)
print("解密：",MM)
