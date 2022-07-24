import random

def xor(a,b):   #异或
    return list(map(lambda x,y:x^y,a,b))

def rol(x,n):   #循环左移
    return ((x<<n)&0xffffffff)|((x>>(32-n))&0xffffffff)

def get_uint32(n):
    return (n[0]<<24)|(n[1]<<16)|(n[2]<<8)|n[3]

def put_uint32(n):
    return [((n>>24)&0xff),((n>>16)&0xff),((n>>8)&0xff),(n&0xff)]

def padding(data,block=16):#填充,block=16
    l=len(data)
    return data+[(16-l%block) for _ in range(16-l%block)]

def unpadding(data):
    return data[:16-data[-1]]

def list2bytes(data):
    return b''.join([bytes((i,)) for i in data])

def bytes2list(data):
    return [i for i in data]

def rand_hex(l):
    return ''.join([random.choice('0123456789abcdef') for _ in range(l)])
