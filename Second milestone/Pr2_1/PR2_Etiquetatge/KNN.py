__authors__ = ['1568204', '1569298', '1569115']
__group__ = 'DL.12'

import numpy as np
import math
import operator
from scipy.spatial.distance import cdist

class KNN:
    def __init__(self, train_data, labels):

        self._init_train(train_data)
        self.labels = np.array(labels)
        #############################################################
        ##  THIS FUNCTION CAN BE MODIFIED FROM THIS POINT, if needed
        #############################################################

        """
        initializes the train data
        :param train_data: PxMxNx3 matrix corresponding to P color images
        :return: assigns the train set to the matrix self.train_data shaped as PxD (P points in a D dimensional space)
        """
    def _init_train(self,train_data):
        
        if train_data is not float:
            self.train_data = train_data.astype(np.float)

        longitud = len(train_data)
        tamany = np.size(self.train_data)
        divisio = tamany/longitud
        conversioEnters = np.int64(divisio) #passem el resultat a enters de 64 bytes
        resultat= np.reshape(self.train_data, (len(train_data), conversioEnters))
        self.train_data = resultat
  
        """
        given a test_data matrix calculates de k nearest neighbours at each point (row) of test_data on self.neighbors
        :param test_data:   array that has to be shaped to a NxD matrix ( N points in a D dimensional space)
        :param k:  the number of neighbors to look at
        :return: the matrix self.neighbors is created (NxK)
                 the ij-th entry is the j-th nearest train point to the i-th test point
        """
    def get_k_neighbours(self, test_data, k):
                
        if test_data is not float:
            test_data = test_data.astype(np.float)

        longitud = len(test_data)
        tamany = np.size(test_data)
        divisio = tamany/longitud
        conversioEnters = np.int64(divisio)  # passem el resultat a enters de 64 bytes
        resultat = np.reshape(test_data, (longitud, conversioEnters))
        test_data = resultat

        distancies = cdist(test_data,self.train_data)
        indexs = np.argsort(distancies)
        self.neighbors = self.labels[indexs[0:longitud, 0:k]]
        
    """
    Get the class by maximum voting
    :return: 2 numpy array of Nx1 elements.
            1st array For each of the rows in self.neighbors gets the most voted value
                        (i.e. the class at which that row belongs)
            2nd array For each of the rows in self.neighbors gets the % of votes for the winning class
    """
    def get_class(self):
       
        llista = []
        longitud = len(self.neighbors)
        for i in range(longitud):
            diccionari = {}
            for x in self.neighbors[i]:
                if x not in diccionari:
                    diccionari[x] = 1
                else:
                    diccionari[x] = diccionari[x] + 1

            MAX=0
            aux=[]
            paraula=""
            for a in diccionari:
                if (diccionari[a] > MAX):
                    MAX = diccionari[a]
                    paraula = a
                elif(diccionari[a] == MAX):
                    aux.append(paraula)
                    aux.append(a)
                    aux.sort()
                    paraula=aux[0]
                    
            llista.append(paraula)                      
        return np.array(llista)

    """
    predicts the class at which each element in test_data belongs to
    :param test_data: array that has to be shaped to a NxD matrix ( N points in a D dimensional space)
    :param k:         :param k:  the number of neighbors to look at
    :return: the output form get_class (2 Nx1 vector, 1st the classm 2nd the  % of votes it got
    """
    def predict(self, test_data, k):
        
        self.get_k_neighbours(test_data, k)
        return self.get_class()



