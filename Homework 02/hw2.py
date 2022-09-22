# Importations
import sys
import string
import math

def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multi-nominal
    parameter vector (characters probabilities of English and Spanish) as
    described in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    # Implementing vectors e,s as lists (arrays) of length 26
    # with p[0] being the probability of 'A' and so on
    e = [0] * 26
    s = [0] * 26
    

    with open('./e.txt', encoding = 'utf-8') as f:
        for line in f:
            # strip: removes the newline character
            # split: split the string on space character
            char, prob = line.strip().split(" ")
            # ord('E') gives the ASCII (integer) value of character 'E'
            # we then subtract it from 'A' to give array index
            # This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char) - ord('A')] = float(prob)
    f.close()

    with open('./s.txt',encoding = 'utf-8') as f:
        for line in f:
            char, prob = line.strip().split(" ")
            s[ord(char) - ord('A')] = float(prob)
    f.close()

    return (e,s)

def shred(filename):

    # Using a dictionary here. You may change this to any data structure of
    # your choice such as lists (X=[]) etc. for the assignment
    X = dict()
    with open (filename, encoding = 'utf-8') as f:
        # TODO: add your code here
        X = dict.fromkeys(string.ascii_uppercase, 0) # Initialize dictionary with all letters and 0

        # Iterate through each line in the file
        for line in f:
            uppercase = line.upper().replace(' ', '').replace('\n', '')
            for char in uppercase:
                if char.isalpha():
                    X[char] += 1
    return X

# TODO: add your code here for the assignment
# You are free to implement it as you wish!
# Happy Coding!

def Q1():
    X = shred('./samples/letter2.txt')
    print('Q1')
    
    for key, value in X.items():
        print(key, value)

def Q2(filename):
    # Get dictionary of letter counts
    X = shred(filename) 
    y = get_parameter_vectors()

    print('Q2')
    print('{:.4f}'.format(round(X["A"] * math.log(y[0][0]), 4)))
    print('{:.4f}'.format(round(X["A"] * math.log(y[1][0]), 4)))

def Q3(filename):
    # Get dictionary of letter counts
    X = shred(filename) 
    y = get_parameter_vectors()

    # Compute probabilities
    english_total = 0
    english_counter = 0
    spanish_total = 0
    spanish_counter = 0

    # Iterate through each character in the dictionary
    for char in X: 
        english_total += X[char] * math.log(y[0][english_counter])
        english_counter +=1
        
    english = english_total + math.log(0.6) # Add the probability of English
    
    # Iterate through each character in the dictionary
    for char in X:
        spanish_total += X[char] * math.log(y[1][spanish_counter])
        spanish_counter +=1
        
    spanish = spanish_total + math.log(0.4) # Add the probability of Spanish
    
    print('Q3')
    print('{:.4f}'.format(round(english, 4)))
    print('{:.4f}'.format(round(spanish, 4)) )   

def Q4(filename):
    # Get dictionary of letter counts
    X = shred(filename) 
    y = get_parameter_vectors()

    # Compute probabilities
    english_total = 0
    english_counter = 0
    spanish_total = 0
    spanish_counter = 0

    # Iterate through each character in the dictionary
    for char in X: 
        english_total += X[char] * math.log(y[0][english_counter])
        english_counter +=1
        
    english = english_total + math.log(0.6) # Add the probability of English
    
    # Iterate through each character in the dictionary
    for char in X:
        spanish_total += X[char] * math.log(y[1][spanish_counter])
        spanish_counter +=1
        
    spanish = spanish_total + math.log(0.4) # Add the probability of Spanish

    print('Q4')

    # Determine which language is more likely
    difference = spanish - english
    if(difference >= 100):
        print('{:.4f}'.format(0))
    elif(difference <= -100):
        print('{:.4f}'.format(1))
    else:
        print('{:.4f}'.format(round(1 / (1 + math.e ** difference), 4)))

def main():
    Q1()
    Q2('./samples/letter2.txt')
    Q3('./samples/letter2.txt')
    Q4('./samples/letter2.txt')

if __name__ == "__main__":
    main()