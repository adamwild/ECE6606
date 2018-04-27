import numpy as np

def XOR(v1, v2):
    sol = 0
    vect = ''
    for i in range(len(v1)):
        vect += str(int(v1[i]) & int(v2[i]))
    for j in vect:
        sol = sol ^ int(j)
    return str(sol)

def conv(stream):
    state = '000'
    code = ''
    for i in stream:
        print state
        ex_state = i+state
        bit1 = XOR('1011', ex_state)
        bit2 = XOR('1101', ex_state)
        print bit1+bit2
        state = ex_state[0:-1]
        code += bit1
        code += bit2
        
def conv1(stream):
    state = '00'
    code = ''
    FSM = {}
    for i in stream:
        ex_state = i+state
        if ex_state not in FSM:
            bit1 = XOR('101', ex_state)
            bit2 = XOR('111', ex_state)
            out = bit1+bit2
            FSM[ex_state] = out
        state = ex_state[0:-1]
        code += FSM[ex_state]
    return code

def conv2(stream):
    state = '0000000'
    code = ''
    FSM = {}
    for i in stream:
        ex_state = i+state
        if ex_state not in FSM:
            bit1 = XOR('10100111', ex_state)
            bit2 = XOR('11111001', ex_state)
            out = bit1+bit2
            FSM[ex_state] = out
        state = ex_state[0:-1]
        code += FSM[ex_state]
    return code

def gen_FSM(v1, v2):
    #key[1:] is the current state, key[0] is the input bit
    FSM = {}
    n = len(v1)-1
    for i in range(2**n):
        s = bin(i)[2:]
        while len(s)<n:
            s = '0'+s
        s0 = '0'+s
        FSM[s0] = XOR(v1, s0) + XOR(v2, s0)
        s1 = '1'+s
        FSM[s1] = XOR(v1, s1) + XOR(v2, s1)
    return FSM

def MU(a,b,p):
    #Computes -log(prob(a|b)) with flip probability of p
    pr = 1.0
    for i in range(len(a)):
        if a[i] == b[i]:
            pr = pr*(1-p)
        else:
            pr = pr*p
    return -np.log(pr)

def inv(string):
    sol = ''
    for i in string:
        sol+= str(1-int(i))
    return sol

def viterbi1(code, FSM, p):
    for i in FSM:
        h = len(i)-1
        break
    curr = ''
    while len(curr)<h:
        curr += '0'
    curr_states = [[curr, 0, '']] #state, weight, decoded message

    for i in range(len(code)/2):
        r = code[(i*2):((i+1)*2)]
        reached = {}
        for st in curr_states:
            #We start from a state previously reached at time t and update
            #states at time t+1
            reach1 = '1' + st[0]
            mu = MU(r, FSM[reach1], p)
            weight = st[1] + mu
            if reach1 not in reached or weight<reached[reach1][1]:
                if reach1 in reached:
                    del reached[reach1]
                reached[reach1] = [reach1[:-1], weight, st[2]+'1']

            reach0 = '0' + st[0]
            mu = MU(r, FSM[reach0], p)
            weight = st[1] + mu
            if reach0 not in reached or weight<reached[reach0][1]:
                if reach0 in reached:
                    del reached[reach0]
                reached[reach0] = [reach0[:-1], weight, st[2]+'0']
                
        curr_states = []
        for j in reached:
            curr_states.append(reached[j])

    #Once the final part of the code is reached, we keep the path that
    #minimizes the log likelihood
    max_w = float('inf')
    for sta in curr_states:
        if sta[1] < max_w:
            sol = sta[2]

    return sol
        
def d_natural(cplx, symbol, Es):
    dic = {}
    dic['10'] = np.sqrt(Es/2)*(-1-1.j)
    dic['01'] = np.sqrt(Es/2)*(-1+1.j)
    dic['00'] = np.sqrt(Es/2)*(1+1.j)
    dic['11'] = np.sqrt(Es/2)*(1-1.j)
    symb_cplx = dic[symbol]
	
    return np.sqrt((symb_cplx.real - cplx.real)**2+(symb_cplx.imag - cplx.imag)**2)

def d_gray(cplx, symbol, Es):
    dic = {}
    dic['00'] = np.sqrt(Es/2)*(-1-1.j)
    dic['01'] = np.sqrt(Es/2)*(-1+1.j)
    dic['11'] = np.sqrt(Es/2)*(1+1.j)
    dic['10'] = np.sqrt(Es/2)*(1-1.j)
    symb_cplx = dic[symbol]
	
    return np.sqrt((symb_cplx.real - cplx.real)**2+(symb_cplx.imag - cplx.imag)**2)

def viterbi2(code, FSM, Es):
    #For soft decoding, natural or gray constellation
    for i in FSM:
        h = len(i)-1
        break
    curr = ''
    while len(curr)<h:
        curr += '0'
    curr_states = [[curr, 0, '']] #state, weight, decoded message

    for r in code:
        reached = {}
        for st in curr_states:
            #We start from a state previously reached at time t and update
            #states at time t+1
            reach1 = '1' + st[0]
            mu = d_gray(r, FSM[reach1], Es) #Change here for Gray/Natural constellation
            weight = st[1] + mu
            if reach1 not in reached or weight<reached[reach1][1]:
                if reach1 in reached:
                    del reached[reach1]
                reached[reach1] = [reach1[:-1], weight, st[2]+'1']

            reach0 = '0' + st[0]
            mu = d_gray(r, FSM[reach0], Es) #Change here for Gray/Natural constellation
            weight = st[1] + mu
            if reach0 not in reached or weight<reached[reach0][1]:
                if reach0 in reached:
                    del reached[reach0]
                reached[reach0] = [reach0[:-1], weight, st[2]+'0']
                
        curr_states = []
        for j in reached:
            curr_states.append(reached[j])

    #Once the final part of the code is reached, we keep the path that
    #minimizes the log likelihood
    max_w = float('inf')
    for sta in curr_states:
        if sta[1] < max_w:
            sol = sta[2]

    return sol   

                
    
    
if __name__ == "__main__":
    #The example introduced in the lecture
    #conv('010110')


    clair = '10010101010010110101110101011011'

    fm = gen_FSM('101','111')
    c1 = conv1(clair)
    print('------')
    print clair
    print viterbi1(c1, fm, 0.1)

    fm = gen_FSM('10100111','11111001')
    c2 = conv2(clair)
    print('------')
    print clair
    print viterbi1(c2, fm, 0.1)
