'''
@author: Nono Saha Cyrille Merleau 
@email: csaha@aims.edu.gh/ nonosaha@mis.mpg.de

This program is an implementation of a Simple Genetic Algorithm to maximize a given landscape function. 

The landscape function is given by: 

                        f(x_1,...,x_N) = 

'''


#Importing the libraries 
import numpy as np 
import random
import math
import pandas


class Landscape : 


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
        def __init__ ( self, N, k, s, p) :
                self.N = N 
                self.k = k
                self.seed = s 
                self.p = p
                self.w = []

                if k > N : 
                        print "k should be greter than N. Please check your entries."
                        return 
                np.random.seed(s)
                #self.w = np.random.random((N,2**(k+1))) 
                """
                for i in range(N) : 
                    for j in range(2**(k+1)) : 
                        r = random.uniform(0,1)
                        if r < self.p : 
                                self.w[i,j] = 0  
                dataFrame = pandas.DataFrame(self.w)
                dataFrame.to_csv("../logs/w"+str(s)+".csv")
                """
                dataFrame = pandas.read_csv("../logs/w1000.csv")
                for l in dataFrame.values : 
                        self.w.append(l[1:])

                self.w = np.array(self.w)


############################
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
        def fitness(self, genotype) : 

                k = math.log(len(self.w[0]),2) - 1 
                k = int(k)
                
                w = []
                
                position = range(len(genotype))

                for i in position : 
                        j = 1 
                        choice = []
                        while j <= k  : 
                                choice.append (position [(i+j)%len(position)])
                                j +=1  
                        choice = np.insert(choice,0,i)

                        b = "".join([genotype[ch] for ch in choice])
                        
                        w.append(self.w[i,int(b,2)])
        
                return sum(w)/len(w)    

###################


        def NKp_fitness(self, genotype) :
                r = np.random.uniform(0,1)
                if r < self.p : 
                        return 0 
                else : 
                        return self.fitness(genotype) 



###################

        def novelty_metric(self, genotype1, genotype2) : 
                
                return abs(int(genotype1.id,2) - int(genotype2.id,2))

        def novelty(self, genotype, population, k) : 
                list_novelty_metrics = []

                for ind in population : 
                        list_novelty_metrics.append(self.hamming_distance(genotype,ind))

                list_novelty_metrics = sorted(list_novelty_metrics) 

                return sum(list_novelty_metrics[:k])/float(k)

        
        def hamming_distance(self, genotype1, genotype2) :
                distance = 0
                b1 = genotype1.id 
                b2 = genotype2.id
                for i in range(len(b1)) : 
                        if b1[i] != b2[i] : 
                                distance +=1
                
                return distance