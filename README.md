# genetic_solver
Genetic algorithms exploration, not for serious use.

The Animal class has a vector of genes, each gene is a floating point number.  The genes 
can be anything, really.  The (vx,vy) components of velocity, fluid density, temperature, 
pressure, whatever the current problem requires.  It is up to the user to assign meaning.

Fitness functions are problem dependent, specified by the user.  In this function, the
genes of each Animal are tested against whatever objectives the user has defined for
the problem.

The Pool class is a collection of Animals. Pools take a fitness function, and
can evaluate fitness, breed more Animals (according to rules) and cull the
population back down to a desired number to provide the next generation.
