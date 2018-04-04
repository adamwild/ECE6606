from galois import *

def generate_GF2(m, q=3, pol = []):
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
    while len(sol) <2*q**m:
        curr_deg += 1
        curr_op.append(0)
        sol['a^'+str(curr_deg)] = pol_to_gal(curr_op, sol, q,q)
    
    return sol


gf = generate_GF(4,2, [1, 0, 0, 1, 1])
r_GF = rev_dic(gf)

sol1 = []
garbage = []
for i in gf:
    for j in gf:
        if (i,j) not in garbage:
            if add_vect_mod(gf[i],gf[j], 2) == gf['a^3']:
                garbage.append((i,j))
                garbage.append((j,i))
                sol1.append((i,j))

##b = [1,0,0,0,1]
##gf['a^16'] = pol_to_gal(b, gf, 2)
gf2 = generate_GF2(4,2, [1, 0, 0, 1, 1])

def interprete(cle):
    if cle == '0' or cle=='1':
        return cle
    elif cle =='a':
        return 'a^2'
    else:
        return 'a^'+str(2*int(cle[2:]))
    
print('Part a')
for tupl in sol1:
    val = (interprete(tupl[0]), interprete(tupl[1]))
    if add_vect_mod(gf2[val[0]],gf2[val[1]], 2) == gf['a^6']:
        print tupl

print('')
print('Part b')
for tupl in sol1:
    val = (interprete(tupl[0]), interprete(tupl[1]))
    if add_vect_mod(gf2[val[0]],gf2[val[1]], 2) == gf['a']:
        print tupl

    
