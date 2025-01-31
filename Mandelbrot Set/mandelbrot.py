import matplotlib.pyplot as plt
import numpy as np

class Mandelbrot:
    def __init__(self, C):
        self.C = C #an array

    def recurse(self):
        Ns = []
        for row in self.C:
            for i in row:
                z_n = 0
                n = 0
                while np.abs(z_n) < 2 and n < 255: 
                    z_n = (z_n)**2 + i
                    n += 1
                Ns.append(n) #assigns colour to C
        Ns = np.array(Ns).reshape(self.C.shape)
        return Ns
    
    def run(self, Ns):      
        plt.imshow(Ns)
        plt.show()

if __name__ == "__main__":
    x = np.linspace(-2.025, 0.6, 512)
    y = np.linspace(-1.125, 1.125, 512)
    xv, yv = np.meshgrid(x, y) #generating
    C = xv + 1j*yv
    thing = Mandelbrot(C)
    cols = thing.recurse()
    thing.run(cols)


    


