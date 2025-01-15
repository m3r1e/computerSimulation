
class Polynomial(): 
    def __init__(self, coefficients):
        self.coefficients = coefficients #initialise the coefficient list

    def order(self):
        order = 0 
        for i in range(len(self.coefficients)): 
            if self.coefficients[i] != 0: #find the last non-zero coefficient and set the order to its index
                order = i 
        return order 
    
    def add(self, p2):
        new_coeffs = [] #coefficients of the polynomial post-addition

        while len(self.coefficients) != len(p2.coefficients): #checking that they are the same length, and appending zeros to the shorter
            if len(self.coefficients) < len(p2.coefficients):
                self.coefficients.append(0)
            if len(self.coefficients) > len(p2.coefficients):
                p2.coefficients.append(0)
            

        for i in range(len(self.coefficients)):
            new_coeffs.append(self.coefficients[i] + p2.coefficients[i]) #adding the coefficients of the two polynomials

        return Polynomial(new_coeffs)

    
    def derivative(self):
        new_coeffs = [] 

        for i in range(len(self.coefficients)):
            new_coeffs.append(self.coefficients[i] * i) #multiplying the coefficient by the corresponding exponent

        return Polynomial(new_coeffs[1:]) #so that the powers in the string method are right
    
    def anti_derivative(self, c):
        new_coeffs = []
        powers = [i for i in range(1, len(self.coefficients) + 1)] #exponents where we already 'add one'

        for i in range(len(self.coefficients)):
            new_coeffs.append(self.coefficients[i] / powers[i]) #dividing the coefficient by the exponent (to which we already added one)

        new_coeffs.insert(0,c)

        return Polynomial(new_coeffs)
        
    
    def __str__(self):
        new_polly = []

        for i in range(len(self.coefficients)):
            if self.coefficients[i] != 0: #only include if the coefficient is not zero
                new_polly.append(f"{self.coefficients[i]}x^{i} +") 

        temp = ' '.join(new_polly) #changing the polynomial from a list to a string (but there is still a '+' on the end here)      
        temp = temp.replace('x^0','') #if 'x^0' is included, we just remove it 
        temp = temp.replace('+ -', '- ') #changing any instances of '+ -' to just '-'
        return temp[:-1] #remove the '+' at the end
        
def main():
    p_a = Polynomial([2, 0, 4, -1, 0, 6])
    p_b = Polynomial([-1, -3, 0, 4.5])
    dp_a = p_a.derivative()
    print(dp_a)
    print(p_a.order())
    print(dp_a.anti_derivative(2)) 
    print(p_a.add(p_b))

if __name__ == "__main__":
    main()

