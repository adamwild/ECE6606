from viterbi import *
from simu import *

import numpy as np

def get_symb_8psk_gray(triple, Es):
    dic = {}
    dic['111'] = np.sqrt(Es/2)*(1)
    dic['110'] = np.sqrt(Es/2)*(1+1.j)
    dic['010'] = np.sqrt(Es/2)*(1.j)
    dic['011'] = np.sqrt(Es/2)*(-1+1.j)

    dic['001'] = np.sqrt(Es/2)*(-1)
    dic['000'] = np.sqrt(Es/2)*(-1-1.j)
    dic['100'] = np.sqrt(Es/2)*(-1.j)
    dic['101'] = np.sqrt(Es/2)*(1-1.j)

    return dic[triple]

def get_symb_8psk_natural(triple, Es):
    dic = {}
    dic['000'] = np.sqrt(Es/2)*(1)
    dic['001'] = np.sqrt(Es/2)*(1+1.j)
    dic['010'] = np.sqrt(Es/2)*(1.j)
    dic['011'] = np.sqrt(Es/2)*(-1+1.j)

    dic['100'] = np.sqrt(Es/2)*(-1)
    dic['101'] = np.sqrt(Es/2)*(-1-1.j)
    dic['110'] = np.sqrt(Es/2)*(-1.j)
    dic['111'] = np.sqrt(Es/2)*(1-1.j)

    return dic[triple]

def decode_8psk_natural(symb, Es):
    dic = {}
    sol=None
    dic['000'] = np.sqrt(Es/2)*(1)
    dic['001'] = np.sqrt(Es/2)*(1+1.j)
    dic['010'] = np.sqrt(Es/2)*(1.j)
    dic['011'] = np.sqrt(Es/2)*(-1+1.j)

    dic['100'] = np.sqrt(Es/2)*(-1)
    dic['101'] = np.sqrt(Es/2)*(-1-1.j)
    dic['110'] = np.sqrt(Es/2)*(-1.j)
    dic['111'] = np.sqrt(Es/2)*(1-1.j)

    dist = float('inf')
    for i in dic:
        val = dic[i]
        d = np.sqrt((symb.real - val.real)**2+(symb.imag - val.imag)**2)
        if d<dist:
            dist = d
            sol = i
    return sol

def decode_8psk(symb, Es):
    dic = {}
    sol = None
    dic['111'] = np.sqrt(Es/2)*(1)
    dic['110'] = np.sqrt(Es/2)*(1+1.j)
    dic['010'] = np.sqrt(Es/2)*(1.j)
    dic['011'] = np.sqrt(Es/2)*(-1+1.j)

    dic['001'] = np.sqrt(Es/2)*(-1)
    dic['000'] = np.sqrt(Es/2)*(-1-1.j)
    dic['100'] = np.sqrt(Es/2)*(-1.j)
    dic['101'] = np.sqrt(Es/2)*(1-1.j)

    dist = float('inf')
    for i in dic:
        val = dic[i]
        d = np.sqrt((symb.real - val.real)**2+(symb.imag - val.imag)**2)
        if d<dist:
            dist = d
            sol = i
    return sol

def simulation3(len_mes = 50, dB = 2, n = 1):
    #Simulation for problem 2

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
    for i in range(len(X_enc)/3):
        x_pair = X_enc[(i*3):((i+1)*3)]
        symbol = get_symb_8psk_natural(x_pair, Es) #Modify here for QPSK change
        QPSK.append(symbol)

    #Transmitting, i.e. adding WGN
    for i in range(len(QPSK)):
        QPSK = QPSK + np.random.normal(0,sigma2,len(QPSK))+ 1.j *np.random.normal(0,sigma2,len(QPSK))
        

    #Hard decoding QPSK
    X_enc_hat = ''
    for symb in QPSK:
        X_enc_hat += decode_8psk_natural(symb, Es) #Modify here for QPSK change


    #De-padding
    #Not needed here

    #Estimate
    p = comp_ber(X_enc, X_enc_hat)
    
    X_hat = viterbi1(X_enc_hat, fm, p)

    ber = comp_ber(X, X_hat)
    fer = comp_fer(X, X_hat, 2)
    return ber, fer
            
