import binascii
import math
from func0 import rol,bytes2list

IV = [
    1937774191, 1226093241, 388252375, 3666478592,
    2842636476, 372324522, 3817729613, 2969243214
]
    
T_j = [
    2043430169, 2043430169, 2043430169, 2043430169,
    2043430169, 2043430169, 2043430169, 2043430169,
    2043430169, 2043430169, 2043430169, 2043430169,
    2043430169, 2043430169, 2043430169, 2043430169,
    2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042
]

def sm3_FF_j(x,y,z,j):   #布尔函数FF
    if j >= 0 and j <= 15:
        f = x^y^z
    elif j >= 16 and j <= 63:
        f = (x & y)|(x & z)|(y & z)
    return f

def sm3_GG_j(x,y,z,j):   #布尔函数GG
    if j >= 0 and j <= 15:
        f = x^y^z
    elif j >= 16 and j <= 63:
        f = (x & y)|(~x & z)
    return f

def sm3_P0(X):   #置换函数P0
    return X^(rol(X,9))^(rol(X,17))

def sm3_P1(X):   #置换函数P1
    return X^(rol(X,15))^(rol(X,23))

def sm3_CF(Vi,Bi):   #压缩函数
    v = []
    for i in range(16):
        weight = 0x1000000
        data = 0
        for k in range(i*4,(i+1)*4):
            data = data + Bi[k] * weight
            weight = int(weight/0x100)
        v.append(data)

    #消息扩展
    for j in range(16,68):
        v.append(0)
        v[j] = sm3_P1(v[j-16]^v[j-9]^(rol(v[j-3],15)))^(rol(v[j-13],7))^v[j-6]
        str1 = "%08x" % v[j]
    v_1 = []
    for j in range(0,64):
        v_1.append(0)
        v_1[j] = v[j]^v[j+4]
        str1 = "%08x" % v_1[j]

    A,B,C,D,E,F,G,H = Vi

    for j in range(0,64):
        SS1 = rol(((rol(A,12)) + E + (rol(T_j[j],j % 32))) & 0xffffffff,7)
        SS2 = SS1^(rol(A,12))
        TT1 = (sm3_FF_j(A,B,C,j) + D + SS2 + v_1[j]) & 0xffffffff
        TT2 = (sm3_GG_j(E,F,G,j) + H + SS1 + v[j]) & 0xffffffff
        D = C
        C = rol(B,9)
        B = A
        A = TT1
        H = G
        G = rol(F,19)
        F = E
        E = sm3_P0(TT2)

        A,B,C,D,E,F,G,H = map(lambda x:x &0xffffffff ,[A,B,C,D,E,F,G,H])

    Vj = [A,B,C,D,E,F,G,H]
    return [Vj[i]^Vi[i] for i in range(8)]

def sm3_Hash(m):
    len1 = len(m)
    reserve1 = len1 % 64
    m.append(0x80)
    reserve1 = reserve1 + 1
    range_end = 56
    if reserve1 > range_end:
        range_end = range_end +64

    for i in range(reserve1,range_end):
        m.append(0x00)

    bit_len = len1 * 8
    bit_len_str = [bit_len % 0x100]
    for i in range(7):
        bit_len = int(bit_len / 0x100)
        bit_len_str.append(bit_len % 0x100)
    for i in range(8):
        m.append(bit_len_str[7-i])

    count = round(len(m) / 64)
    B = []
    for i in range(0,count):
        B.append(m[i*64:(i+1)*64])
    V=[]
    V.append(IV)
    for i in range(0,count):
        V.append(sm3_CF(V[i],B[i]))

    y = V[i+1]
    result = ""
    for i in y:
        result = '%s%08x' % (result,i)
    return result
    
def sm3_hash(msg,vectors):
    len1 = len(msg)
    reserve1 = len1 % 64
    msg.append(0x80)
    reserve1 = reserve1 + 1
    # 56-64, add 64 byte
    range_end = 56
    if reserve1 > range_end:
        range_end = range_end + 64

    for i in range(reserve1, range_end):
        msg.append(0x00)

    bit_length = (len1) * 8
    bit_length_str = [bit_length % 0x100]
    for i in range(7):
        bit_length = int(bit_length / 0x100)
        bit_length_str.append(bit_length % 0x100)
    for i in range(8):
        msg.append(bit_length_str[7-i])

    group_count = round(len(msg) / 64) - 1

    B = []
    for i in range(0, group_count):
        B.append(msg[(i + 1)*64:(i+2)*64])

    V = []
    V.append(vectors)
    for i in range(0, group_count):
        V.append(sm3_CF(V[i], B[i]))

    y = V[i+1]
    result = ""
    for i in y:
        result = '%s%08x' % (result, i)
    return result

def sm3_KDF(z, keylen):   #z为16进制表示的比特串（str），krylen为密钥长度（单位byte）
    keylen = int(keylen)
    ct = 0x00000001
    rc = math.ceil(keylen/32)
    z = [i for i in bytes.fromhex(z.decode('utf8'))]
    h = ""
    for i in range(rc):
        message = z  + [i for i in binascii.a2b_hex(('%08x' % ct).encode('utf8'))]
        h = h + sm3_Hash(message)
        ct += 1
    return h[0: keylen * 2]

if __name__ == '__main__':
    y = sm3_Hash(bytes2list(b"bear"))
    print(y)
