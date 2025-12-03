from matplotlib import pyplot as plt
import numpy as np

def plot(pool, show=True):
    if show:
        y = pool.breeders[0].y # best breeder solution
        x = np.linspace(0,len(y)-1,len(y))
        
        anal = x**2
        c = plt.plot(x,anal)
        plt.setp(c, marker='s', markersize=20, linestyle=' ',
                 color='blue',label='analytic x**2')
        c = plt.plot(x,y)
        plt.setp(c, marker='.', markersize=20, linestyle=' ',
                 color='red', label='best solution')
        plt.show()
#----------------------------------------------------------------
