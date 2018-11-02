import Landscape 
import Evolution 


import numpy 
import matplotlib.pyplot as plt 




def main () : 

    population_size = 100

    N = 10
    k = 4

    number_of_generation = 100 
    mut_prob = 1./N

    seed = 1000 

    landscape = Landscape.Landscape(N,k,seed) 

    evolution = Evolution.Evolution(landscape,population_size, N) 

    history  = evolution.run(number_of_generation,mut_prob)
    means = [ ]
    for gen in history : 
        values = [genotype.fitness for genotype in gen]
        means.append(numpy.max(values))

    plt.plot(means)

    plt.show()


if __name__ == "__main__"  : 

    main()