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
        def __init__ ( self, N, k, s) :
                self.N = N 
                self.k = k
                self.seed = s 

                if k > N : 
                        print "k should be greter than N. Please check your entries."
                        return 
                np.random.seed(s)
                self.w = np.random.random((N,2**(k+1))) 
        

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
                print len(genotype), len(self.w)
                k = math.log(len(self.w[0]),2) - 1 
                k = int(k)
                
                w = []
                for i in range(len(genotype)) : 
                        l = [x for x in range(len(genotype)) if x != i]
                        print l
                        choice = np.random.choice(l,k, replace=False)
                        choice = np.insert(choice,0,i)
                        print choice
                        b = "".join([genotype[ch] for ch in choice])
                        print int(b,2) 
                        print b 
                        w.append(self.w[i,int(b,2)])
                return sum(w)/len(w)    



