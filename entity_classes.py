from collections import deque
import numpy as np
import random

suitDict = {"S": 0, "H": 1, "C": 2, "D":3}

class Card:
    def __init__(self, val, st):
        self.value = val
        self.suit = st
    
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
        self.cards.append(Card(-1, "jk"))
        self.cards.append(Card(-1, "jk"))
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
    
    def checkMelds(self):  # only checks for win state for now, returns bool if game is won
        pass