from random import choice
import binascii
import sm3
import math
import func0

Initial_table = {
    'n': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123',
    'p': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF',
    'g': '32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7'\
         'bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0',
    'a': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC',
    'b': '28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93',
}
'''
Initial_table = {
    'n': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123',
    'p': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF',
    'x_g': '32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7',
    'y_g': 'bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0',
    'a': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC',
    'b': '28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93',
}
'''

class CryptSM2(object):

    def __init__(self,private_key,public_key,ecc_table=Initial_table):
        self.private_key = private_key
        self.public_key = public_key
        self.para_len = len(ecc_table['n'])
        self.ecc_a3 = (int(ecc_table['a'],base=16)+3) % int(ecc_table['p'],base=16)
        self.ecc_table=ecc_table

    def _k_point(self,k,Point):
        Point = '%s%s' % (Point,'1')
        mask_str = '8'
        for i in range(self.para_len-1):
            mask_str += '0'
        mask = int(mask_str,16)
        T = Point
        flag = False
        for j in range(self.para_len*4):
            if (flag):
                T = self._double_point(T)
            if (k & mask) != 0:
                if (flag):
                    T = self._add_point(T,Point)
                else:
                    flag = True
                    T = Point
            k = k << 1
        return self._convert_jacb_to_nor(T)

    def _double_point(self,Point):
        l = len(Point)
        len2 = 2 * self.para_len
        if l < len2:
            return None
        else:
            x1 = int(Point[0:self.para_len],16)
            y1 = int(Point[self.para_len:len2],16)
            if l == len2:
                z1 = 1
            else:
                z1 = int(Point[len2:],16)

            T6 = (z1 * z1) % int(self.ecc_table['p'], base=16)
            T2 = (y1 * y1) % int(self.ecc_table['p'], base=16)
            T3 = (x1 + T6) % int(self.ecc_table['p'], base=16)
            T4 = (x1 - T6) % int(self.ecc_table['p'], base=16)
            T1 = (T3 * T4) % int(self.ecc_table['p'], base=16)
            T3 = (y1 * z1) % int(self.ecc_table['p'], base=16)
            T4 = (T2 * 8) % int(self.ecc_table['p'], base=16)
            T5 = (x1 * T4) % int(self.ecc_table['p'], base=16)
            T1 = (T1 * 3) % int(self.ecc_table['p'], base=16)
            T6 = (T6 * T6) % int(self.ecc_table['p'], base=16)
            T6 = (self.ecc_a3 * T6) % int(self.ecc_table['p'], base=16)
            T1 = (T1 + T6) % int(self.ecc_table['p'], base=16)
            z3 = (T3 + T3) % int(self.ecc_table['p'], base=16)
            T3 = (T1 * T1) % int(self.ecc_table['p'], base=16)
            T2 = (T2 * T4) % int(self.ecc_table['p'], base=16)
            x3 = (T3 - T5) % int(self.ecc_table['p'], base=16)

            if (T5 % 2 == 1):
                T4 = (T5 + ((T5 + int(self.ecc_table['p'],16)) >> 1) - T3 ) % int(self.ecc_table['p'],16)
            else:
                T4 = (T5 + (T5 >> 1) - T3) % int(self.ecc_table['p'],16)

            T1 = (T1 * T4) % int(self.ecc_table['p'], base=16)
            y3 = (T1 - T2) % int(self.ecc_table['p'], base=16)
            form = '%%0%dx' % self.para_len
            form = form * 3
            return form % (x3, y3, z3)

    def _add_point(self,P1,P2):
        len2 = 2 * self.para_len
        l1 = len(P1)
        l2 = len(P2)
        if (l1 < len2) or (l2 < len2):
            return None
        else:
            X1 = int(P1[0:self.para_len], 16)
            Y1 = int(P1[self.para_len:len2], 16)
            if (l1 == len2):
                Z1 = 1
            else:
                Z1 = int(P1[len2:], 16)
            x2 = int(P2[0:self.para_len], 16)
            y2 = int(P2[self.para_len:len2], 16)

            T1 = (Z1 * Z1) % int(self.ecc_table['p'], base=16)
            T2 = (y2 * Z1) % int(self.ecc_table['p'], base=16)
            T3 = (x2 * T1) % int(self.ecc_table['p'], base=16)
            T1 = (T1 * T2) % int(self.ecc_table['p'], base=16)
            T2 = (T3 - X1) % int(self.ecc_table['p'], base=16)
            T3 = (T3 + X1) % int(self.ecc_table['p'], base=16)
            T4 = (T2 * T2) % int(self.ecc_table['p'], base=16)
            T1 = (T1 - Y1) % int(self.ecc_table['p'], base=16)
            Z3 = (Z1 * T2) % int(self.ecc_table['p'], base=16)
            T2 = (T2 * T4) % int(self.ecc_table['p'], base=16)
            T3 = (T3 * T4) % int(self.ecc_table['p'], base=16)
            T5 = (T1 * T1) % int(self.ecc_table['p'], base=16)
            T4 = (X1 * T4) % int(self.ecc_table['p'], base=16)
            X3 = (T5 - T3) % int(self.ecc_table['p'], base=16)
            T2 = (Y1 * T2) % int(self.ecc_table['p'], base=16)
            T3 = (T4 - X3) % int(self.ecc_table['p'], base=16)
            T1 = (T1 * T3) % int(self.ecc_table['p'], base=16)
            Y3 = (T1 - T2) % int(self.ecc_table['p'], base=16)

            form = '%%0%dx' % self.para_len
            form = form * 3
            return form % (X3, Y3, Z3)

    def _convert_jacb_to_nor(self,Point):
        len2 = self.para_len * 2
        x = int(Point[0:self.para_len],16)
        y = int(Point[self.para_len:len2],16)
        z = int(Point[len2:],16)
        z_inv = pow(z, int(self.ecc_table['p'], base=16) - 2, int(self.ecc_table['p'], base=16))
        z_invSquar = (z_inv * z_inv) % int(self.ecc_table['p'], base=16)
        z_invQube = (z_invSquar * z_inv) % int(self.ecc_table['p'], base=16)
        x_new = (x * z_invSquar) % int(self.ecc_table['p'], base=16)
        y_new = (y * z_invQube) % int(self.ecc_table['p'], base=16)
        z_new = (z * z_inv) % int(self.ecc_table['p'], base=16)
        if z_new == 1:
            form = '%%0%dx' % self.para_len
            form = form * 2
            return form % (x_new, y_new)
        else:
            return None

    def encrypt(self,data):    #加密
        m = data.hex()
        k = func0.rand_hex(self.para_len)
        C1 = self._k_point(int(k,16),self.ecc_table['g'])
        xy = self._k_point(int(k,16),self.public_key)
        x2 = xy[0:self.para_len]
        y2 = xy[self.para_len:self.para_len*2]
        ml = len(m)
        t = sm3.sm3_KDF(xy.encode('utf8'),ml/2)
        if int(t,16) == 0:
            return None
        else:
            form = '%%0%dx' % ml
            C2 = form % (int(m,16) ^ int(t,16))
            C3 = sm3.sm3_Hash([i for i in bytes.fromhex('%s%s%s' % (x2,m,y2))])
            return bytes.fromhex('%s%s%s' % (C1,C3,C2))

    def decrypt(self,data):   #解密
        data = data.hex()
        len2 = 2 * self.para_len
        len3 = len2 + 64
        C1 = data[0:len2]
        C2 = data[len3:]
        C3 = data[len2:len3]
        xy = self._k_point(int(self.private_key,16),C1)
        x2 = xy[0:self.para_len]
        y2 = xy[self.para_len:len2]
        cl = len(C2)
        t = sm3.sm3_KDF(xy.encode('utf8'),cl/2)
        if int(t,16) == 0:
            return None
        else:
            form = '%%0%dx' % cl
            M = form % (int(C2,16) ^ int(t,16))
            u = sm3.sm3_Hash([i for i in bytes.fromhex('%s%s%s' % (x2,M,y2))])
            return bytes.fromhex(M)

    def verify(self, Sign, data):
        # 验签函数，sign签名r||s，E消息hash，public_key公钥
        r = int(Sign[0:self.para_len], 16)
        s = int(Sign[self.para_len:2*self.para_len], 16)
        e = int(data.hex(), 16)
        t = (r + s) % int(self.ecc_table['n'], base=16)
        if t == 0:
            return 0

        P1 = self._k_point(s, self.ecc_table['g'])
        P2 = self._k_point(t, self.public_key)
        if P1 == P2:
            P1 = '%s%s' % (P1, 1)
            P1 = self._double_point(P1)
        else:
            P1 = '%s%s' % (P1, 1)
            P1 = self._add_point(P1, P2)
            P1 = self._convert_jacb_to_nor(P1)

        x = int(P1[0:self.para_len], 16)
        return (r == ((e + x) % int(self.ecc_table['n'], base=16)))

    def sign(self, data, K):  # 签名函数, data消息的hash，private_key私钥，K随机数，均为16进制字符串
        E = data.hex() # 消息转化为16进制字符串
        e = int(E, 16)
        d = int(self.private_key, 16)
        k = int(K, 16)

        P1 = self._k_point(k, self.ecc_table['g'])

        x = int(P1[0:self.para_len], 16)
        R = ((e + x) % int(self.ecc_table['n'], base=16))
        if R == 0 or R + k == int(self.ecc_table['n'], base=16):
            return None
        d_1 = pow(d+1, int(self.ecc_table['n'], base=16) - 2, int(self.ecc_table['n'], base=16))
        S = (d_1*(k + R) - R) % int(self.ecc_table['n'], base=16)
        if S == 0:
            return None
        else:
            return '%064x%064x' % (R,S)

    def _sm3_z(self, data):
        """
        SM3WITHSM2 签名规则:  SM2.sign(SM3(Z+MSG)，PrivateKey)
        其中: z = Hash256(Len(ID) + ID + a + b + xG + yG + xA + yA)
        """
        # sm3 with sm2 的z值
        z = '0080'+'31323334353637383132333435363738' + \
            self.ecc_table['a'] + self.ecc_table['b'] + self.ecc_table['g'] + \
            self.public_key
        z = binascii.a2b_hex(z)
        Za = sm3.sm3_Hash(func0.bytes2list(z))
        M_ = (Za + data.hex()).encode('utf-8')
        e = sm3.sm3_Hash(func0.bytes2list(binascii.a2b_hex(M_)))
        return e

    def sign_with_sm3(self, data, random_hex_str=None):
        sign_data = binascii.a2b_hex(self._sm3_z(data).encode('utf-8'))
        if random_hex_str is None:
            random_hex_str = func.random_hex(self.para_len)
        sign = self.sign(sign_data, random_hex_str) #  16进制
        return sign

    def verify_with_sm3(self, sign, data):
        sign_data = binascii.a2b_hex(self._sm3_z(data).encode('utf-8'))
        return self.verify(sign, sign_data) 


import base64
from gmssl import sm2, func

def test_sm2():
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    sm2_crypt = CryptSM2(public_key=public_key, private_key=private_key)
    data = b"111"
    enc_data = sm2_crypt.encrypt(data)
    dec_data = sm2_crypt.decrypt(enc_data)
    print(b"dec_data:%s" % dec_data)
    assert data == dec_data
    print("-----------------test sign and verify---------------")
    random_hex_str = func.random_hex(sm2_crypt.para_len)
    sign = sm2_crypt.sign(data, random_hex_str)
    print('sign:%s' % sign)
    verify = sm2_crypt.verify(sign, data)
    print('verify:%s' % verify)
    assert verify

    
def test_sm2sm3():
     private_key = "3945208F7B2144B13F36E38AC6D39F95889393692860B51A42FB81EF4DF7C5B8"
     public_key = "09F9DF311E5421A150DD7D161E4BC5C672179FAD1833FC076BB08FF356F35020"\
                  "CCEA490CE26775A52DC6EA718CC1AA600AED05FBF35E084A6632F6072DA9AD13"
     random_hex_str = "59276E27D506861A16680F3AD9C02DCCEF3CC1FA3CDBE4CE6D54B80DEAC1BC21"
     sm2_crypt = CryptSM2(public_key=public_key, private_key=private_key)
     data = b"message digest"
     print("-----------------test SM2withSM3 sign and verify---------------")
     sign = sm2_crypt.sign_with_sm3(data, random_hex_str)
     print('sign: %s' % sign)
     verify = sm2_crypt.verify_with_sm3(sign, data)
     print('verify: %s' % verify)
     assert verify


if __name__ == '__main__':
    test_sm2()
    test_sm2sm3()




















    

    
    

















    
                
