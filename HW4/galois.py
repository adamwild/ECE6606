from polynome import *

def incr(p, q=3):
    i = len(p)-1
    while p[i]>=(q-1):
        p[i] = 0
        i -= 1
    p[i] +=1

def generate_monic(deg, q=3):
    #Generates all monics of a given degree for a given field
    base = [1]
    sol = []
    while len(base)<=deg:
        base.append(0)
    sol.append(Poly(list(base)))
    while True:
        incr(base, q)
        if base[0] !=2:
            sol.append(Poly(list(base)))
        else:
            break
    
    return(sol)
    

def monic_polynomials(m,q=3):
    base = []
    for i in range(1,m):
        base.extend(generate_monic(i,q))
                
    mon_elim = generate_monic(m,q)
    for i in range(len(base)):
        for j in range(len(base)):
            a = Poly(list(base[i].pol))
            b = Poly(list(base[j].pol))
            pol = a*b
            for k in mon_elim:
                if k==pol:
                    mon_elim.remove(k)
    
    return mon_elim

def get_prim_elt(m, q=3):
    #Fetches a primitive polynomial for GF(q^m)
    monics = monic_polynomials(m,q)
    for pol in monics:
        if pol.deg() == m and pol.is_prim():
            return pol

def add_vect_mod(a,b, mod):
    sol = [0]*len(a)
    for i in range(len(a)):
        sol[i] = (a[i]+b[i]) %mod
    return sol


def scal_vect_mod(a,b,mod):
    sol = [0]*len(b)
    for i in range(len(b)):
        sol[i] = (a*b[i]) %mod
    return sol

def pol_to_gal(pol, dic, mod, q=3):
    vect=[0]*len(dic['0'])
    for i in range(len(pol)):
        if len(pol)-(i+1) == 0:
            vect = add_vect_mod(vect,scal_vect_mod(pol[i],dic['1'],mod),mod)
        elif len(pol)-(i+1) == 1:
            vect = add_vect_mod(vect,scal_vect_mod(pol[i],dic['a'],mod),mod)
        else:
            vect = add_vect_mod(vect,scal_vect_mod(pol[i],dic['a^'+str(len(pol)-(i+1))],mod),mod)
    return vect

def generate_GF(m, q=3, pol = []):
    #Generates the Galois Field q^m from the primitive polynomial pol
    if pol == []:
        pol=get_prim_elt(m,q)
    else:
        pol = Poly(pol)
    sol = {}
    sol['0'] = [0]*m
    for i in range(m):
        if i ==0:
            base = [0]*m
            base[i] = 1
            sol['1'] = base
        elif i ==1:
            base = [0]*m
            base[i] = 1
            sol['a'] = base
        else:
            base = [0]*m
            base[i] = 1
            sol['a^'+str(i)] = base

    
    curr_deg = pol.deg()
    curr_op = scal_vect_mod(-1,list(pol.pol[1:]),q)
    sol['a^'+str(curr_deg)] = pol_to_gal(curr_op, sol, q,q)
    while len(sol) <q**m:
        curr_deg += 1
        curr_op.append(0)
        sol['a^'+str(curr_deg)] = pol_to_gal(curr_op, sol, q,q)
    
    return sol

def rev_dic(dic):
    sol = {}
    for i in dic:
        sol[str(dic[i])] = i
    return sol

def check_GF(dic):
    #Checks if a GF has been contructed properly
    sol = []
    for i in dic:
        if dic[i] not in sol:
            sol.append(dic[i])
        else:
            return False
    return True

def print_GF(dic):
    print '0 = ' + str(dic['0'])
    print '1 = ' + str(dic['1'])
    print 'a = ' + str(dic['a'])
    for i in range (3,len(dic)):
        print 'a^'+str(i-1)+' = ' + str(dic['a^'+str(i-1)])

if __name__ == "__main__":
    gf = generate_GF(2,3)
    print_GF(gf)
    print check_GF(gf)

    print('-----')
    gf = generate_GF(4,2, [1, 0, 0, 1, 1])
    print_GF(gf)
    print check_GF(gf)
    
