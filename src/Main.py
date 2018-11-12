import Landscape
import Archive 
import Evolution


import numpy 
import matplotlib.pyplot as plt 




def main () : 

    population_size = 100

    N = 10
    k = 6
    p = 0.99

    lamda = [0,1,1]

    number_of_neighbors = 25

    number_of_generation = 100
    mut_prob = 1./N
 
    seed = 1000   
    

    landscape = Landscape.Landscape(N,k,seed,p) 
    evolution = Evolution.Evolution(landscape,population_size, 1, number_of_neighbors,Archive.Archive(10,""), N) 
    mth = ["None","N","R"]
    for i in range(3): 
        print " ====================================================================="
        archive =  Archive.Archive(10,mth[i]) 
        evolution.archiving = archive
        #evolution.lamda = lamda[i]
        
        history  = evolution.run(number_of_generation,mut_prob)
        maxs = [ ]
        for gen in history : 
            values = [genotype.fitness for genotype in gen]
            maxs.append(numpy.max(values))
        plt.plot(maxs, label=r"$method = $" +str(mth[i]))
        
    
    plt.xlabel("Generation")
    plt.ylabel("Max Fitness")

    plt.title("Novelty Vs Fitness")
    plt.legend(loc="lower right", shadow=True, fontsize='12')
    plt.show()
    

if __name__ == "__main__"  : 

    main()