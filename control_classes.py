from entity_classes import *

class GameMgr:
    def __init__(self, seed=None):
        self.deck = Deck()
        self.discardPile = DiscardPile()
        self.hand1 = Hand()
        self.hand2 = Hand()
        
        # initializes game state
        self.deck.shuffle(seed)
        self.deck.joker = self.deck.draw()
        for _ in range(13):
            self.hand1.draw(self.deck.draw())
            self.hand2.draw(self.deck.draw())
        self.discardPile.discard(self.deck.draw())

        print("Hand 1:", self.hand1)
        print()
        print("Hand 2:", self.hand2)
        print()
        print(self.discardPile)
        print()
        print(self.deck)
        print("Joker:", self.deck.joker)
        print("Length of deck:", len(self.deck.cards))
        print()

class Player:
    pass

class BasicAgent(Player):
    pass

class AdvancedAgent(Player):
    pass


if __name__ == "__main__":
    GameMgr(123)