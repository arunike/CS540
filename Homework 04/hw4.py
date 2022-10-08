## Imports
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy

## Load data from csv file
def load_data(filepath): 
    list_dict = list() 
    with open(filepath) as csv_file: ## Open file
        reader = csv.DictReader(csv_file) ## Read file
        for row in reader: ## Iterate over rows
            list_dict.append(row) ## Append row to list
    
    return list_dict

## Calculate features
def calc_features(row):
    array = np.append(np.zeros(shape = (6,0)), [int(row['Attack']), int(row['Sp. Atk']), int(row['Speed']), int(row['Defense']), int(row['Sp. Def']), int(row['HP'])])
    
    return array.astype(np.int64)

## Hierarchical Agglomerative Clustering
def hac(features):
    features_length = len(features) ## Get length of features
    distanceMatrix = np.empty([features_length, features_length]) ## Create empty distance matrix
    dataPoints = dict() ## Create empty dictionary for data points

    for label in range(features_length): ## Iterate over features
        dataPoints[label] = [label]

    for i in range(features_length): ## Iterate over features
        for j in range(features_length):
            if i == j:
                continue
            distanceMatrix[i][j] = np.linalg.norm(features[i] - features[j]) ## Calculate distance between features

    Z = np.empty([0,4]) ## Create empty array for Z
    index = features_length ## Set index to length of features
    
    for n in range(features_length - 1): ## Iterate over features
        minimum = float('inf') ## Set minimum to infinity
        z_0 = 0
        z_1 = 0

        for i in dataPoints: ## Iterate over data points
            for j in dataPoints:
                if i == j: 
                    continue

                cluster_i = dataPoints[i] ## Get cluster i
                cluster_j = dataPoints[j] ## Get cluster j
                maximum = float('-inf') ## Set maximum to negative infinity
                
                for ci in cluster_i: ## Iterate over cluster i
                    for cj in cluster_j: ## Iterate over cluster j
                        if maximum < distanceMatrix[ci][cj]: ## If maximum is less than distance between ci and cj
                            maximum = distanceMatrix[ci][cj]
                
                if minimum > maximum:  ## If minimum is greater than maximum
                    minimum = maximum
                    z_0 =  i
                    z_1 = j
                    
                elif maximum == minimum: ## If maximum is equal to minimum
                    if z_0 > i:
                        z_0 =  i
                        z_1 = j
                    elif z_0 == i:
                        if z_1 > j:
                            z_1 = j
        
        dataPoints[index] = dataPoints[z_0] + dataPoints[z_1] ## Add data points to index
        
        ## Remove old data points
        del dataPoints[z_0]
        del dataPoints[z_1]

        Z = np.vstack([Z, [z_0, z_1, minimum, len(dataPoints[index])]]) ## Add to Z
        
        index += 1 ## Increment index
    return Z

## Plot visualization
def imshow_hac(Z): 
    plt.figure()
    hierarchy.dendrogram(Z)
    plt.show()

if __name__ == '__main__':
    def main():
        imshow_hac(hac([calc_features(row) for row in load_data('Pokemon.csv')][:30]))

    main()