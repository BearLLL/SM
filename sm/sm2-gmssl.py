from gmssl import sm2
import base64

privatekey = "00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5"
publickey = "B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207"

SM2 = sm2.CryptSM2(public_key=publickey,private_key=privatekey)

def enc(m):
    encode_m = SM2.encrypt(m.encode(encoding='utf-8'))
    enc_m = base64.b64encode(encode_m).decode()
    return enc_m

def dec(c):
    decode_c = base64.b64decode(c.encode())
    dec_c = SM2.decrypt(decode_c).decode(encoding='utf-8')
    return dec_c

M = 'bear123bear'
print("明文：",M)
C = enc(M)
print("加密：",C)
MM = dec(C)
print("解密：",MM)
