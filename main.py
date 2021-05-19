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


    def getDistance(self, pair1, pair2):
        return math.sqrt((pair1[0]-pair2[0])**2 + (pair1[1]-pair2[1])**2)

    def writeToFile(self, iteration, clusters, centroids):
        f = open("K-means.txt", "a")
        f.write("Iteration " + str(iteration)+"\n\n")
        for i in clusters:
            output = "Cluster " + str(i) + ": "
            for j in range(0, len(clusters[i])):
                feature = clusters[i][j]
                key_list = list(data.keys())
                val_list = list(data.values())
                pos = val_list.index(feature)
                key = key_list[pos]
                if j == len(clusters[i])-1:
                    output = output + str(key)
                else: output = output + str(key) + ", "
            
            f.write(output+"\n")
            f.write("Centroid: (" + str(round(centroids[i][0], 2)) + ", " + str(round(centroids[i][1],2)) + ")"+"\n\n")
            output = ""

        f.close()

    def drawScatter(self):
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


        totaldata = []
        for i in data:
            totaldata.append(data[i])

        totaldata = np.array(totaldata)
        plot2 = plt.figure(2)
        x, y = totaldata.T
        plt.scatter(x,y, c = 'g')
        plt.show()

    def fit(self):
        f = open("K-means.txt", "w")
        f.close()
        if self.k == 3:
            centroids = {1: [2,10],2: [5,8],3: [1,2]} #setup centroid dict
        else: centroids = {}

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

            print(clusters)
            break
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
            
            self.writeToFile(i, clusters, centroids)

            stopCritMet = True
            for k in centroids:
                #print ("Difference: ", abs(centroids[i][0] - prev_centroids[i][0]) + abs(centroids[i][1] - prev_centroids[i][1]))
                if abs(centroids[k][0] - prev_centroids[k][0]) + abs(centroids[k][1] - prev_centroids[k][1]) > self.tol:
                    stopCritMet = False

            if stopCritMet == True:
                #print("Done")
                break

        return self.iterations, clusters, centroids


derp = KMeans()
derp.fit()
#derp.drawScatter()
