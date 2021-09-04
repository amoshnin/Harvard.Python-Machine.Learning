import itertools
import random
from typing import *


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines: Set[Tuple[int, int]] = set()
        self.mines_found: Set[Tuple[int, int]] = set()

        # Initialize an empty field with no mines
        self.board: List[List[bool]] = []
        for i in range(self.height):
            row = [False] * self.width
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

    def print(self):
        """
        Prints a text-based representation of where mines are located.
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

    def is_mine(self, cell: Tuple[int, int]):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell: Tuple[int, int]):
        """
        Returns the number of mines that are within one row and column of a given cell, not including the cell itself.
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
    Logical statement about a Minesweeper game. A sentence consists of a set of board cells, and a count of how many of those cells are mines.
    """

    def __init__(self, cells: Set[Tuple[int, int]], count: int):
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

        if (len(self.cells) == self.count):
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        if (self.count == 0):
            return self.cells
        return set()

    def mark_mine(self, cell: Tuple[int, int]):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        if (cell not in self.cells):
            return

        self.cells.discard(cell)
        self.count -= 1

    def mark_safe(self, cell: Tuple[int, int]):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        if (cell not in self.cells):
            return

        self.cells.discard(cell)


class MinesweeperAI():
    """
    Minesweeper game player.
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made: Set[Tuple[int, int]] = set()

        # Keep track of cells known to be safe or mines
        self.mines: Set[Tuple[int, int]] = set()
        self.safes: Set[Tuple[int, int]] = set()

        # List of sentences about the game known to be true
        self.knowledge: List[Sentence] = []

    def mark_mine(self, cell: Tuple[int, int]):
        """
        Marks a cell as a mine, and updates all knowledge to mark that cell as a mine as well.
        """

        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell: Tuple[int, int]):
        """
        Marks a cell as safe, and updates all knowledge to mark that cell as safe as well.
        """

        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_sentence(self, sentence: Sentence):
        """
        Append sentence into knowledge. And, recursivelly, try add any new sentences if they can be inferred from the previous knowledge.
        """

        # ignore if sentence is not helpfull
        if len(sentence.cells) == 0:
            return

        # ignore if sentence is already in knowledge
        for prev_sentence in self.knowledge:
            if sentence == prev_sentence:
                return

        self.knowledge.append(sentence)
        inferred_sentences: List[Sentence] = []

        for prev_sentence in self.knowledge[0:-1]:
            if len(prev_sentence.cells) == 0:
                continue

            if sentence.cells.issubset(prev_sentence.cells):
                # print(sentence, 'is subset of', prev_sentence)
                inferred_sentences.append(Sentence(
                    prev_sentence.cells.difference(sentence.cells),
                    prev_sentence.count - sentence.count
                ))

            if prev_sentence.cells.issubset(sentence.cells):
                # print(prev_sentence, 'is subset of', sentence)
                inferred_sentences.append(Sentence(
                    sentence.cells.difference(prev_sentence.cells),
                    sentence.count - prev_sentence.count
                ))

        for inferred_sentence in inferred_sentences:
            # print('Inferred sentence:', inferred_sentence)
            self.add_sentence(inferred_sentence)

    def add_knowledge(self, cell: Tuple[int, int], count: int):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        """

        self.moves_made.add(cell)
        self.mark_safe(cell)

        # add a new sentence to the AI's knowledge base based on the value of `cell` and `count`;
        new_sentence_cells = set()
        for i in range(cell[0]-1, cell[0]+2):
            for j in range(cell[1]-1, cell[1]+2):
                if (i, j) == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    new_sentence_cells.add((i, j))

        new_sentence = Sentence(new_sentence_cells, count)

        # be sure to only include cells whose state is still undetermined in the sentence.
        for cell in new_sentence_cells:
            if cell in self.mines:
                new_sentence.mark_mine(cell)
            elif cell in self.safes:
                new_sentence.mark_safe(cell)

        self.add_sentence(new_sentence)

        # mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        new_mines = []
        new_safes = []

        for sentence in self.knowledge:
            for cell in sentence.known_mines():
                new_mines.append(cell)
            for cell in sentence.known_safes():
                new_safes.append(cell)

        for cell in new_mines:
            self.mark_mine(cell)
        for cell in new_safes:
            self.mark_safe(cell)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        available = self.safes.difference(self.moves_made)
        if len(available) > 0:
            return available.pop()
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        """

        # Should choose randomly among cells that: have not already been chosen, and are not known to be mines
        available: Set[Tuple[int, int]] = set()
        for i in range(self.height):
            for j in range(self.width):
                available.add((i, j))

        available.difference_update(self.moves_made)
        available.difference_update(self.mines)

        if len(available) > 0:
            return random.choice(tuple(available))
        return None
