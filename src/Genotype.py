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

