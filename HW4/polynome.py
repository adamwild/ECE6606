class Poly():

    def __init__(self, l = [0]):
        self.pol = l
        self.len = self.length()

    def deg(self):
        return self.length()-1

    def length(self):
        return len(self.pol)

    def mod(self, n=3):
        for i in range(self.length()):
            self.pol[i] = self.pol[i]%n

    def clean(self):
        while self.length() >1 and self.pol[0] == 0:
            self.pol = self.pol[1:]

    def __str__(self):
        s = ''
        incr = 0
        self.clean()
        if self.pol == [0]:
            return '0'
        for i in self.pol:
            incr += 1
            if i != 0:
                if i <0:
                    w = '- '+str(-i)
                else:
                    w = '+ '+str(i)
                if self.len-incr == 0:
                    s += w

                elif self.len-incr == 1:
                    if i >0:
                        s += '+'+str(i)+'x '
                    else:
                        s += '-'+str(-i)+'x '

                elif i == 1:
                    s += 'x^'+str(self.len-incr)+" "
                elif i == -1:
                    s += '-x^'+str(self.len-incr)+" "
                else:
                    s += w+'x^'+str(self.len-incr)+" "
        while s[0]==' ' or s[0]=='+':
            s = s[1:]
        return s

    def __add__(self, poly):
        p1 = self.pol
        p2 = poly.pol
        deg = max(self.deg(), poly.deg())
        sol = [0]*(deg+1)

        while len(p1)!=len(sol):
            p1.insert(0,0)
        while len(p2)!=len(sol):
            p2.insert(0,0)

        for i in range(len(sol)):
            sol[i] = p1[i]+p2[i]

            
        sol = Poly(list(sol))
        sol.mod()
        sol.clean()
        sol.len=sol.length()
        
        return sol

    def __sub__(self, poly):
        p1 = self.pol
        p2 = poly.pol
        deg = max(self.deg(), poly.deg())
        sol = [0]*(deg+1)

        while len(p1)!=len(sol):
            p1.insert(0,0)
        while len(p2)!=len(sol):
            p2.insert(0,0)

        for i in range(len(sol)):
            sol[i] = p1[i]-p2[i]

        sol = Poly(list(sol))
        sol.mod()
        sol.clean()
        sol.len=sol.length()
        
        return sol

    def __mul__(self, poly):
        p1 = self.pol
        p2 = poly.pol
        p1.reverse()
        p2.reverse()
        deg = self.deg()+poly.deg()
        sol = [0]*(deg+1)



        for i in range(len(p1)):
            for j in range(len(p2)):
                sol[i+j] += p1[i]*p2[j]

        sol.reverse()
        sol = Poly(list(sol))
        sol.mod()
        sol.clean()
        return sol
        

    def __mod__(self, poly):
        p1 = Poly(list(self.pol))
        p2 = Poly(list(poly.pol))
        p1.mod()
        p2.mod()
        zero = Poly()
        quot = Poly()
        while p1 != zero and p1.deg() >= p2.deg():
            q_int = [p1.pol[0]/p2.pol[0]]
            while len(q_int)<=p1.deg()-p2.deg():
                q_int.append(0)
            q_int = Poly(q_int)
            to_sub = q_int*p2
            p1 = p1-to_sub
            #quot = quot + q_int
        return p1

    def __eq__(self, poly):
        self.clean()
        self.mod()
        poly.clean()
        poly.mod()

        return self.pol==poly.pol

    def is_prim(self, q=3,m=2):
        #Will test divisibility until x^(q^m-1)-2
        zero = Poly()
        curr_p = Poly([1,-1])
        while curr_p.deg()<(q**m)-2:
            if curr_p%self == zero:
                return False
            curr_p.pol.insert(1,0)
            curr_p.len = curr_p.length()
        return True

        

if __name__ == "__main__":
    A = Poly([2,0,0,-1])
    B = Poly([1,0,1])
    C = Poly([2, 0, 0, 2])
    D = Poly([2, 0, 2, 0])
    E = Poly([1,0,-1])
    F = Poly([1,0,0,0,-1])
    G = Poly([1,0,0,-1])
    H = Poly([1,1,2])
    print(F)
    print(B)
    print(F%B)
    print('-----')
    print(B)
    print(B.is_prim())
    print('-----')
    print(H)
    print(H.is_prim())
