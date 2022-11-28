import heapq
import copy
import numpy as np

def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (if second state is omitted then it is assumed that it is the goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """

    distance = 0 ## Variable initialization 
    numpy_state = np.reshape(from_state, (3 , 3)) ## Convert from state list to numpy array
    numpy_desired = np.reshape(to_state, (3, 3)) ## Convert to state list to numpy array

    for i in range(3): ## Loop through rows
        for j in range(3): ## Loop through columns
            if numpy_state[i][j] == 0: ## If the value is 0, skip
                continue

            x = int(np.where(numpy_desired == numpy_state[i][j])[0]) ## Get the row of the desired state
            y = int(np.where(numpy_desired == numpy_state[i][j])[1]) ## Get the column of the desired state
            distance += abs(i - x) + abs(j - y) ## Add the distance to the total distance

    return distance

def print_succ(state):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))


def get_succ(state):
    """
    TODO: implement this function.

    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
    """
    
    ## Array declarations 
    succ_states = list()
    right_list = [1, 2, 4, 5, 7, 8]
    left_list = [0, 1, 3, 4, 6, 7]
    up_list = [0, 1, 2, 3, 4, 5]
    down_list = [3, 4, 5, 6, 7, 8]
    
    for i in range(len(state)): ## Loop through the state
        ## Variable initializations
        right = i + 1
        left = i - 1
        up = i - 3
        down = i + 3
        if right in right_list: ## If the right move is valid
            if(state[right] == 0): ## If the right move is a 0
                temp_state = copy.deepcopy(state)
                temp_state[right] = state[i]  
                temp_state[i] = 0
                if temp_state not in succ_states and temp_state != state: ## If the state is not already in the list
                    succ_states.append(temp_state)
        if left in left_list: ## If the left move is valid
            if(state[left] == 0): ## If the left move is a 0
                temp_state = copy.deepcopy(state)
                temp_state[left] = state[i]
                temp_state[i] = 0
                if temp_state not in succ_states and temp_state != state: ## If the state is not already in the list
                    succ_states.append(temp_state)
        if up in up_list: ## If the up move is valid
            if(state[up] == 0): ## If the up move is a 0
                temp_state = copy.deepcopy(state)
                temp_state[up] = state[i]
                temp_state[i] = 0
                if temp_state not in succ_states and temp_state != state: ## If the state is not already in the list
                    succ_states.append(temp_state)
        if down in down_list: ## If the down move is valid
            if(state[down] == 0): ## If the down move is a 0
                temp_state = copy.deepcopy(state)
                temp_state[down] = state[i]
                temp_state[i] = 0
                if temp_state not in succ_states and temp_state != state: ## If the state is not already in the list
                    succ_states.append(temp_state)

    return sorted(succ_states)


def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: Implement the A* algorithm here.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
    """

    ## Variable declarations
    open = []
    visited = []
    index = 0

    h = get_manhattan_distance(state) ## Get the h value of the initial state
    heapq.heappush(open, (h , state, (0, h, -1))) ## Push the initial state to the open list

    while True: ## Loop until a solution is found
        if len(open) == 0: ## If the open list is empty, no solution was found
            break
        
        popped = heapq.heappop(open) ## Pop the lowest h value from the open list
        
        if popped[1] == goal_state: ## If the popped state is the goal state, print the path
            steps = list()
            current = popped
            while True: ## Loop until the initial state is reached
                steps.insert(0,current[1])
                if current[2][2] == -1: ## If the parent is the initial state, break
                    break
                else: ## Else, set the current state to the parent
                    current = visited[current[2][2]]
            for i in range(len(steps)): ## Print the path
                print(str(steps[i]) + ' h=' + str(get_manhattan_distance(steps[i])) + ' moves: ' + str(i))

            print("Max queue length: " + str(len(open) + 1)) ## Print the max queue length

            return True
        
        else: ## Else, add the popped state to the visited list
            visited.append(popped)
            g = popped[2][0] + 1
            successors = get_succ(popped[1])
            for succ in successors: ## Loop through the successors
                check  = -1
                for i in range(len(visited)): ## Loop through the visited list
                    if visited[i][1] == succ: ## If the successor is in the visited list, set the check variable
                        check = i
                        break           
                if check == -1 : ## If the successor is not in the visited list
                    h = get_manhattan_distance(succ)
                    heapq.heappush(open, (g + h , succ, (g , h, index)))
                else: ## Else, if the successor is in the visited list
                    if visited[check][2][0] > g : ## If the g value of the successor is greater than the current g value
                        visited[check] = (g + h , succ, (g , h, index))

            index += 1 ## Increment the index

if __name__ == "__main__":
    """
    Feel free to write your own test code here to examine the correctness of your functions. 
    Note that this part will not be graded. `
    """
    print_succ([2,5,1,4,0,6,7,0,3])
    print()

    print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    print()

    solve([4,3,0,5,1,6,7,2,0])
    print()