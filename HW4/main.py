from galois import *

#We will compute over GF(3^m), choose m :
m=2

#Please do NOT modify these 2 lines!
gf = generate_GF(m,3)
r_GF = rev_dic(gf)


#Choose the elements you want to add/multiply together:
#Highest order comes first, i.e. [2,1,0,1] = 2a^3 + 1a^2 + 0a + 1

a = [1,1,-1,1,1] 
b = [1,2,1,2]


def add(a,b):
    a = pol_to_gal(a, gf, 3)
    b = pol_to_gal(b, gf, 3)
    sol = add_vect_mod(a,b, 3)

    return r_GF[str(sol)]

def mult(a,b):
    a = Poly(list(a))
    b = Poly(list(b))
    sol = a*b
    sol = sol.pol
    sol = pol_to_gal(sol, gf, 3)
    
    return r_GF[str(sol)]

#Final results:
print(add(a,b))
print(mult(a,b))
    
