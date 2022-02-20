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
        """"
        if test_data is not float:
            test_data = test_data.astype(np.float)

        longitud = len(test_data)
        tamany = np.size(test_data)
        divisio = tamany/longitud
        conversioEnters = np.int64(divisio)  # passem el resultat a enters de 64 bytes
        resultat = np.reshape(test_data, (len(test_data), conversioEnters))
        test_data = resultat

        distancia = cdist(test_data,self.train_data)

        self.neighbors

        self.neighbors = np.random.randint(k, size=[test_data.shape[0],k])

        """
        primera = False
        if isinstance(test_data, float) is False:
            test_data = test_data.astype(np.float)
        test_data = np.reshape(test_data, (len(test_data), np.int64(np.divide(np.size(test_data), len(test_data)))))
        distancias = cdist(test_data, self.train_data)
        self.neighbors = self.labels[np.argsort(cdist(test_data, self.train_data))[0:len(test_data), 0:k]]
        if primera is False:
            primera = True



    """
    Get the class by maximum voting
    :return: 2 numpy array of Nx1 elements.
            1st array For each of the rows in self.neighbors gets the most voted value
                        (i.e. the class at which that row belongs)
            2nd array For each of the rows in self.neighbors gets the % of votes for the winning class
    """
    def get_class(self):
        
        llista = []

        for i in self.neighbors:
            diccionari = {}
            longitud = len(i)
            for a in range(longitud):
                element = i[a]
                if element in diccionari:
                    diccionari[element] = diccionari[element] +1
                else:
                    diccionari[element] = 1
            clau = diccionari.get
            maxim = max(diccionari, key=clau)
            llista.append(maxim)
        llista = np.array(llista)

        return llista
        """
        output = {}
        lista = []
        # lista_percent = []
        for prenda in self.neighbors:
            # len_prenda = len(prenda)
            for i in range(len(prenda)):
                if prenda[i] not in output:
                    output[prenda[i]] = 1
                else:
                    output[prenda[i]] += 1
            # insert = max(output, key=output.get)
            lista.append(max(output, key=output.get))
            # lista_percent.append((output.get(insert) / len(prenda))*100)
            output = {}
        return np.array(lista)  # ,np.array(lista_percent)
        """

    """
    predicts the class at which each element in test_data belongs to
    :param test_data: array that has to be shaped to a NxD matrix ( N points in a D dimensional space)
    :param k:         :param k:  the number of neighbors to look at
    :return: the output form get_class (2 Nx1 vector, 1st the classm 2nd the  % of votes it got
    """
    def predict(self, test_data, k):
        self.get_k_neighbours(test_data, k)
        return self.get_class()



