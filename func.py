# genetic algorithm to find a function that solves an algebraic eqn

import numpy as np
import random as rnd
import sys
sys.path.append('../rachelHydro')
from kernels import cubicSplineKernel

#-------------------------------------------------------------------------------
class Animal:
    """Each animal has vector of floating point 'genes' that is N long, and each gene
    takes on a value between y0 and y1.
    """
    def __init__(self,N, y0=0.0, y1=1.0):
        self.y = np.array(N*[0.0])
        for i in range(len(self.y)):
            self.y[i] = y0 + rnd.random()*(y1-y0)

    def __repr__(self):
        return str(self.y)

    def breed(self, b):
        new = Animal(len(self.y))
        for i in range(len(new.y)):
            p = rnd.random()
            if p > .95:     # mutate wildly
                new.y[i] = self.y[i]*2.0*rnd.random()
            elif p > 0.80:  # jiggle a little
                new.y[i] = self.y[i]*(0.95 + 0.1*rnd.random())
            elif p > .40:  # get it from me
                new.y[i] = self.y[i]  
            else:          # get it from other parent
                new.y[i] = b.y[i]
        return new

#-------------------------------------------------------------------------------
class BoundedAnimal(Animal):
    """Animals where the first and last genes, i.e, the boundary points, never move"""
    def __init__(self, N, b0=0.0, b1=1.0, y0=0.0, y1=1.0):
        Animal.__init__(N,y0,y1)
        self.y0 = b0
        self.y1 = b1
        self.y[0] = self.y0
        self.y[-1] = self.y1

    def breed(self, b):
        Animal.breed(b)
        self.y[0] = y0
        self.y[-1] = y1
        
    

#-------------------------------------------------------------------------------
class Pool:
    def __init__(self, fit, N, M, y0, y1, Critter=Animal, sort=False,
                 printCycle=1):
        self.fitness = fit
        self.cycle = 0
        self.min_err = 9e99
        self.N = N
        self.breeders = []
        self.printCycle = printCycle
        for i in range(N):
            self.breeders.append(Critter(M, y0, y1))
        if sort:
            for b in self.breeders:
                b.y.sort()
        print( "initializing pool with %d breeders" % N)
#         for b in self.breeders:
#             print( b)
#         print( "-----------------")

    def step(self, n=1):
        for i in range(n):
            self.diagnose()
            self.repopulate()
            self.cycle += 1

    def diagnose(self):
        """print current state of the pool"""
        if self.cycle % self.printCycle == 0:
            print( "cycle %4d min_err=%g best=" % (self.cycle, self.min_err),  self.breeders[0])

    def evaluate(self):
        """compute fitness of each breeder, note lowest error"""
        minErr = 9e99
        self.error = []
        for b in self.breeders:
            err = self.fitness(b.y)
            self.error.append((err, b))
            if err < minErr:
                minErr = err
        self.min_err = minErr

    def repopulate(self):
        """evaluate population, cull worst 80% and replace with new breeders
        born from the top 20%"""
        
        self.evaluate()
        self.error.sort(key=lambda x: x[0])  # sort by err value
        self.breeders = [b for e,b in self.error]

        # fraction f are kept, (1-f) are replaced
        f = 0.2
        N = len(self.breeders)
        nKeep = int(f*N)
        nKill = int((1-f)*N)
        iNew = 0
        while iNew < nKill:
            imom = int(iNew % nKeep)
            ipop = int(rnd.random()*nKeep)
            mom = self.breeders[imom]
            pop = self.breeders[ipop]
            self.breeders[nKeep + iNew] = mom.breed(pop)
            iNew += 1

#-------------------------------------------------------------------------------
##########################

def run(pool, maxIters = 10, tol = 1.0):
    err = 9e99
    i = 0
    while err > tol and i < maxIters:
        pool.step()
        i += 1
        err = pool.min_err
    print( 'final min_err = ', pool.min_err, " best soln = ", pool.breeders[0])
            
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    # test 0, does anything work?
    # a = Animal(2)
    # print( a)

    #----------------------------------------------------------------
    # test 1, Pool, breeding, solving an example
    def fitFunc(y): # looking for y = i**2
        return sum([abs(y[i] - i*i) for i in range(len(y))])

    # Pool takes a fitness function, number of animals N, data length
    # for the animals M, then each gene lies between two numbers y0,
    # y1, and the animal type is the Critter, =Animal.  The 'sort'
    # argument sort or not during initialization.
    pool  = Pool(fitFunc, 1000, 8, 0, 64 )

    run(pool, maxIters = 100, tol = 1.0)

    def plot(show=True):
        if show:
            from matplotlib import pyplot as plt
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
    # # test 2, SPH mass distribution
    # def density(x):
    #     return 1 + x

    # def code_rho(x):
    #     h = .02
    #     kernel = cubicSplineKernel(h, x)
    #     # rho_i = sum m W(xi, xj) over mass points
    #     m = 0.02
    #     N = len(x)
    #     rho = np.array(N*[0.0])
    #     for i in range(N):
    #         rho[i] = 0.0
    #         for j in range(N):
    #             rho[i] += m*kernel.W(i,j)
    #     return rho
        
    # def fitness(x):
    #     error = sum(abs(code_rho(x)[:-1] - density(x)[:-1]))/len(x)
    #     return error
        
    # # Pool takes a fitness function, number of animals N, data length
    # # for the animals M, then each gene lies between two numbers y0,
    # # y1, and the animal type is the Critter, =Animal.  The 'sort'
    # # argument sort or not during initialization.
    # pool  = Pool(fitness, 200, 10, 0, .05 , Critter=Animal, sort=True, printCycle=10)

    # run(pool, maxIters = 100, tol = 5e-4)
    #----------------------------------------------------------------

    # def plot(show=True):
    #     if show:
    #         from matplotlib import pyplot as plt
    #         x = pool.breeders[0].y
    #         d = density(x)
    #         rho = code_rho(x)
    #         c = plt.plot(x,d)
    #         plt.setp(c, marker='s', markersize=20, linestyle=' ',
    #                  color='blue',label='analytic 1+x')
    #         c = plt.plot(x,rho)
    #         plt.setp(c, marker='.', markersize=20, linestyle=' ',
    #                  color='red', label='code_rho')
    #         plt.show()

    plot()


        
