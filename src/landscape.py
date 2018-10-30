'''
@author: Nono Saha Cyrille Merleau 
@email: csaha@aims.edu.gh 

This program is an implementation of a Simple Genetic Algorithm to maximize a given landscape function. 

The landscape function is given by: 

                        f(x_1,...,x_N) = x_1*w_1 + x_2*w_2 + ... + x_N*w_N
        Where x_i is 0 or 1 and w_i is a random number between [r_i,1] with r_i = K/N

'''


#Importing the libraries 
import numpy as np 
import sympy as sp
import random


#Landscape function
''' This function generates one landscape function for a given parameters: 
        INPUT
        =====
                N(Type: int) : it is the number genes that constitutes the genotype
                K(Type: int) : it controls the number of connections between the gene i and the others N-1 
                s(Type: int): it is the seed
        OUTPUT
        ======
                The function returns a symbolic function f(x_1,...,x_N)
'''
def F(N, K, s) :
    #initialize tha value of f to 0
    f = 0
    random.seed(s)
    #compute the ruggedness coefficient 
    r = float(K)/N
    for i in range(N) : 
       w = uniform(r,1) 
       x = sp.var("x"+str(i+1)) # create a symbolic variable x_1, ..., x_N
       f += w*x
    return f


#Definition of the genotype class 
''' This class defines the structure of genotype: 
        Attributes
        ==========
                id(string): it is a binary sequence of lenght N. (x_i,...,x_N)
                fitness(float): it is the corresponding value of the landscape function of a genotype (x_i,...,x_N).
'''
class Genotype : 

    def __init__(self, id, fitness) : 
        self.id = id 
        self.fitness = fitness 




#Definition of necessary functions 

'''
    This method generates a random uniform number between [a,b]
        INPUT
        =====
                a(Type: float) : lower bound
                b(Type: float) : upper bound
        ======
                Type(float) : The function returns a random float between a and b
'''
def uniform(a,b) : 
        return (b-a)*random.random() + a 


'''
This method compute the fitness landscape of a given binary sequence of genotype (x_i,...,x_N)
        INPUT
        =====
                f(Type: symbolic addition) : it is the symbolic landscape function.
                genotype(Type: string) : a sequence of bit of lenth N. 
        OUTPUT
        ======
                The function returns a float
'''
def fitness(f,genotype) : 
    gen = map(int, genotype)
    g = lambda x1,x2,x3,x4,x5,x6,x7,x8,x9,x10 : eval(str(f))# convert the symbolic landscape to a numerical function of 10 variables
    
    return g(gen[0],gen[1],gen[2],gen[3],gen[4],gen[5],gen[6],gen[7],gen[8],gen[9])/len(genotype)


'''
    This method is used to mutate a given genotype to form a new offspring. 
        For a given number of bit n to mutate, we select randomly n-bits and for each bit selected replace it by a random selected bit. 
        INPUT
        =====
                genotype(Type: string) : a sequence of bit of lenth N.
                number_of_bit(Type: int): the default value is 1. It is the number bit to mutate
        OUTPUT
        ======
                The function returns a new offspring
'''
def mutate(genotype, number_of_bit=1) : 
    vect_gen = map(int, genotype)
    for i in random.sample(range(0,len(genotype)),number_of_bit) :
        if vect_gen[i] == 1 : 
            vect_gen[i] = 0
        else: 
            vect_gen[i] = 1
    return vect_gen


'''
    This method is used to cross two given genotypes to form two new offspring for the next generation.
    
    For two given sequences of bit, the crossover consists of selecting n-bit in genotype1 and n-bit in genotype2 
    and exchange them to form two new genotype. 

        INPUT
        =====
                genotype1(Type: string) : a sequence of bit of lenth N. that represent a parent
                genotype2(Type: string) : a sequence of bit of lenth N. that represent a donor
                number_of_bit(Type: int): the default value is 1. It is the number bit to cross(to exchange)
        OUTPUT
        ======
                The function returns two new offsprings.
'''
def crossover(genotype1, genotype2, number_of_bit=1) : 
    vect1 = map(int, genotype1)
    vect2 = map(int, genotype2)
    swap = 0 
    male = random.sample(range(0,len(genotype1)),number_of_bit)
    female = random.sample(range(0,len(genotype2)),number_of_bit)
    for i in range(number_of_bit):
        swap = vect1[male[i]]
        vect1[male[i]] = vect2[female[i]] 
        vect2[female[i]]  = swap
    return vect1, vect2    


'''
    This method is used to select a fittest individual among the population for the given tournament_size.
    
    Based on the tournament_size some genotype are selected among the population and amont the selected genotypes the fittest one will be selected.


        INPUT
        =====
                population(Type: list of genotype) : the current population of genotype.
                tournament_size(Type: int): the default value is 10. It is the number individual to select randomly.
        OUTPUT
        ======
                The function returns one fittest genotype.
'''
def selection(population,tournament_size=10) :
    selected = random.sample(population,tournament_size)
    fitest = selected[0]

    for gen in selected : 
        if gen.fitness > fitest.fitness : 
            fitest = gen
    return fitest


#Generate the initial population of size N 
'''
    This method is used to genrate a N-random genetypes as an initial population.
        INPUT
        =====
                evalution_function(Type: sympy add function) : It is a landscape function to maximize use as a fitness function.
                population_size(Type: int) : the initial number of genotype to generate.
                init_depth(Type: int): the default value is 10. It is the number of genes that contains each genotype.
        OUTPUT
        ======
                The function returns a list of genotypes.
'''
def initialize(evalution_funtion, population_size, init_depth=10) : 
    n = 0 
    population = []
    for i in xrange(2**init_depth):
        genotype = bin(i)[2:].zfill(init_depth)
        population.append(Genotype(genotype,fitness(evalution_funtion,genotype)))

    return random.sample(population,population_size)  

'''
 This function is implementing the simple genetic algorithm
        INPUT
        =====
                population_size(Type: int) : the number of genotypes to generate.
                number_of_generation(Type: int) : the number of generation .
                tournament_size(Type: int) : the initial number of genotype to generate.
                crossing_rate(Type: float between [0,1]) : the rate of crossover operation.
                mut_rate(Type: float between [0,1]): the rate of mutation operation.
        OUTPUT
        ======
                The function returns a list of fittest genotypes.
'''
def mySimplega(f, population_size, number_of_generation, tournament_size, crossing_rate, mut_rate) : 
   

    prev_population = initialize(f,population_size) #Initialize the population of genotype
    fitest = prev_population[0] #set tha first individual as the fittest one.
    print fitest.id, fitest.fitness
    while number_of_generation > 0 : 
        print 'Generation ', number_of_generation
        #Compute the number of genotype that comes from mutation process and that will be involved in the next generation
        number_mut = int(population_size*mut_rate) 
        #Compute the number of genotype that comes from crossover process and that will be involved in the next generation
        number_cross = int(population_size*crossing_rate)
        newgeneration = []

        while number_cross>0 : 
            parent1 = selection(prev_population) 
            parent2 = selection(prev_population)
            
            child1, child2 = crossover(parent1.id,parent1.id, 2)
            newgeneration.append(Genotype(child1, fitness(f,child1)))
            newgeneration.append(Genotype(child2, fitness(f,child2)))

            number_cross -=2
            
        while number_mut > 0 :
            indiv = selection(prev_population)
            new_indiv = mutate(indiv.id, 1)
            newgeneration.append(Genotype(new_indiv,fitness(f,new_indiv)))
            number_mut -=1

        prev_population = np.copy(newgeneration)

        for gen in prev_population: 
            if gen.fitness > fitest.fitness : 
                fitest = gen

        print fitest.id, fitest.fitness
        number_of_generation -=1
    return fitest

#Definition of the main function
def main() : 
    
    N = 10
    K = 5
    s = 2001
    TOURNAMENT_SIZE = 3
    MUTATION_RATE = 0.9
    CROSSOVER_RATE = 0.1
    NUMBER_OF_GENERATION = 5
    POPULATION_SIZE = 50
    
    #We generate 10 landscape functions and optimize them for N = 10 and K = 4
    for i in range(10) : 
        f = F(N,K,i)
        print "landscape Function ", i
        fittest = mySimplega(f,POPULATION_SIZE,NUMBER_OF_GENERATION, TOURNAMENT_SIZE, CROSSOVER_RATE, MUTATION_RATE)
        print "Fittest genotype = ", fittest.id, "  landscape value = ", fittest.fitness
    
    #Fixing N and varying K from 1 to N-1 
    while K < N : 
        f = F(N,K,s)
        best_mut_rate = 0
        best_crossover_rate = 1 
        best_geno = mySimplega(f,POPULATION_SIZE,NUMBER_OF_GENERATION, TOURNAMENT_SIZE, best_crossover_rate, best_mut_rate )
        for mut_rate in np.arange(0.1,1,0.1) : 
            crossover_rate = 1 - mut_rate 
            fittest = mySimplega(f,POPULATION_SIZE,NUMBER_OF_GENERATION, TOURNAMENT_SIZE, crossover_rate, mut_rate )
            if best_geno.fitness < fittest.fitness : 
                best_geno = fittest 
                best_crossover_rate = crossover_rate
                best_mut_rate = mut_rate 
        print "The value of K is ", K
        print "Best mut rate = ", best_mut_rate, "Best crossover rate = ", best_crossover_rate
        s +=1
        K = K+1 

if __name__ == "__main__" : 
    main()