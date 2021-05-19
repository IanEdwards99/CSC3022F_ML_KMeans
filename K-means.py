import math
import numpy as np
import copy
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

#data = np.array([[2,10], [2,5], [8,4], [5,8], [7,5], [6,4], [1,2], [4,9]])
data = np.array([[2,10], [2,5], [8,4], [5,8], [7,5], [6,4], [1,2], [4,9], [5,5], [4,3], [2,9], [7,6], [8,2], [3,3], [3,6], [0,9]])

x,y = data.T
# plt.scatter(x,y)
# plt.show()
K = 3 #number of clusters
centroids = {}
centroids[0] = [2,10]
centroids[1] = [5,8]
centroids[2] = [1,2]
#centroids = {[2,10],[5,8],[1,2]} #predefined centroids
for centroid in centroids:
    print(centroid)

quit()
clusters = []

def getClosestCentroid(x, y, centroids):
    min = math.sqrt((x-centroids[0][0])**2 + (y-centroids[0][1])**2) #Get distance from current point to first centroid
    bestCentroid = centroids[0] #current closest centroid
    for i in centroids:
        currentDist = math.sqrt((x-i[0])**2 + (y-i[1])**2) #Get distance from current point to current centroid
        if (currentDist < min): #closer centroid found
            min = currentDist
            bestCentroid = i
    return centroids.index(bestCentroid) #return which cluster has closest centroid. If 4 is closest centroid, cluster 1 is returned, out of cluster 0,1 and 2.

def recalculateCentroids(centroids):
    for i in range(0, len(clusters)): #get each cluster of values to recalculate its centroid
        meanx = 0
        meany = 0
        for j in clusters[i]: #loop through values of cluster and get the pair there.
            meanx += j[0]    
            meany += j[1]
        meanx = meanx/(len(clusters[i]))
        meany = meany/len(clusters[i])
        centroids[i] = [meanx, meany]

    return centroids

def display():
    for i in range(0, len(clusters)):
        print("Cluster: ", i+1, ": ", end="", sep = "")
        for j in range(0, len(clusters[i])):
            if (j < len(clusters[i])-1):
                print(data.index(clusters[i][j])+1, ", ", end = "", sep = "")
            else: print(data.index(clusters[i][j])+1, end = "", sep = "")
        print("\n")

if (len(data) % K != 0):
    itemsPerCluster = int(len(data)/K) +1
else:
    itemsPerCluster = (int)(len(data)/K)

classifications = {}


for i in range(K): #Divide data up into clusters.
    classifications[i] = data[i*itemsPerCluster:(i+1) * itemsPerCluster].tolist()

print(classifications)
print(centroids)

#begin algorithm
counter = 0
iteration = 1

while counter < 50:
    for datachunkNr in range(len(classifications)):
        for featureset in classifications[datachunkNr]:
            distances = [np.linalg.norm(np.array(featureset)-np.array(centroids[centroid])) for centroid in centroids] #get list of distances from a point to each centroid
            newCluster = distances.index(min(distances))
            if newCluster != datachunkNr:
                classifications[newCluster].append(featureset)
                classifications[datachunkNr].remove(featureset)

    prev_centroids = dict(centroids)
    for classification in classifications: #loop through each cluster
        centroids[classification] = np.average(classifications[classification], axis = 0).tolist()

    optimized = True
    for c in centroids:
        original_c = np.array(prev_centroids[c])
        current_c = np.array(centroids[c])
        if np.sum((current_c-original_c)/original_c*100) > 0.001:
            optimized = False
        
    if optimized:
        break
    counter += 1

print(centroids)
print(classifications)
mydata = []

for i in classifications:
    mydata.append(np.array(classifications[i]))
x,y = mydata[0].T
plot1 = plt.figure(1)
plt.scatter(x,y, c='b')
x,y = mydata[1].T
plt.scatter(x,y, c='r')
x,y = mydata[2].T
plt.scatter(x,y, c='y')

plot2 = plt.figure(2)
x, y = data.T
plt.scatter(x,y, c = 'g')
plt.show()
# f = open("K-means.txt", "w")
# f.write("how to write to a file.")
# f.close()

# f = open("K-means.txt", "r")
# print(f.read())


"""
    #print("Iteration ", iteration)
    iteration += 1
    display()

    for i in range(0, len(clusters)): #clusters is a list of 3 lists.
        for pair in clusters[i]: #get a pair of coords from each position in a current cluster
            newClusterNr = getClosestCentroid(pair[0], pair[1], centroids)
            if (newClusterNr != i):
                clusters[newClusterNr].append(pair) #add pair to new cluster
                clusters[i].remove(pair) #delete pair from old cluster
    
    counter += 1
    centroids = recalculateCentroids(centroids)
"""