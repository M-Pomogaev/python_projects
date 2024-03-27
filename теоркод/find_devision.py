from polinomial import Polinom
import numpy as np

class Devisor:
    def __init__(self, field):
        self.field = field
        
    def int_to_polinom(self, num):
        coef = []
        while num > 0:
            coef.append(num % self.field)
            num //= self.field
        return Polinom(coef, self.field)
        
    def find_devision(self, devidend):
        dev = devidend.copy()
        devisors = []
        num = self.field
        polinom = self.int_to_polinom(num)
        while dev.degree > polinom.degree:
            if dev % polinom == 0:
                devisors.append(polinom)
                dev = dev / polinom
            num += 1
            polinom = self.int_to_polinom(num)
        devisors.append(dev)
        return devisors
            
def find_result(pol):
    devisor = Devisor(pol.field)
    print("pol:", pol)
    devisors = devisor.find_devision(pol)
    for i in devisors:
        print("    pol/", i)
    pol = Polinom([1], 3)
    for i in devisors:
        pol = pol * i
    print("pol:", pol)

def test():
    devisor = Devisor(5)
    print("5 to pol", devisor.int_to_polinom(5))
    print("1+5*2+5**2*3+5**3*4+5**4*4+5**5*5 to pol", devisor.int_to_polinom(1+5*2+5**2*3+5**3*4+5**4*4+5**5*5))
    find_result(Polinom([1, 2, 1],5))
    find_result(Polinom.make_xn_polinom(10, 1, 3) - Polinom([1], 3))
    find_result(Polinom.make_xn_polinom(13, 1, 5) - Polinom([1], 5))
    find_result(Polinom.make_xn_polinom(9, 1, 7) - Polinom([1], 7))
    
    
    
if __name__ == "__main__":
    test()
