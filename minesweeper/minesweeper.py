import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        known_mines = set()
        if self.count == len(self.cells) and self.count != 0:
            for i in self.cells:
                known_mines.add(i)
        return known_mines



    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        known_safes = set()
        if self.count == 0:
            for i in self.cells:
                known_safes.add(i)
        return known_safes




    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell not in self.cells:
            return

        updated = set()

        for acell in self.cells:
            if acell == cell:
                continue
            updated.add(acell)

        self.cells = updated
        if len(updated) == 0:
            self.count = 0
        else:
            self.count -= 1
        return
        


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        
        if cell not in self.cells:
            return

        updated = set()

        for acell in self.cells:
            if acell == cell:
                continue
            updated.add(acell)

        self.cells = updated
        return



class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_cell(self,width,height,cell,cells):
        if (width,height) != cell:
            if cell[0] - width >= -1 and cell[0] - width <= 1:
                if cell[1] - height >= -1 and cell[1] - height <= 1:
                    neighbor_cell = (width,height)
                    cells.add(neighbor_cell)
    


    
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        cells = set()
        self.moves_made.add(cell)
        self.mark_safe(cell)
        print (f"{cell[0]},{cell[1]}")
        
        for width in range(self.width):
            for height in range(self.height):
                if (width,height) not in self.moves_made and (width,height) not in self.safes:
                    self.add_cell(width,height,cell,cells)
                
        

        temp = copy.deepcopy(self.knowledge)
        sentence = Sentence(cells,count)
        self.knowledge.append(sentence)

        print(sentence)
        while temp != self.knowledge:
            temp = copy.deepcopy(self.knowledge)
            for sentence in self.knowledge:
                new_mines = sentence.known_mines()
                new_safes = sentence.known_safes()
                if new_safes is not None:
                    self.safes = self.safes.union(new_safes)
                if new_mines is not None:
                    self.mines = self.mines.union(new_mines) 

                for new_cell in sentence.cells.copy():
                    if new_cell in new_mines:
                        self.mark_mine(new_cell)

                    if new_cell in new_safes:
                        self.mark_safe(new_cell)
                    
            # for sentence in self.knowledge:        
            #     if len(sentence.cells) == 0:
            #             self.knowledge.remove(sentence)


        # print(self.knowledge[0])
        # print("1")
            new_knowledge = []
            remove_list = []
            for sentence in self.knowledge:
                for i in range(len(self.knowledge)):
                    if sentence.cells != self.knowledge[i].cells:
                        if sentence.cells.issubset(self.knowledge[i].cells) and len(sentence.cells)!=0:
                            difference = self.knowledge[i].cells.difference(sentence.cells)
                            new_count = self.knowledge[i].count - sentence.count
                            new_sentence = Sentence(difference, new_count)
                            new_knowledge.append(new_sentence)
                            remove_list.append(self.knowledge[i])


            for new in new_knowledge:
                self.knowledge.append(new) 

            for remove in remove_list:
                if remove in self.knowledge:
                    self.knowledge.remove(remove)                       

        
        print("UPDATED KNOWLEDGE")
        for sentence in self.knowledge:
            print(sentence)
        

    

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) == 0:
            return None
            print("none")
        else:
            for move in self.safes:
                if move not in self.moves_made:
                    return move
        


        # raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:
            x = random.randint(0,7)
            y = random.randint(0,7)
            move = (x,y)

            if move not in self.mines and move not in self.moves_made:
                print (f"{x},{y}")
                return move
            

        raise NotImplementedError
