

import numpy
import random
import Genotype
import Archive


class Evolution : 


##################
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
    def __init__(self, landscape, population_size, lamda , k, archiving, init_depth=10) : 
        
        self.population_size = population_size 
        self.init_depth = init_depth 
        self.landscape = landscape
        self.lamda = lamda
        self.k = k 
        n = 0 
        population = []
        for i in xrange(2**init_depth):
            genotype_id = bin(i)[2:].zfill(init_depth)
            population.append(Genotype.Genotype(genotype_id,landscape.fitness(genotype_id)))

        self.init_pop = numpy.random.choice(population,population_size,replace=False)  
        self.archiving = archiving 


##################
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

##################
    def mutateAll(self,population, mut_prob) : 
        
        new_pop = []
        for genotype in population : 
            new_pop.append(self.mutate(genotype,mut_prob))

        return new_pop 

###################

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
        
##################
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

##################
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

##################
    # Natural selection based on fitness proportionate and novelty proportion 
    def novelty_selection(self,population,size, lamda, k) : 

        sum_fitness = 0 
        sum_novelty = 0
        saved_novelty = [] 

        for genotype in population : 
            sum_fitness += genotype.fitness 
            n = self.landscape.novelty(genotype, population,k)
            sum_novelty += n 
            saved_novelty.append(n)
        self.archiving.archive(population, saved_novelty)
        proportion_prob = []
        for i in range(len(population)) : 
            proportion_prob.append((1-lamda)*(population[i].fitness/sum_fitness) + lamda*(saved_novelty[i]/sum_novelty))
        
        choices = numpy.random.choice(population,size=size,p=proportion_prob)
        return choices


##################
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
    def crossover(self, genotype1, genotype2, number_of_bit=1) : 
        vect1 = map(str, genotype1.id)
        vect2 = map(str, genotype2.id)

        r = numpy.random.randint(0, len(vect1))
        swap = vect1[: r]
        vect1[:r] = vect2[:r]
        vect2[:r] = swap 

        return  Genotype.Genotype("".join(vect1), self.landscape.fitness("".join(vect1))), Genotype.Genotype("".join(vect2), self.landscape.fitness("".join(vect2))) 

#####################

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
            
            selected = self.novelty_selection (numpy.insert(prev_population,len(prev_population),self.archiving.archiving), int(self.population_size*0.9),self.lamda, self.k)

            new_generation = numpy.insert(new_generation,len(new_generation),self.mutateAll(selected, mut_prob) )
            history.append(new_generation)

            
            prev_population = numpy.copy(new_generation)

            i = i +1 

        return history
