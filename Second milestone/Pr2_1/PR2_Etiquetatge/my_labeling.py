__authors__ = ['1568204', '1569298', '1569115']
__group__ = 'DL.12'

import numpy as np
import Kmeans as km
import KNN 
from utils_data import read_dataset, visualize_k_means, visualize_retrieval
import matplotlib.pyplot as plt
#import cv2
import time


def Retrieval_by_color(llistaImatges, etiquetes, colors):
    llista=[]
    aux = 0
    for a in etiquetes: #recorrem totes les etiquetes
        for b in a:     #recorrem cada element de l'etiqueta
            if(b in colors): #si l'element de l'etiqueta correspon amb el color desitjat entrem a l'if
                llista.append(llistaImatges[aux]) #afegim l'element corresponent a una llista auxiliar
        aux = aux + 1   #augmentem el comptador
    
    return llista


def Kmeans_statistics(llistaImatges, kmeans, Kmax):
    K = 2           #inici de K=2
    i = Kmax-K      #calculem el numero de iteracions màximes
    llista = []
    llistaIteracions = []

    while (K != Kmax): #loop mentre el numero de iteracions no sigui el màxim
        tInicial = time.time() #temps inicial de la iteració
        kmeans[K].fit()
        wcd = kmeans[K].whitinClassDistance() #amb aquesta comanda i l'anterior calculem la distància
        tFinal = time.time() #temps final de la iteració
        Temps = tFinal - tInicial #temps total
        llista.append(Temps)
        llistaIteracions.append(K)
        K = K + 1  # augmentem K, ==> una iteració menys a fer

    plt.plot(llistaIteracions, llista) #afegim les dues llistes a la gràfica
    plt.ylabel('Temps(s)') #indiquem les dades de l'eix Y
    plt.xlabel('Iteracions') #indiquem les dades de l'eix X
    plt.show() #mostrem la gràfica


if __name__ == '__main__':

    #Load all the images and GT
    train_imgs, train_class_labels, train_color_labels, \
    test_imgs, test_class_labels, test_color_labels = read_dataset(ROOT_FOLDER='./images/', gt_json='./images/gt.json')

    #List with all the existant classes
    
    #Retrieval_by_color
    classes = list(set(list(train_class_labels) + list(test_class_labels)))
    a = Retrieval_by_color(test_imgs, test_color_labels, ["Red"])
    visualize_retrieval(a,len(a))
    print(len(test_imgs),len(a))
    
    #Kmeans_statistics
    kmeans = []
    for i in test_imgs[:20]:
        kmeans.append(km.KMeans(i))    
    Kmeans_statistics(test_imgs[:10],kmeans,5)
    
    #Diferents heurístiques per BestK
    llistaaux=[]
    for img in test_imgs[:5]:
        kms = km.KMeans(img)
        kms.fit()
        llistaaux.append(kms.whitinClassDistance())
    print(llistaaux)

    #find_bestK
    llista=[]
    for imagen_aux in range(5):
        x = km.KMeans(test_imgs[imagen_aux]) #inicialitzem l'objecte kmeans
        x.fit()
        x.find_bestK(8) #cridema a la funció
        llista.append(x.K) #afegim resultat
    print(llista)    
        
## You can start coding your functions here









