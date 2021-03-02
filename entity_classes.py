from collections import deque
import random

class Card:
    def __init__(self, val, st):
        self.value = val
        self.suit = st

class Deck:
    def __init__(self):
        self.cards = []
        # each card is represented by a letter for suit + number for value. A is 1, J, Q, K are 11, 12, 13 respectively
        for s in ["S", "H", "C", "D"]:
            for v in range(1, 14):
                self.cards.append(Card(v, s))
        self.cards.append(Card(-1, "jk"))
        self.cards.append(Card(-1, "jk"))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self):
        return self.cards.pop()
    
    def returnToDeck(self, card):
        self.cards.append(card)

class DiscardPile:
    def __init__(self):
        self.cards = deque()
    
    def draw(self):
        return self.cards.pop()
    
    def discard(self, card):
        self.cards.append(card)

class Hand:
    def __init__(self):
        self.cards = []
    
    def draw(self, card):
        self.cards.append(card)
    
    def discard(self, val):
        for index, card in enumerate(self.cards):
            if card.value == val:
                return self.cards.pop(index)
        return "error"