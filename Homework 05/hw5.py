## Imports
import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
from pandas import Series

## Main function
def main(file):
    ## Create a list of the data
    year = [] 
    days = []

    with open(file) as csv_file: ## Open the file
        f = csv.reader(csv_file, delimiter=',')
        next(f)

        for row in f: ## For each row in the file
            if row[0] != '"': ## If the row is not a header
                year.append(int(row[0]))
            if row[-1] != '-': ## If the row is not a header
                days.append(int(row[-1]))

    s = Series(days, year) ## Create a series
    ax = s.plot.line() ## Plot the series
    ax.set_xlabel("Year") ## Set the x label
    ax.set_ylabel("Num of frozen days") ## Set the y label
    plt.savefig("plot.jpg") ## Save the plot

    #Q3a
    X = []

    for x in year: ## For each year
        vector = [1,x] ## Create a vector
        vector = np.array(vector) ## Convert to numpy array
        X.append(vector) ## Append to X

    X = np.array(X) ## Convert to numpy array

    ## Print the result
    print("Q3a: ")
    print(X)

    #Q3b
    Y = []

    for y in days: ## For each day
        Y.append(y) ## Append the day to the list

    Y = np.array(Y) ## Convert to numpy array

    ## Print the result
    print("Q3b: ")
    print(Y)

    #Q3c
    X_t = np.transpose(X) ## Transpose X
    Z = np.dot(X_t, X) ## Multiply X transpose by X

    ## Print the result
    print("Q3c: ")
    print(Z)

    #Q3d
    I = np.linalg.inv(Z) ## Invert Z

    ## Print the result
    print("Q3d: ")
    print(I)

    #Q3e 
    PI = np.dot(I, X_t) ## Multiply I by X transpose

    ## Print the result
    print("Q3e: ")
    print(PI)

    #Q3f
    hat_beta = np.dot(PI, Y) ## Multiply PI by Y

    ## Print the result
    print("Q3f: ")
    print(hat_beta)

    #Q4
    ## Initialize the list
    b_0 = hat_beta[0]
    b_1 = hat_beta[1]
    x_test = 2021
    y_test = b_0 + np.dot(b_1, x_test)

    print("Q4: " + str(y_test)) ## Print the result

    #Q5
    if b_1 > 0: ## If b_1 is positive
        print("Q5a: >")
        print("Q5b: The sign of greater than means that the number of winter days has an increasing (positive) trend along with years.")
    elif b_1 < 0: ## If b_1 is negative
        print("Q5a: <")
        print("Q5b: The sign of less than means that the number of winter days has a decreasing (negative) trend along with years.")
    else: ## If b_1 is 0
        print("Q5a: =") 
        print("Q5b: The sign of equal to means that the number of winter days does not change along with years.")

    #Q6
    x_star = -(b_0) / (b_1) ## Calculate x_star

    ## Print the result
    print("Q6a: "+ str(x_star))
    print("Q6b: We can see from the graph that the frozen days could be different between two consecutive years. That means it is possible for Mendota to freeze again after the prediction year. So I feel like the x* is not a perfect compelling prediction that states Mendota will no longer freeze." )

if __name__ == "__main__":
    main(sys.argv[1]) ## Run the main function