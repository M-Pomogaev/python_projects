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
    
    def find_minpolinoms(self, el_order):
        self.check_order(el_order)
        step = self.n // el_order
        classes = find_classes(self.p, el_order)
        self.minpols = dict()
        for i in classes:
            coefs = []
            for j in powerset(i):
                coef = Polinom([-1], self.p)
                for k in j:
                    coef = coef * self.alpha_n(k*step)
                lenj = len(j)
                if (lenj == 0):
                    continue
                if (lenj > len(coefs)):
                    coefs.append(coef)
                else: 
                    coefs[lenj-1] += coef
            coefs.reverse()
            coefs_ = [i % self.polinom for i in coefs]
            coefs_.append(Polinom([1], self.p))
            self.minpols[i] = coefs_
            
def print_classes(field):
    print("classes:", field.classes)
    for i in field.classes:
        print(i,":")
        for j in i:
            print("    ", j, ": ",field.alpha_n(j))
    
def print_minpolinoms(field, el_order):
    field.find_minpolinoms(el_order)
    for i in field.minpols:
        print(i,":")
        for j in field.minpols[i]:
            print("    ", j)
            
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
    field = Field(Polinom([2, 0, 0, 0, 1], 5))
    field.print_field(13)
    print_minpolinoms(field, )
    
            