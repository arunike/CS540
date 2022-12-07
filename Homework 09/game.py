import random
import copy

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    ## Check if the game is in drop phase or move phase
    def check_drop_phase(self, state):
        ## Variable declarations
        myCount = 0
        opponentCount = 0

        for i in range(len(state)): ## Loop through the state
            for j in range(len(state[0])): ## Loop through the state to count the number of pieces
                if(state[i][j] == self.my_piece): ## If the piece is mine, increment myCount
                    myCount += 1
                elif(state[i][j] == self.opp): ## If the piece is opponent's, increment opponentCount
                    opponentCount += 1

        if (opponentCount < 4 or myCount < 4): ## If the number of pieces is less than 4, return True
            return True

        return False

    ## Generate the successor states
    def succ(self, state):
        ## Variable declarations
        successors = []
        drop_phase = False
        myCount = 0
        oppCount = 0
        myPosition = []
        
        for i in range(len(state)): ## Loop through the state
            for j in range(len(state[0])): ## Loop through the state to count the number of pieces
                if(state[i][j] == self.my_piece): ## If the piece is mine, increment myCount
                    myPosition.append([i, j])
                    myCount += 1
                elif(state[i][j] == self.opp): ## If the piece is opponent's, increment opponentCount
                    oppCount += 1
        if (oppCount < 4 or myCount < 4): ## If the number of pieces is less than 4, return True
            drop_phase = True

        if drop_phase: ## If the game is in drop phase
            for i in range(len(state)): ## Loop through the state
                for j in range(len(state[0])): ## Loop through the state to find the empty spaces
                    if(state[i][j] == ' '): ## If the space is empty, add it to the successors
                        successors.append([i, j])
        else: ## If the game is in move phase
            for pos in myPosition: ## Loop through the positions of my pieces
                row = [pos[0] - 1, pos[0], pos[0] + 1]
                col = [pos[1] - 1, pos[1], pos[1] + 1]

                for x in row: ## Loop through the row to find the empty spaces
                    for y in col: ## Loop through the column to find the empty spaces
                        if x > -1 and x < 5 and y > -1 and y < 5 and state[x][y] == ' ': ## If the space is empty, add it to the successors
                            successors.append([x, y, pos[0], pos[1]])

        random.shuffle(successors) ## Shuffle the successors

        return successors

    ## Heuristic function to evaluate the state
    def heuristic_game_value(self, state):
        terminal = self.game_value(state) ## Check if the game is over

        if(terminal != 0): ## If the game is over, return terminal
            return terminal

        ## Variable initializations
        max_val = float('-inf')
        min_val = float('inf')

        for row in state: ## Loop through the state
            for col in range(2): ## Loop through the state of 2 to find the 4 in a row
                pieces = []

                for i in range(4): ## Loop through the state of 4 to find the 4 in a row
                    pieces.append(row[col + i])
                
                ## Determine the maximum and minimum values
                max_val = max(max_val, pieces.count(self.my_piece) * 0.2 )
                min_val = min(min_val, pieces.count(self.opp) * (-0.2))

        for col in range(5): ## Loop through the state
            for row in range(2): ## Loop through the state of 2 to find the 4 in a row
                pieces = []

                for i in range(4): ## Loop through the state of 4 to find the 4 in a row
                    pieces.append(state[row + i][col])

                ## Determine the maximum and minimum values
                max_val = max(max_val, pieces.count(self.my_piece) * 0.2 )
                min_val = min(min_val, pieces.count(self.opp) * (-0.2))

        for row in range(2): ## Loop through the state
            for col in range(2): ## Loop through the state of 2 to find the 4 in a row
                pieces = []

                for i in range(4): ## Loop through the state of 4 to find the 4 in a row
                    if(col + i < 5 and row + i < 5): ## If the column and row are less than 5, add it to the pieces
                        pieces.append(state[row + i][col + i] )

                ## Determine the maximum and minimum values
                max_val = max(max_val, pieces.count(self.my_piece) * 0.2 )
                min_val = min(min_val, pieces.count(self.opp) * 0.2 * (-1) )

        for row in range(2): ## Loop through the state
            for col in range(3, 5): ## Loop through the state of 3 to 5 to find the 4 in a row
                pieces = list() 

                for i in range(4): ## Loop through the state of 4 to find the 4 in a row
                    if(col - i >= 0 and row + i < 5): ## If the column and row are greater than 0 and less than 5, add it to the pieces
                        pieces.append( state[row + i][col - i] )

                ## Determine the maximum and minimum values
                max_val = max(max_val, pieces.count(self.my_piece) * 0.2 )
                min_val = min(min_val, pieces.count(self.opp) * 0.2 * (-1) )
                
        for row in range(4): ## Loop through the state
            for col in  range(4): ## Loop through the state of 4 to find the 4 in a row
                pieces = list()
                pieces.append(state[row][col])
                pieces.append(state[row][col + 1])
                pieces.append(state[row + 1][col])
                pieces.append(state[row + 1][col + 1])
                max_val = max(max_val, pieces.count(self.my_piece) * 0.2 )
                min_val = min(min_val, pieces.count(self.opp) * (-0.2))

        return max_val + min_val

    ## Max value function to determine the maximum value of the state
    def max_value(self, state, depth):
        if(self.game_value(state) != 0): ## If the game is over, return the game value
            return self.game_value(state)
        if(depth > 1): ## If the depth is greater than 1, return the heuristic game value
            return self.heuristic_game_value(state)
        if (self.check_drop_phase(state)): ## If the game is in drop phase
            alpha = float('-inf')
            succ_list = self.succ(state)

            for row, col in succ_list: ## Loop through the successors
                temp_state = copy.deepcopy(state)
                temp_state[row][col] = self.my_piece
                alpha = max(alpha, self.min_value(temp_state, depth + 1))
        else: ## If the game is in move phase
            alpha = float('-inf')
            succ_list = self.succ(state)

            for row, col, source_row, source_col in succ_list: ## Loop through the successors
                temp_state = copy.deepcopy(state)
                temp_state[row][col] = self.my_piece
                temp_state[source_row][source_col] = ' '
                alpha = max(alpha, self.min_value(temp_state, depth + 1))

        return alpha
    
    ## Min value function to determine the minimum value of the state
    def min_value(self, state, depth):
        if(self.game_value(state) != 0): ## If the game is over, return the game value
            return self.game_value(state)
        if(depth > 1): ## If the depth is greater than 1, return the heuristic game value
            return self.heuristic_game_value(state)
        if (self.check_drop_phase(state)): ## If the game is in drop phase
            beta = float('inf')
            succ_list = self.succ(state)

            for row, col in succ_list: ## Loop through the successors
                temp_state = copy.deepcopy(state)
                temp_state[row][col] = self.opp
                beta = min(beta,  self.max_value(temp_state, depth + 1))
        else: ## If the game is in move phase
            beta = float('inf')
            succ_list = self.succ(state)

            for row, col, source_row, source_col in succ_list: ## Loop through the successors
                temp_state = copy.deepcopy(state)
                temp_state[row][col] = self.opp
                temp_state[source_row][source_col] = ' '
                beta = min(beta, self.max_value(temp_state, depth + 1))

        return beta

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        drop_phase = self.check_drop_phase(state) # TODO: detect drop phase

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        move = []
        nextMove = []
        
        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            succ_list = self.succ(state)
            max_succ_val = float('-inf')

            for row, col, source_row, source_col in succ_list: ## Loop through the successors
                temp_state = copy.deepcopy(state)
                temp_state[row][col] = self.my_piece
                temp_state[source_row][source_col] = ' '
                succ_val = self.max_value(temp_state, 0)

                if(succ_val > max_succ_val): ## If the successor value is greater than the max successor value
                    nextMove = [(row, col), (source_row, source_col)]
                    max_succ_val = succ_val

            move = nextMove ## Set the move to the next

            return move
        else: ## If the game is in drop phase
            succ_list = self.succ(state)
            max_succ_val = float('-inf')

            for row, col in succ_list: ## Loop through the successors
                temp_state = copy.deepcopy(state)
                temp_state[row][col] = self.my_piece
                suc_val = self.max_value(temp_state, 0)

                if(suc_val > max_succ_val): ## If the successor value is greater than the max successor value
                    nextMove = [row, col]
                    max_succ_val = suc_val

        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, (nextMove[0], nextMove[1]))
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # TODO: check \ diagonal wins
        for i in range(2):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == state[i + 3][j + 3]:
                    return 1 if state[i][j] == self.my_piece else -1

        # TODO: check / diagonal wins
        for i in range(2):
            for j in range(3,5):
                if state[i][j] != ' ' and state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2] == state[i + 3][j - 3]:
                    return 1 if state[i][j] == self.my_piece else -1

        # TODO: check box wins
        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i][j + 1] == state[i + 1][j] == state[i + 1][j + 1]:
                    return 1 if state[i][j] == self.my_piece else -1
        
        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAME PLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                        (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()