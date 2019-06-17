import ctypes as ct


def Hash(data):
#    data = ct.c_uint16(data)
    m = int("0xa1b2c3d4",0)
    seed = int("0x1a2b3c4d",0)
    r = 24
    data=str(data)
    length = len(str(data))
    h = seed ^ length
#    h = ct.c_uint16(h)
    currentIndex = 0
    dd = bytes(data, encoding = "utf8")
    ind = 0
    while length >= 4:
        k = dd[ind]
#        print("1--k="+str(k))
        ind += 1
        k|= (dd[ind] << 8)
#        print("2--k="+str(k))
        ind += 1
        k|= (dd[ind] << 16)
#        print("3--k="+str(k)) 
        ind += 1
        k|= (dd[ind] << 24)
#        print("4--k="+str(k))  
#        print("m="+str(m)+",length="+str(length)+",h="+str(h))  
        k = k * m 
        k = k % 4294967296
#        print("m="+str(m)+",length="+str(length)+",h="+str(h)+",k="+str(k))  
        k ^= k >> r
#        print("m="+str(m)+",length="+str(length)+",h="+str(h)+",k="+str(k))  
        k = k * m
        k = k % 4294967296
#        print("m="+str(m)+",length="+str(length)+",h="+str(h)+",k="+str(k))  
        h *= m
        h = h % 4294967296
#        print("m="+str(m)+",length="+str(length)+",h="+str(h)+",k="+str(k))  
        h ^= k
        h = h % 4294967296
#        print("m="+str(m)+",length="+str(length)+",h="+str(h)+",k="+str(k))
        ind += 1  
        length -= 4
    
    if length == 3:
        k = dd[ind+0]
        k |= (dd[ind+1] << 8)
        h ^= k
        h ^= (dd[ind+2] << 16)
        h *= m
        h = h % 4294967296

    if length == 2:
        k = dd[ind+0]
        k |= (dd[ind+1] << 8)
        h ^= k
        h *= m
        h = h % 4294967296

    if length == 1:
        k = dd[ind+0]
        h ^= k
        h *= m
        h = h % 4294967296
#        print("case1: m="+str(m)+",length="+str(length)+",h="+str(h)+",k="+str(k))  

    h ^= (h >> 13)
    h *= m
    h = h % 4294967296
    h ^= (h >> 15)
#    print("m="+str(m)+",length="+str(length)+",h="+str(h)+",k="+str(k))  

    return format(h,'X')


#print(str(Hash("$ANMR,0912000000,19/06/12-16:14:00,100,00000000,00000000,00000000,436F3720,4386D1EE,437C0C3D,42A26FF6,42A61BCC,429D550A,48339980,00000000")) )   
