from polinomial import Polinom, int_to_polinom
import numpy as np

class Devisor:
    def __init__(self, field):
        self.field = field
        
    def find_devision(self, devidend):
        dev = devidend.copy()
        devisors = []
        num = self.field
        polinom = int_to_polinom(num, self.field)
        while dev.degree > polinom.degree:
            if dev % polinom == 0:
                devisors.append(polinom)
                dev = dev / polinom
            num += 1
            polinom = int_to_polinom(num, self.field)
        devisors.append(dev)
        return devisors
    
def find_undivisable(field, n):
    devisor = Devisor(field)
    num = field**n
    while len(devisor.find_devision(int_to_polinom(num, field))) > 1:
        num += 1
    return int_to_polinom(num, field)
            
def find_result(pol):
    devisor = Devisor(pol.field)
    print("pol:", pol)
    devisors = devisor.find_devision(pol)
    for i in devisors:
        print("    pol/", i)
    pol = Polinom([1], pol.field)
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
    #test()
    #devisor = Devisor(2)
    #find_result(Polinom([1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1], 2))
    print(find_undivisable(5, 4))
