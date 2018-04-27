from pb2 import *
from viterbi import *

import numpy as np
import time

import pylab
import matplotlib.pyplot as plt

def zero_pad(mes, n=3):
    cpt = 0
    while len(mes)%n !=0:
        mes += '0'
        cpt += 1
    return mes, cpt

def depad(mes, cpt):
    return mes[:-cpt]

def list_str(liste):
    sol = ''
    for i in liste:
        sol += str(i)
    return sol

def get_symb_QPSK_gray(double, Es):
    dic = {}
    dic['00'] = np.sqrt(Es/2)*(-1-1.j)
    dic['01'] = np.sqrt(Es/2)*(-1+1.j)
    dic['11'] = np.sqrt(Es/2)*(1+1.j)
    dic['10'] = np.sqrt(Es/2)*(1-1.j)

    return dic[double]

def get_symb_QPSK_natural(double, Es):
    dic = {}
    dic['10'] = np.sqrt(Es/2)*(-1-1.j)
    dic['01'] = np.sqrt(Es/2)*(-1+1.j)
    dic['00'] = np.sqrt(Es/2)*(1+1.j)
    dic['11'] = np.sqrt(Es/2)*(1-1.j)

    return dic[double]

def hard_decodeQPSK_gray(symb):
    sol = ""
    if symb.real>0:
        sol+='1'
    else:
        sol+='0'
    if symb.imag >0:
        sol+= '1'
    else:
        sol+='0'
    return sol

def hard_decodeQPSK_natural(symb):
    sol = ""
    if symb.imag >0:
        sol+= '0'
    else:
        sol+='1'
    if (symb.imag>0 and symb.real>0) or (symb.imag<0 and symb.real<0):
        sol+='0'
    else:
        sol+='1'
    
    return sol

def comp_ber(X, X_hat):
    val = 0.0
    for i in range(len(X)):
        if X[i] != X_hat[i]:
            val +=1
    return val/len(X)

def comp_fer(X, X_hat, len_frame):
    val = 0.0
    for i in range(len(X)/len_frame):
        if X[len_frame*i:len_frame*(i+1)] != X_hat[len_frame*i:len_frame*(i+1)]:
            val +=1
    return val/len(X)
    

def simulation1(len_mes = 50, dB = 2, n = 1):
    #Hard decoding, gray constellation

    #fm = gen_FSM('101','111')
    fm = gen_FSM('10100111','11111001')
    
    N0 = 1.8
    #dB = 2
    Eb = N0*10**(float(dB)/10)
    Es = (2*Eb)/n
    sigma2 = N0/2

    #Creating initial message X
    X = np.random.randint(2, size=len_mes)
    X = list_str(X)

    #Coding using f_enc
    #X_enc = conv1(X)
    X_enc = conv2(X)

    #Padding to prepare for QPSK
    #Not needed for 1/2 convolutional codes


    #Encoding onto QPSK symbols
    QPSK = []
    for i in range(len(X_enc)/2):
        x_pair = X_enc[(i*2):((i+1)*2)]
        symbol = get_symb_QPSK_gray(x_pair, Es) #Modify here for QPSK change
        QPSK.append(symbol)

    #Transmitting, i.e. adding WGN
    for i in range(len(QPSK)):
        QPSK = QPSK + np.random.normal(0,sigma2,len(QPSK))+ 1.j *np.random.normal(0,sigma2,len(QPSK))
        

    #Hard decoding QPSK
    X_enc_hat = ''
    for symb in QPSK:
        X_enc_hat += hard_decodeQPSK_gray(symb) #Modify here for QPSK change


    #De-padding
    #Not needed here

    #Estimate
    p = comp_ber(X_enc, X_enc_hat)
    X_hat = viterbi1(X_enc_hat, fm, p)

    ber = comp_ber(X, X_hat)
    fer = comp_fer(X, X_hat, 2)
    return ber, fer

def simulation2(len_mes = 50, dB = 2, n = 1):
    #Hard decoding, natural constellation

    #fm = gen_FSM('101','111')
    fm = gen_FSM('10100111','11111001')
    
    N0 = 1.8
    #dB = 2
    Eb = N0*10**(float(dB)/10)
    Es = (2*Eb)/n
    sigma2 = N0/2

    #Creating initial message X
    X = np.random.randint(2, size=len_mes)
    X = list_str(X)

    #Coding using f_enc
    #X_enc = conv1(X)
    X_enc = conv2(X)

    #Padding to prepare for QPSK
    #Not needed for 1/2 convolutional codes


    #Encoding onto QPSK symbols
    QPSK = []
    for i in range(len(X_enc)/2):
        x_pair = X_enc[(i*2):((i+1)*2)]
        symbol = get_symb_QPSK_gray(x_pair, Es) #Change here for Gray/Natural
        QPSK.append(symbol)

    #Transmitting, i.e. adding WGN
    for i in range(len(QPSK)):
        QPSK = QPSK + np.random.normal(0,sigma2,len(QPSK))+ 1.j *np.random.normal(0,sigma2,len(QPSK))
        

    #Soft decoding QPSK
    X_enc_hat = QPSK


    #De-padding
    #Not needed here

    #Estimate
    X_hat = viterbi2(X_enc_hat, fm, Es)

    ber = comp_ber(X, X_hat)
    fer = comp_fer(X, X_hat, 2)
    return ber, fer

def temps_simu(temps, values = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
    sol = []
    BER = []
    FER = []
    for decib in values:
        print decib
        t0 = time.time()
        nbre_simu = 0
        b, f = 0.0, 0.0
        while (time.time() - t0 < temps):
            nbre_simu += 1
            b1, f1 = simulation3(len_mes = 51, dB = decib, n = 3)
            b += b1
            f += f1
        b = b/nbre_simu
        f = f/nbre_simu
        BER.append(b)
        FER.append(f)
    print (BER, FER)
    return BER, FER
    


if __name__ == "__main__":
    (Ber,Fer) = temps_simu(10, [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 23, 25])
