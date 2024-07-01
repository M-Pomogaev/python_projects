from polinomial import Polinom, int_to_polinom
import numpy as np
import itertools as it

def find_classes(field, mod):
    classes = []
    for i in range(mod):
        classes.append([i])
        num = i
        while (num * field % mod != i):
            num = num * field % mod
            classes[i].append(num)
    ans = set()
    for i in classes:
        i.sort()
        ans.add(tuple(i))
    return ans

def powerset(iterable):
    s = list(iterable)
    return it.chain.from_iterable(it.combinations(s, r) for r in range(len(s)+1))
    
class Field:
    def __init__(self, polinom: Polinom) -> None:
        self.polinom = polinom
        self.p = polinom.field
        self.m = polinom.degree
        self.n = np.power(self.p, self.m)
        self.find_alpha()
        
    def polinom_in_field(self, polinom: Polinom):
        return polinom % self.polinom
    
    def check_order(self, el_order):
        if ((self.n-1) % el_order != 0):
            raise Exception("n must be multiple of el_order")
        
    def find_alpha(self):
        for i in range(1, self.n):
            self.alpha = int_to_polinom(i, self.p)
            self.field = self.find_circle(self.alpha)
            if (len(self.field) == self.n):
                break
              
    def find_circle(self, alpha: Polinom):
        circle = [Polinom([1], self.p)]
        if (alpha == 1):
            return circle
        pol = alpha
        circle.append(pol)
        while (pol != 1):
            pol = (pol * alpha) % self.polinom
            circle.append(pol)
        return circle
    
    def print_field(self, el_order):
        self.check_order(el_order)
        step = self.n // el_order
        print("polinom:", self.polinom)
        print("alpha:", self.alpha_n(step))
        for i in range(0, self.n, step):
            print(i // step, " -> ", self.field[i])
            
    def alpha_n(self, n):
        pol = np.power(self.alpha, n)
        return pol % self.polinom
    def minus_one_power(self, pol):
        pol = self.polinom_in_field(pol)
        negative = self.alpha_n(1)
        while self.polinom_in_field(negative * pol) != 1:
            negative = negative * self.alpha_n(1)
        return self.polinom_in_field(negative)
    
    def pol_to_power(self, pol):
        pol = self.polinom_in_field(pol)
        if pol == 0:
            return -1
        power = 0
        while self.polinom_in_field(self.alpha_n(power)) != pol:
            power += 1
        return power
    
    def find_minpolinoms(self, el_order):
        self.check_order(el_order)
        step = self.n // el_order
        classes = find_classes(self.p, el_order)
        self.minpols = dict()
        for i in classes:
            coefs = []
            for j in powerset(i):
                lenj = len(j)
                if (lenj == 0):
                    continue
                coef = Polinom([((-1)**lenj)], self.p)
                for k in j:
                    coef = coef * self.alpha_n(k*step)
                if (lenj > len(coefs)):
                    coefs.append(coef)
                else: 
                    coefs[lenj-1] += coef
            coefs.reverse()
            coefs_ = [i % self.polinom for i in coefs]
            coefs_ = [int(i) for i in coefs_]
            coefs_.append(1)
            self.minpols[i] = Polinom(coefs_, self.p)
            
def print_classes(field):
    print("classes:", field.classes)
    for i in field.classes:
        print(i,":")
        for j in i:
            print("    ", j, ": ",field.alpha_n(j))
    
def print_minpolinoms(field, el_order):
    field.find_minpolinoms(el_order)
    for i in field.minpols:
        print(i, ":\n   ", field.minpols[i])
        
def find_Rid_Solomin(field, delta, b):
    powers = [i for i in range(b, delta + b - 1)]
    coefs = []
    for j in powerset(powers):
        lenj = len(j)
        if (lenj == 0):
            continue
        pow = 0
        for k in j:
            pow = (pow + k) % (field.n - 1)
        coef = Polinom([(-1)**lenj], field.p) * field.alpha_n(pow)
        if (lenj > len(coefs)):
            coefs.append(coef)
        else: 
            coefs[lenj-1] += coef
    coefs.reverse()
    coefs = [field.pol_to_power(i) for i in coefs]
    coefs.append(0)
    return coefs
    
    
        
def locator_polinom(field, e1, e3):
    b = e1
    c = 1
    e1_negative = field.minus_one_power(b)
    a = field.polinom_in_field((b*b*b + e3)*e1_negative)
    print("a: ", a, "b: ", b, "c: ", c)
    neg_b = field.minus_one_power(b) 
    d = field.polinom_in_field(a * neg_b * neg_b * c)
    print("d  ",d)
    u = []
    for i in range(0, field.n - 1):
        pol = field.alpha_n(i) + field.alpha_n(2*i)
        if d == field.polinom_in_field(pol):
            u.append(field.alpha_n(i))
    for i in u:
        pol = field.minus_one_power(a) * b * i
        print("x: ", field.minus_one_power(field.polinom_in_field(pol)))
    
    
            
def test():
    field = Field(Polinom([1, 0, 0, 1, 1], 2))
    field.print_field(80)
    print_classes(field)
    print_minpolinoms(field)
    
    
if __name__ == "__main__":
    #test()
    #classes = find_classes(3, 80)
    #for i in classes:
    #    print(i,":")
    field = Field(Polinom([2, 2, 1], 3))
    field.print_field(8)
    print_minpolinoms(field, 8)
    locator_polinom(field, field.alpha_n(7), field.alpha_n(5))
    #print(find_Rid_Solomin(field, 5, 1))
    
    
            