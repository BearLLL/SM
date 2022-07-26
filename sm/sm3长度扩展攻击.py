import random
import sm3
import struct
import func0

m = str(random.random())
m_Hash = sm3.sm3_Hash(func0.bytes2list(bytes(m,encoding='utf-8')))
m_len = len(m)
other_m = "bear123bear"
pad_str = ""
pad_list = []

def Padding(m):
    mlen = len(m)
    m.append(0x80)
    mlen = mlen + 1
    tail = mlen % 64
    range_end = 56
    if tail >range_end:
        range_end = range_end + 64
    for i in range(tail,range_end):
        m.append(0x00)
    bit_len = (mlen - 1) * 8
    m.extend([int(x) for x in struct.pack('>q',bit_len)])
    for j in range(int((mlen-1)/64)*64+(mlen-1)%64,len(m)):
        global pad_list
        pad_list.append(m[j])
        global pad_str
        pad_str += str(hex(m[j]))
    return m

def guess(hash1,ml,other_m):
    vectors = []
    mm = ""
    for i in range(0,len(hash1),8):
        vectors.append(int(hash1[i:i+8],16))

    if ml > 64:
        for i in range(0,int(ml/64) * 64):
            mm += 'a'

    for i in range(0,ml % 64):
        mm += 'a'
    mm = func0.bytes2list(bytes(mm,encoding='utf-8'))
    mm = Padding(mm)
    mm.extend(func0.bytes2list(bytes(other_m,encoding='utf-8')))
    return sm3.sm3_hash(mm,vectors)

guess_hash = guess(m_Hash,m_len,other_m)
new_m = func0.bytes2list(bytes(m,encoding='utf-8'))
new_m.extend(pad_list)
new_m.extend(func0.bytes2list(bytes(other_m,encoding='utf-8')))
new_m_str = m + pad_str + other_m

hash2 = sm3.sm3_Hash(new_m)

print("生成m")
print("m: ",m)
print("m length:%d" % len(m))
print("m hash:" + m_Hash)
print("附加消息:", other_m)
print("-----------------------------------------------------")
print("计算人为构造的消息的hash值")
print("hash_guess:" , guess_hash)
print("-----------------------------------------------------")
print("验证攻击是否成功")
print("计算hash(m+padding+m')")
print("new message: \n" + new_m_str)
print("hash(new message):" + hash2)
if hash2 == guess_hash:
    print("攻击成功!")
else:
    print("攻击失败...")


























    
        
