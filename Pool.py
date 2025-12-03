import random as rnd
from Animal import Animal

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

    def run(self, maxIters = 10, tol = 1.0):
        err = 9e99
        i = 0
        while err > tol and i < maxIters:
            self.step()
            i += 1
            err = self.min_err
        print( 'final min_err = ', self.min_err, " best soln = ", self.breeders[0])
            
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

