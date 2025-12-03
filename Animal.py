# genetic algorithm to find a function that solves an algebraic eqn

import numpy as np
import random as rnd
import sys

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

