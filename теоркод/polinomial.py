import numpy as np

def devide_in_field(devider: int, devidend: int, field: int):
    for i in range(0, field):
        if (i * devider) % field == devidend:
            return i

class Polinom:
    def __init__(self, coefficients: np.array, field: int):
        coefficients = np.int16(np.mod(coefficients, field))
        for i in range(len(coefficients)-1, 0, -1):
            if coefficients[i] == 0:
                coefficients = np.delete(coefficients, i)
            else:
                break
        self.coefficients = np.mod(coefficients, field)
        self.field = field
        self.degree = len(coefficients) - 1
        
    def make_xn_polinom(deg, coef, field):
        xn_coefs = np.zeros(deg + 1)
        xn_coefs[deg] = coef
        return Polinom(xn_coefs, field)
    
    def copy(self):
        return Polinom(self.coefficients, self.field)
    
    def __eq__(self, other) -> bool:
        if type(other) == int:
            if self.degree != 0:
                return False
            if self.coefficients[0] != other:
                return False
            return True
        if self.degree != other.degree:
            return False
        for i in range(self.degree + 1):
            if self.coefficients[i] != other.coefficients[i]:
                return False
        return True
    
    def __str__(self) -> str:
        return str(self.coefficients)
        
    def __main_coef__(self):
        return self.coefficients[self.degree]
    
    def __print__(self):
        print(self.coefficients)
        
    def __add__(self, other):
        max_deg = max(self.degree, other.degree)
        self_coef = np.zeros(max_deg + 1)
        other_coef = np.zeros(max_deg + 1)
        for i in range(self.degree + 1):
            self_coef[i] = self.coefficients[i]
        for i in range(other.degree + 1):
            other_coef[i] = other.coefficients[i]
        self_coef = np.mod(self_coef + other_coef, self.field)
        return Polinom(self_coef, self.field)
    
    def __mul__(self, other):
        if type(other) == int:
            return Polinom(np.mod(self.coefficients * other, self.field), self.field)
        coefficients = np.zeros(self.degree + other.degree + 1)
        for i in range(self.degree + 1):
            for j in range(other.degree + 1):
                coefficients[i + j] = np.mod(coefficients[i + j] + self.coefficients[i] * other.coefficients[j], self.field)
        return Polinom(coefficients, self.field)
    
    def __sub__(self, other):
        return self + other * -1
    
    def __moditer__(self, devider, devidend):
        deg = devidend.degree - devider.degree
        if deg < 0:
            return devidend
        else:
            a_deg = devide_in_field(devider.__main_coef__(), devidend.__main_coef__(), self.field)
            xn = Polinom.make_xn_polinom(deg, a_deg, self.field)
            return self.__moditer__(devider, devidend - devider * xn)
    
    def __mod__(self, other):
        devidend = self.copy()
        return self.__moditer__(other, devidend)
    
    def __deviter__(self, devider, devidend, res):
        deg = devidend.degree - devider.degree
        if deg < 0:
            return res
        else:
            a_deg = devide_in_field(devider.__main_coef__(), devidend.__main_coef__(), self.field)
            xn = Polinom.make_xn_polinom(deg, a_deg, self.field)
            return self.__deviter__(devider, devidend - devider * xn, res + xn)
    
    def __truediv__(self, other):
        res = Polinom(np.zeros(1), self.field)
        devidend = self.copy()
        return self.__deviter__(other, devidend, res)
    
def test():
    p1 = Polinom(np.array([1, 2, 3, 0, 0]), 5)
    p2 = Polinom(np.array([3, 4, 3, 0]), 5)
    print("p1:", p1, "p2:", p2)
    p3 = p1 + p2
    print("p3=p1+p2:", p3)
    p4 = p1 * p2
    print("p4=p1*p2:", p4)
    p5 = p1 - p2
    print("p5=p1-p2:", p5)
    p6 = Polinom.make_xn_polinom(10, 2, 5)
    print("p6=2x^10:", p6)
    p7 = p6 % p1
    print("p7=p6%p1:", p7)
    p8 = (p6-p7) % p1
    print("p8=(p6-p7)%p1:", p8)
    p9 = p6 / p1
    print("p9=p6/p1:", p9)
    p10 = p9 * p1
    print("p10=p9*p1:", p10)
    print("p10==p1:", p10 == p1)
    print("p5==p7:", p5 == p7)
    print("p8==0:", p8 == 0)

if __name__ == "__main__":
    test()