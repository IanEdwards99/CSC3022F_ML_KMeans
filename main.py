#Author: Ian Edwards EDWIAN004
#CSC3022F ML Assignment 1
#Date: 21/05/2021
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import copy
style.use('ggplot')

data = {1:[2,10], 2:[2,5], 3:[8,4], 4:[5,8], 5:[7,5], 6:[6,4], 7:[1,2], 8:[4,9]} #Number examples from 1 to 8.

class KMeans:
    def __init__(self, k=3, tol = 0.001, iterations = 10):
        self.k = k
        self.iterations = iterations
        self.tol = tol


    def getDistance(self, pair1, pair2): #Calculate distance between two points. Could have used math.dist() or numpy.linalg.norm()
        return math.sqrt((pair1[0]-pair2[0])**2 + (pair1[1]-pair2[1])**2)

    def writeToFile(self, iteration, clusters, centroids): #Function to handle file writing.
        f = open("K-means.txt", "a")
        f.write("Iteration " + str(iteration)+"\n\n")
        for i in clusters: #loop through and get a single cluster at a time
            output = "Cluster " + str(i) + ": "
            for j in range(0, len(clusters[i])):  #loop through single cluster, feature by feature
                feature = clusters[i][j] #Get the feature, but example number must be printed out...
                key_list = list(data.keys()) #generate a list from the keys of the dictionary.
                val_list = list(data.values()) #generate a list form the values of the dictionary
                pos = val_list.index(feature) #get the position in the list of the pair/feature found.
                key = key_list[pos] #Get the example number of the feature found.
                if j == len(clusters[i])-1:
                    output = output + str(key)
                else: output = output + str(key) + ", "
            
            f.write(output+"\n")
            f.write("Centroid: (" + str(round(centroids[i][0], 2)) + ", " + str(round(centroids[i][1],2)) + ")"+"\n\n")
            output = ""

        f.close()

    def drawScatter(self): #function to plot data. Only works for specific case of k=3.
        iterations, clusters, centroids = self.fit()
        mydata = []
        for i in clusters:
            mydata.append(np.array(clusters[i]))
        x,y = mydata[0].T
        plot1 = plt.figure(1)
        plt.scatter(x,y, c='b')
        x,y = mydata[1].T
        plt.scatter(x,y, c='r')
        x,y = mydata[2].T
        plt.scatter(x,y, c='y')
        plt.title("Scatter of data after clustering algorithm has been run.")
        plt.xlabel("x axis")
        plt.ylabel("y axis")


        totaldata = []
        for i in data:
            totaldata.append(data[i])

        totaldata = np.array(totaldata)
        plot2 = plt.figure(2)
        x, y = totaldata.T
        plt.scatter(x,y, c = 'g')
        plt.title("Scatter of data before clustering algorithm has been run.")
        plt.xlabel("x axis")
        plt.ylabel("y axis")
        plt.show()

    def fit(self):
        f = open("K-means.txt", "w")
        if self.k == 3:
            centroids = {1: [2,10],2: [5,8],3: [1,2]} #setup initital centroid dict
            for i in centroids:
                f.write("Centroid " + str(i) + ": (" + str(round(centroids[i][0], 2)) + ", " + str(round(centroids[i][1],2)) + ")"+"\n")
        else: centroids = {} #if K != 3, still have a dict. Can have loop hereafter, to loop through first K elements and add to centroid dict.
        f.write("Clusters are empty.\n\n")
        f.close()

        #Now to start clustering:
        for i in range(1, self.iterations): #Repeat a certain number of times.
            
            clusters = {} #create new clusters dict to add new points to. (Prevents need to remove a coord once moved.)
            for d in range(1, self.k+1):
                clusters[d] = [] #Create new entry in dict of clusters, 0 through to 2 for each cluster. Each cluster will be a list of paired coordinates.

            #Assign each data point to closest centroid:
            for j in data: #loop from 0 to 7
                pair = data[j]
                distances = [self.getDistance(pair, centroids[centroid]) for centroid in centroids] #Get list of distances from point to each centroid
                clusterNr = distances.index(min(distances)) + 1 #take cluster nr of closest centroid

                clusters[clusterNr].append(pair) #append the coords to the closest cluster
                prev_centroids = copy.deepcopy(centroids) #Create copy of centroids dict.

            #Re-compute centroids of each cluster
            for l in centroids:
                c_x = 0
                c_y = 0
                for pair in clusters[l]:
                    c_x += pair[0]
                    c_y += pair[1]
                
                if (len(clusters[l]) != 0):
                    centroids[l][0] = c_x/len(clusters[l])
                    centroids[l][1] = c_y/len(clusters[l])
            
            self.writeToFile(i, clusters, centroids) #output current iteration data to textfile.

            stopCritMet = True
            for k in centroids:
                #print ("Difference: ", abs(centroids[i][0] - prev_centroids[i][0]) + abs(centroids[i][1] - prev_centroids[i][1]))
                if abs(centroids[k][0] - prev_centroids[k][0]) + abs(centroids[k][1] - prev_centroids[k][1]) > self.tol:
                    stopCritMet = False

            if stopCritMet == True:
                return self.iterations, clusters, centroids

        return self.iterations, clusters, centroids


derp = KMeans() #create Kmeans class
derp.fit() #call the fit function.
derp.drawScatter() #draw plots.
