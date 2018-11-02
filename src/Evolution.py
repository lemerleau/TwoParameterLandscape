

import numpy
import random
import Genotype


class Evolution : 



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
    def __init__(self, landscape, population_size, init_depth=10) : 
        
        self.population_size = population_size 
        self.init_depth = init_depth 
        self.landscape = landscape
        n = 0 
        population = []
        for i in xrange(2**init_depth):
            genotype_id = bin(i)[2:].zfill(init_depth)
            population.append(Genotype.Genotype(genotype_id,landscape.fitness(genotype_id)))

        self.init_pop = numpy.random.choice(population,population_size,replace=False)  



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
    def mutate(self,genotype, mut_prob) : 
        
        list_gene = []
        for i in range(len(genotype.id)): 
            r = numpy.random.uniform(0,1)
            if r < mut_prob : 
                selct = numpy.random.choice([0,1],size=1)
                list_gene.append(str(selct[0]))
            else : 
                list_gene.append(genotype.id[i])
        new_genotype = Genotype.Genotype("".join(list_gene), self.landscape.fitness("".join(list_gene)) )

        return new_genotype

    def mutateAll(self,population, mut_prob) : 
        
        new_pop = []
        for genotype in population : 
            new_pop.append(self.mutate(genotype,mut_prob))

        return new_pop 


    def reproduce(self,population, size) : 

        list_fitness = [ ]
        for genotype in population : 
            list_fitness.append(genotype.fitness) 
        list_fitness = sorted(list_fitness,reverse=True)


        sorted_genotypes = []

        for fitness in list_fitness : 
            for genotype in population : 
                if genotype.fitness == fitness : 
                    sorted_genotypes.append(genotype)

        
        return sorted_genotypes[:size]
        

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
    def tournament_selection(self, population,tournament_size=10) :
        
        selected = random.sample(population,tournament_size)
        fitest = selected[0]

        for gen in selected : 
            if gen.fitness > fitest.fitness : 
                fitest = gen
        return fitest

    # Natural selection based on fitness proportionate method
    def fitness_proportion_selection(self,population,size) : 

        sum_fitness = 0 
        for genotype in population : 
            sum_fitness += genotype.fitness 

        proportion_prob = []
        for genotype in population : 
            proportion_prob.append(genotype.fitness/sum_fitness)
        
        choices = numpy.random.choice(population,size=size,p=proportion_prob)
        return choices



    '''
    This function is implementing the simple genetic algorithm
            INPUT
            =====
                    number_of_generation(Type: int) : the number of generation .
                    mut_prob(Type: float between [0,1]): the rate of mutation operation.
            OUTPUT
            ======
                    The function returns a list of fittest genotypes.
    '''
    def run(self, number_of_generation, mut_prob) : 
    

        prev_population = self.init_pop #Initialize the population of genotype
        history = [ ]
        history.append(prev_population)
        i = 0 
        while i < number_of_generation : 
            print 'Generation ', i
            
            new_generation = self.reproduce(prev_population, int(self.population_size*0.1))
            print new_generation
            selected = self.fitness_proportion_selection (prev_population, int(self.population_size*0.9))
            new_generation = numpy.insert(new_generation,len(new_generation),self.mutateAll(selected, mut_prob) )
            history.append(new_generation)

            
            prev_population = numpy.copy(new_generation)

            i = i +1 

        return history
