__authors__ = ['1568204', '1569298', '1569115']
__group__ = 'DL.12'

import numpy as np
import utils


class KMeans:

    def __init__(self, X, K=1, options=None):
        """
         Constructor of KMeans class
             Args:
                 K (int): Number of cluster
                 options (dict): dictºionary with options
            """
        self.num_iter = 0
        self.K = K
        self._init_X(X)
        self._init_options(options)  # DICT options

    #############################################################
    ##  THIS FUNCTION CAN BE MODIFIED FROM THIS POINT, if needed
    #############################################################

    def _init_X(self, X):
        """Initialization of all pixels, sets X as an array of data in vector form (PxD)
            Args:
                X (list or np.array): list(matrix) of all pixel values
                    if matrix has more than 2 dimensions, the dimensionality of the smaple space is the length of
                    the last dimension
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
        if X is not float:
            self.X = X.astype(np.float)
        dimensio = X.shape

        if dimensio[1] != 3:
            tamany = X.size
            files = np.divide(tamany, 3)
            filesINT = np.int64(files)
            self.X = X.reshape(filesINT, 3)

    def _init_options(self, options=None):
        """
        Initialization of options in case some fields are left undefined
        Args:
            options (dict): dictionary with options
        """
        if options == None:
            options = {}
        if not 'km_init' in options:
            options['km_init'] = 'first'
        if not 'verbose' in options:
            options['verbose'] = False
        if not 'tolerance' in options:
            options['tolerance'] = 0
        if not 'max_iter' in options:
            options['max_iter'] = np.inf
        if not 'fitting' in options:
            options['fitting'] = 'WCD'  # within class distance.

        # If your methods need any other prameter you can add it to the options dictionary
        self.options = options

        #############################################################
        ##  THIS FUNCTION CAN BE MODIFIED FROM THIS POINT, if needed
        #############################################################

    def _init_centroids(self):
        """
        Initialization of centroids
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
        tipus = self.options['km_init'].lower()

        self.old_centroids = np.empty([self.K, 3])
        self.centroids = np.empty([self.K, 3], np.float64)
        self.centroids[:] = np.nan

        x = 0 #comptador a 0, serà utilitzat en els 3 tipus
        if tipus == 'first':
            for i in self.X: #recorrem cada element
                comprobacio = np.equal(i, self.centroids).all(1) #comprovem que l'element iterat no pertanyi als centroids
                if not any(comprobacio): #si cap element hi pertany (retorna tot false)
                    self.centroids[x] = i #afegim el centroid i a la posició que determini el comptador
                    x = x + 1
                    if x == self.K: #si la x == k sortim del for
                        break

        elif tipus == 'random':
            np.random.seed()
            longitud = len(self.X) - 1 #-1 ja que recorrerà de 0 a n-1
            index = np.random.randint(low=0, high=longitud) #escull un valor random entre el rang 0 a longitud

            while self.K != x:
                comprobacio = np.equal(self.X[index], self.centroids).all(1) #comprovem que l'element random no pertanyi als centroids
                if not any(comprobacio): #si cap element hi pertany (retorna tot false)
                    self.centroids[x] = self.X[index] #afegim el centroid random d'X a la posició corresponent
                    x = x + 1

                np.random.seed() #tornem a calcular un valor aleatori
                longitud = len(self.X) - 1
                index = np.random.randint(low=0, high=longitud)


    def get_labels(self):
        """        Calculates the closest centroid of all points in X
        and assigns each point to the closest centroid
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
        dis = distance(self.X, self.centroids)
        self.labels = np.argmin(dis, 1)

    def get_centroids(self):
        """
        Calculates coordinates of centroids based on the coordinates of all the points assigned to the centroid
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################

        aux = (self.K, 3)
        self.old_centroids = np.array(self.centroids, copy=True)
        rgb = np.empty(aux, np.float64)
        PCentroid = np.bincount(self.labels)
        PCentroid = PCentroid.reshape(-1, 1)
        rgb = [(self.X[self.labels == i].sum(0)) for i in range(self.K)]
        self.centroids = np.divide(rgb, PCentroid)

        pass

    def converges(self):
        """
        Checks if there is a difference between current and old centroids
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################

        aux = np.allclose(self.old_centroids, self.centroids, self.options['tolerance'])
        return aux

    def fit(self):
        """
        Runs K-Means algorithm until it converges or until the number
        of iterations is smaller than the maximum number of iterations.
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################

        self._init_centroids()
        while (not self.converges()) and (self.num_iter < self.options['max_iter']):
            self.get_labels()
            self.get_centroids()
            self.num_iter = np.add(self.num_iter, 1)
        pass

    def whitinClassDistance(self):
        """
         returns the whithin class distance of the current clustering
        """

        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################

        dis = distance(self.X, self.centroids)
        mi = np.min(dis, axis=1)
        sq = np.square(mi)
        su = np.sum(sq)
        longitud = len(self.X)
        div = np.divide(1, longitud)
        resultat = np.multiply(div, su)
        return resultat
        """
        c = np.array([])
        for x in range(self.K):
            llista = np.where(self.labels == x) #seleccionem els valors que compleixin aquesta condició
            llista2 = self.X[llista[0]] #agafem el primer valor per a poder recorrer les X
            for y in llista2:
                valor = y - self.centroids[x]
                intra = np.matmul(valor, valor.T) #multiplicacio de les matrius
                inter = np.matmul(self.centroids[x], self.centroids[x].T) #multiplicacio de les matrius

                fischer = intra / inter
                c = np.append(c, fischer)

        sumaClusters = sum(c)
        total = sumaClusters / len(c)
        return (total)
        """




    def find_bestK(self, max_K):
        """
         sets the best k anlysing the results up to 'max_K' clusters
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
        self.K = 2
        self.fit()
        aux = self.whitinClassDistance()
        for x in range(3, max_K):
            self.K = x
            self.fit()
            aux2 = aux
            aux = self.whitinClassDistance()
            div = np.divide(aux, aux2)
            if ((1 - div) < 0.20):
                self.K = self.K - 1
                self.fit()
                break

        pass

    """
    Calculates the distance between each pixcel and each centroid
    Args:
        X (numpy array): PxD 1st set of data points (usually data points)
        C (numpy array): KxD 2nd set of data points (usually cluster centroids points)

    Returns:
        dist: PxK numpy array position ij is the distance between the
        i-th point of the first set an the j-th point of the second set
    """
def distance(X, C):


    #########################################################
    ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
    ##  AND CHANGE FOR YOUR OWN CODE
    #########################################################

    X0 = X[:, 0, np.newaxis]
    X1 = X[:, 1, np.newaxis]
    X2 = X[:, 2, np.newaxis]
    C0 = C[:, 0]
    C1 = C[:, 1]
    C2 = C[:, 2]
    sq0 = np.square(X0 - C0)
    sq1 = np.square(X1 - C1)
    sq2 = np.square(X2 - C2)
    add0 = np.add(sq0, sq1)
    add1 = np.add(add0, sq2)
    resultat = np.sqrt(add1)

    return resultat


def get_colors(centroids):
    """
    for each row of the numpy matrix 'centroids' returns the color laber folllowing the 11 basic colors as a LIST
    Args:
        centroids (numpy array): KxD 1st set of data points (usually centroind points)

    Returns:
        lables: list of K labels corresponding to one of the 11 basic colors
    """

    #########################################################
    ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
    ##  AND CHANGE FOR YOUR OWN CODE
    #########################################################

    l = len(centroids)
    PColors = utils.get_color_prob(centroids)
    etiquetes = np.empty(l, dtype=object)
    for x in range(l):
        ma = np.argmax(PColors[x])
        etiquetes[x] = utils.colors[ma]
    return etiquetes
