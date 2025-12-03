# genetic algorithm to find a function that solves an algebraic eqn

import numpy as np
from Animal import Animal
from Pool import Pool
from Plot import plot

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

    pool.run(maxIters = 100, tol = 1.0)

    plot(pool)


        
