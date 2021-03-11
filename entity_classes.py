from collections import deque
import numpy as np
import random

suitDict = {"S": 0, "H": 1, "C": 2, "D":3}

# Helper functions for matrix representation of cards

# Gets index of first occuring card in a hand (row-wise)
def getFirstCard(matrix, shp):
    for i in range(shp[0]):
        for j in range(shp[1]):
            if matrix[i][j]:
                return (i, j)

# Gets all indexes of same value for same-value melds
def getSameValue(matrix, index):
    j = index[1]
    result = []
    for i in range(4):
        if i != index[0] and matrix[i][j]:
            result.append(i)
    return result

# Entity classes

class Card:
    def __init__(self, val, st):
        self.value = val  # actual number on card
        self.suit = st
        self.points = val  # point value of card
        if val == -1:  # joker cards have no points
            self.points = 0
        elif val == 1 or val > 10:  # ace and face cards
            self.points = 10
    
    def __repr__(self) -> str:
        return "Card()"
    
    def __str__(self) -> str:
        strVal = ["A"] + [str(x) for x in range(2, 11)] + ["J", "Q", "K"]
        if self.value != -1:
            return self.suit + strVal[self.value - 1]
        else:
            return "JKR"

class Deck:
    def __init__(self):
        self.cards = []
        # each card is represented by a letter for suit + number for value. A is 1, J, Q, K are 11, 12, 13 respectively
        for s in suitDict.keys():
            for v in range(1, 14):
                self.cards.append(Card(v, s))
        self.cards.append(Card(-1, "JK1"))
        self.cards.append(Card(-1, "JK2"))
        self.joker = None
    
    def __repr__(self) -> str:
        return "Deck()"
    
    def __str__(self) -> str:
        output = "Deck: "
        for card in self.cards:
            output += str(card) + "    "
        return output
    
    def shuffle(self, seed):
        if seed:
            random.seed(seed)
        random.shuffle(self.cards)
    
    def draw(self):
        return self.cards.pop()
    
    def returnToDeck(self, card):
        self.cards.append(card)

class DiscardPile:
    def __init__(self):
        self.cards = deque()
    
    def __repr__(self) -> str:
        return "DiscardPile()"
    
    def __str__(self) -> str:
        output = "Discard Pile: "
        for card in self.cards:
            output += str(card) + "    "
        return output
    
    def draw(self):
        return self.cards.pop()
    
    def discard(self, card):
        self.cards.append(card)

class Hand:
    def __init__(self):
        self.cards = []
        self.cardMatrix = np.zeros((4,13))
        self.jokers = 0
    
    def __repr__(self) -> str:
        return "Hand()"
    
    def __str__(self) -> str:
        output = ""
        for card in self.cards:
            output += str(card) + "    "
        return output
    
    def draw(self, card):
        self.cards.append(card)
        if card.value != -1:
            self.cardMatrix[suitDict[card.suit]][card.value-1] = 1
        else:
            self.jokers += 1
    
    def discard(self, val):
        for index, card in enumerate(self.cards):
            if card.value == val:
                if val != -1:
                    self.cardMatrix[suitDict[card.suit]][card.value-1] = 0
                else:
                    self.jokers -= 1
                return self.cards.pop(index)
        return "error"

    def checkMelds(self, matrix=None, jkr=None):  # only checks for win state for now, returns bool if game is won
        if matrix==None:
            matrix = self.cardMatrix.copy()
        if jkr==None:
            jkr = self.jokers.copy()
        # Recursive function
        # find first 1 in matrix, check all melds including chances+jokers (reduce num of jokers in this case) using this card
        # for each meld, recursive call checkMelds with new matrix, without the cards in the meld being considered
        # if no chances => return false, backtrack one step
        # base case => matrix is all 0s, return true
        # end of recursion case => if all melds lead to false, return false

        # Base case:
        if np.all(matrix==0):
            return True
        
        # Recursive case
        # search for straight melds on right side only, prevents overlap
        shp = np.shape(matrix)
        i, j = getFirstCard(matrix, shp)
        if j == 12:  # king
            right1 = right2 = right3 = (False, (i,j))
        elif j == 11:  # queen
            right1 = (bool(matrix[i][j+1]), (i, j+1))
            right2 = (bool(matrix[i][0]), (i, 0))
            right3 = False
        elif j == 10:  # jack:
            right1 = (bool(matrix[i][j+1]), (i, j+1))
            right2 = (bool(matrix[i][j+2]), (i, j+2))
            right3 = (bool(matrix[i][0]), (i, 0))
        else:
            right1 = (bool(matrix[i][j+1]), (i, j+1))
            right2 = (bool(matrix[i][j+2]), (i, j+2))
            right3 = (bool(matrix[i][j+3]), (i, j+3))
        
        melds = []
        # no elif anywhere in case the other card needs to be used for something; considers all cases

        # straight melds
        # pure highest in order so it's considered first if possible
        if right1[0] and right2[0]:
            # add to melds here
            if right3[0]:
                # add to melds here
                pass
            if jkr:
                # add to melds here
                pass
        if right1[0] and jkr:
            # add to melds here
            if right3[0]:
                # add to melds here
                pass
        if right2[0] and jkr:
            # add to melds here
            if right3[0]:
                # add to melds here
                pass
        if right3[0] and jkr==2:
            # add to melds here
            pass
        if jkr==2:
            # add to melds here
            pass

        # same value melds
        j_vals = getSameValue(matrix, (i, j))
        if len(j_vals) == 3:
            # add to melds here
            pass
        if len(j_vals) == 2:
            # add to melds here
            pass
        if jkr:
            # add to melds here
            pass
