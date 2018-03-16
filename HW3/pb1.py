import numpy as np
from scipy.special import binom
import pickle

def write(mat):
    sol = ''
    for i in mat:
        if i == '[':
            sol+= '['
        elif i==' ':
            sol+= ','
        elif i==';':
            sol+='],['
        elif i==']':
            sol+= ']]'
        elif i=='0' or i=='1':
            sol+= i
    return sol

def mult_bin_mat(A,B):
    print('A', A)
    print('B', B)
    sol = np.zeros([len(A),len(B[0])])
    for i in range(len(A)):
        for j in range(len(B[0])):
            val = 0
            for k in range(len(A[0])):
                val = val^(A[i,k]*B[k,j])
            sol[i,j] = val
    return sol.astype(int)

def mult_bin_vect_mat(a,B):
    sol = np.zeros(len(B[0]))
    for i in range(len(B[0])):
        val = 0
        for j in range(len(a)):
            val = val^(a[j]*B[j,i])
        sol[i] = val
    return sol.astype(int)

def print_mat(mat):
    sol = ''
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            sol += str(mat[i,j])+' '
        sol+='\n'
    print sol

def binary_vectors(n):
    sol = []
    zeros = np.zeros(n)
    zeros.astype(int)
    for i in range(1,2**n):
        e = []
        str_bin = bin(i)[2:]
        while len(str_bin)<n:
            str_bin = '0' + str_bin
        for j in str_bin:
            e.append(int(j))
        e = np.array(e)
        sol.append(e)
    return sol

def wt(vect):
    if type(vect) == str:
        sol = 0
        for i in vect:
            sol+= int(i)
        return sol
    else:
        return np.sum(vect)

def organize(vectors):
    sol = []
    for vect in vectors:
        if len(sol) == 0:
            sol.append(vect)
        else:
            for i in range(len(sol)):
                if wt(sol[i])>= wt(vect):
                    sol.insert(i,vect)
                    break
                if i == len(sol)-1:
                    sol.append(vect)
                    break
    return sol
            


def enumerate_vect(n):
    sol = []
    for weight in range(n+1):
        for i in range(1, 2**n):
            string = bin(i)[2:]
            if wt(string) == weight:
                vect = []
                for i in string:
                    vect.append(int(i))
                while len(vect)<n:
                    vect.insert(0,0)
                sol.append(vect)
    return sol

def enum_vect(n):
    for weight in range(1,n+1):
        vect = []
        for i in range(weight):
            vect.append(1)
        while len(vect)<n:
            vect.append(0)

        #Do stuff
        #Update vect
        num_vect = int(binom(n, weight))
        print vect
        for i in range(num_vect-1):
            vect = update(vect)
            

def update(vect):
    qte = 1
    n = len(vect)
    ind_fst1 = False
    if vect[n-1] == 0:
        fst_enc_is0 = True
    else:
        fst_enc_is0 = False
    for j in range(1,n):
        if vect[n-j] == 0:
            ind = j+1
            while vect[n-ind] != 1:
                ind +=1
            vect[n-ind] = 0
            for k in range(1,qte+1):
                vect[n-ind+k] = 1
            return vect
        else:
            if fst_enc_is0 is True:
                vect[n-j] = 0
                vect[n-j+1] = 1
                return vect
            else:
                vect[n-j] = 0
                qte += 1

def update_synd_table(e, H, synd_table):
    e = np.array(e)
    synd = mult_bin_vect_mat(e, H.T)
    synd.astype(int)

    zeros = True
    synd_str = ''
    for i in synd:
        if i == 1:
            zeros = False
        synd_str += str(i)
        
    if (not zeros) and (synd_str not in synd_table):
        synd_table[synd_str] = e
    return synd_table

def comp_synd_table(n, H):
    synd_table = {}
    for weight in range(1,n+1):
        vect = []
        for i in range(weight):
            vect.append(1)
        while len(vect)<n:
            vect.append(0)

        #Do stuff
        #Update vect
        num_vect = int(binom(n, weight))
        print vect
        update_synd_table(vect, H, synd_table)
        for i in range(num_vect-1):
            vect = update(vect)
            update_synd_table(vect, H, synd_table)
    return synd_table

def to_vect(string):
    sol = []
    for i in string:
        sol.append(int(i))
    return sol

def to_string(vect):
    sol = ''
    for i in vect:
        sol+= str(i)
    return sol

def encode(mes, G):
    decoding = {}
    enc = ''
    while len(mes)%12 !=0:
        mes += '0'

    for i in range(len(mes)/12):
        cur = mes[i*12:(i+1)*12]
        cur_vect = to_vect(cur)
        code = mult_bin_vect_mat(cur_vect, G)
        code_str = to_string(code)
        enc += code_str
        if cur not in decoding:
            decoding[code_str] = cur
            
    return decoding, enc

def decode(code, dic_decode, H, synd_table):
    sol = ''
    for i in range(len(code)/24):
        cur = code[i*24:(i+1)*24]
        cur_vect = to_vect(cur)
        synd = mult_bin_vect_mat(cur_vect, H.T)
        synd_str = to_string(synd)
        if synd_str == '000000000000':
            if cur not in dic_decode:
                sol+='000000000000'
            else:
                sol += dic_decode[cur]
        else:
            if synd_str not in synd_table:
                sol += '000000000000'
            else:
                error = synd_table[synd_str]
                corrected = ''
                for i in range(len(error)):
                    corrected += str(int(error[i])^int(cur[i]))
                    if corrected not in dic_decode:
                        sol += '000000000000'
                    else:
                        sol += dic_decode[corrected]
        return sol

"""
B = np.array([[1,1,0,1,1,1,0,0,0,1,0,1],[1,0,1,1,1,0,0,0,1,0,1,1],[0,1,1,1,0,0,0,1,0,1,1,1],[1,1,1,0,0,0,1,0,1,1,0,1],[1,1,0,0,0,1,0,1,1,0,1,1],[1,0,0,0,1,0,1,1,0,1,1,1],[0,0,0,1,0,1,1,0,1,1,1,1],[0,0,1,0,1,1,0,1,1,1,0,1],[0,1,0,1,1,0,1,1,1,0,0,1],[1,0,1,1,0,1,1,1,0,0,0,1],[0,1,1,0,1,1,1,0,0,0,1,1],[1,1,1,1,1,1,1,1,1,1,1,0]])
one = np.eye(12)
G = np.concatenate((B,one),axis=1)
G = G.astype(int)
H = np.concatenate((one,B.T), axis=1)
H = H.astype(int)"""


"""
synd_table = pickle.load( open( "save.p", "rb" ) )
decoding_table, coded = encode('110101101111000011110000',G)
decode(coded, decoding_table, H)



print_mat(G)
print_mat(H)
print_mat(mult_bin_mat(G,H.T))
"""

