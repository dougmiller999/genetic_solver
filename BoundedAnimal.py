from Animal import Animal

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
        
    

