import numpy as np
import time

import pylab
import matplotlib.pyplot as plt

import pb1
import pickle
B = np.array([[1,1,0,1,1,1,0,0,0,1,0,1],[1,0,1,1,1,0,0,0,1,0,1,1],[0,1,1,1,0,0,0,1,0,1,1,1],[1,1,1,0,0,0,1,0,1,1,0,1],[1,1,0,0,0,1,0,1,1,0,1,1],[1,0,0,0,1,0,1,1,0,1,1,1],[0,0,0,1,0,1,1,0,1,1,1,1],[0,0,1,0,1,1,0,1,1,1,0,1],[0,1,0,1,1,0,1,1,1,0,0,1],[1,0,1,1,0,1,1,1,0,0,0,1],[0,1,1,0,1,1,1,0,0,0,1,1],[1,1,1,1,1,1,1,1,1,1,1,0]])
one = np.eye(12)
G = np.concatenate((B,one),axis=1)
G = G.astype(int)
H = np.concatenate((one,B.T), axis=1)
H = H.astype(int)

synd_table = pickle.load( open( "save.p", "rb" ) )

def encode_rep(mess, k):
    sol = ''
    for i in mess:
        symb = str(i)
        while len(symb)<k:
            symb += i
        sol+= symb
    return sol

def decode_rep(mess,k):
    sol = ''
    for i in range(len(mess)/k):
        symb = mess[k*i:k*(i+1)]
        val = 0
        for j in symb:
            if j =='1':
                val +=1
            else:
                val-=1
        if val>0:
            sol += '1'
        else:
            sol += '0'
    return sol

def comp_ber(X, X_hat):
    val = 0.0
    r1 = len(X)
    r2 = len(X_hat)
    r = min(r1,r2)
    for i in range(r):
        if X[i] != X_hat[i]:
            val +=1
    return val/len(X)

def comp_fer(X, X_hat, len_frame):
    val = 0.0
    for i in range(len(X)/len_frame):
        if X[len_frame*i:len_frame*(i+1)] != X_hat[len_frame*i:len_frame*(i+1)]:
            val +=1
    return val/len(X)

def pad_pair(X):
    if len(X)/2 !=0:
        X += '0'
        return True, X
    else:
        return False, X

def depad_pair(boolean, X):
    if boolean:
        return X[:-1]
    else:
        return X

def decode(mes_received):
    stream1_est = []
    stream2_est = []
    for i in mes_received:
        if i.real > 0:
            stream1_est.append(0)
        else:
            stream1_est.append(1)
        if i.imag > 0:
            stream2_est.append(0)
        else:
            stream2_est.append(1)
    return np.array(stream1_est), np.array(stream2_est)

def str_list(string):
    sol = []
    for i in string:
        sol.append(int(i))
    return sol

def list_str(liste):
    sol = ''
    for i in liste:
        sol += str(i)
    return sol

def simulation(mes_len, dB = 2, n = 1):
    tours_simu = 0

    #Length of repetition code
    #n = 3
    
    N0 = 1.8
    #dB = 2
    Eb = N0*10**(float(dB)/10)
    Es = (2*Eb)/n

    sigma2 = N0/2

    X = np.random.randint(2, size=mes_len)
    X = list_str(X)

    #X_enc = encode_rep(X,n)
    decoding_table, X_enc = pb1.encode(X, G)
    pad,X_enc = pad_pair(X_enc)
    
    s1 = np.array(str_list(X_enc[0:len(X_enc)/2]))
    s2 = np.array(str_list(X_enc[len(X_enc)/2:]))

    s2 = s2[:-1]



    QPSK_symbol = np.sqrt(Es/2)*((1-2*s1) + 1.j*(1-2*s2))

    #Transmission
    message_rec = QPSK_symbol + (np.random.normal(0,sigma2,len(s1))+ 1.j *np.random.normal(0,sigma2,len(s2)))

    #Reception
    s1_rec, s2_rec = decode(message_rec)
    s1_rec = list_str(s1_rec)
    s2_rec = list_str(s2_rec)
    
    X_hat_enc = s1_rec + s2_rec
    X_hat_enc = depad_pair(pad, X_hat_enc)

    #X_hat = decode_rep(X_hat_enc,n)
    X_hat = pb1.decode(X_hat_enc, decoding_table, H, synd_table)
    
    ber = comp_ber(X, X_hat)
    #fer = comp_fer(X, X_hat, 2)
    fer = 0

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
            b1, f1 = simulation(mes_len = 60, dB = decib, n = 3)
            b += b1
            f += f1
        b = b/nbre_simu
        f = f/nbre_simu
        BER.append(b)
        FER.append(f)
    print (BER, FER)
    return BER, FER
        
def plots():
    ber_1 =[0.1542986425339386, 0.12563125012475562, 0.099372045064223, 0.07565472494057864, 0.052368978557429245, 0.03453062640985693, 0.021232474128082383, 0.011205432937181656, 0.005523336095001364, 0.0021208483393357286, 0.000657099300846343, 0.00014364720247073183, 3.13625130154429e-05]
    
    fer_1 = [0.1393939393939418, 0.11531168286792355, 0.09254212337623775, 0.07137911589827221, 0.049814877145743675, 0.033309307385310426, 0.020585263408159492, 0.01094577049835211, 0.005345800291947748, 0.0020808323329331675, 0.0006439573148294162, 0.00014364720247073183, 3.13625130154429e-05]
    
    ber_3 = [0.1537874797958731, 0.12415260677914838, 0.09885185572156889, 0.07542514913915552, 0.053363338217851164, 0.034671532846716216, 0.021415850803207796, 0.011597519802622998, 0.005194032072031832, 0.002175028715266741, 0.0007172805936475012, 0.0001762502753910552, 2.271178741766977e-05]
    fer_3 = [0.1386290854717956, 0.11391396868825317, 0.09207211599856292, 0.07074880161269723, 0.05092108017584424, 0.03331186489194305, 0.020701687775156522, 0.011281002467212014, 0.005097295085016914, 0.002142444015412558, 0.0007107598609779784, 0.00016156275244180062, 2.271178741766977e-05]

    ber_11 = [0.15219555796929504, 0.12494785148102075, 0.09858745209924445, 0.0735754068474154, 0.05254367505094198, 0.034743115353138246, 0.021366911849603695, 0.011711030326688913, 0.005489558684099384, 0.0019117097716935063, 0.0005750100626760964, 0.0001604341487573328, 3.079362879820165e-05]
    fer_11 =[0.13788850797099284, 0.11465908962780319, 0.09184638191938929, 0.06945536246912941, 0.05018316241885903, 0.03341171859690487, 0.02072169359603968, 0.011458917868267138, 0.005330210101106659, 0.0018824115376445637, 0.0005678224368926453, 0.00015345875098527487, 3.079362879820165e-05]

    ber_hw3 = [0.5018831010026904, 0.4965227817745791, 0.4968938844573364, 0.49663542417688034, 0.49056036556036675, 0.46462009803921533, 0.44693130630630645, 0.39266020864381496, 0.3116619115549218, 0.24337349397590347, 0.1436974789915966, 0.09723999052357257, 0.03343852267414678]
    
    values = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    plt.plot(values, ber_hw3, color='blue', lw=1, label='n = 3', marker='o')
    plt.yscale('log')
    plt.xlabel('Power efficiency Eb/N0 (dB)')
    plt.ylabel('Bit Error Rate')
    plt.grid(color='g', linestyle='-', linewidth=0.1)
    plt.title('Bit Error Rate for the Golay code')
    plt.legend()
    plt.show()

#temps_simu(10)
plots()
