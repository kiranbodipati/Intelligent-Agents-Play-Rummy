from entity_classes import *
import random

class GameMgr:
    def __init__(self, seed=None):
        self.deck = Deck()
        self.discardPile = DiscardPile()
        self.Player1 = Player()
        self.Player2 = Player()
        # initializes game state
        
        
        self.DealGame(seed)

        print("Hand 1:", self.Player1.hand)
        print()
        print("Hand 2:", self.Player2.hand)
        print()
        print(self.discardPile)
        print()
        print(self.deck)
        print("Joker:", self.deck.joker)
        print("Length of deck:", len(self.deck.cards))
        print()

        self.PlayPvP()

    def DealGame(self, seed):
        # initializes game state
        self.deck.shuffle(seed)
        self.deck.joker = self.deck.draw()
        for _ in range(13):
            self.Player1.hand.draw(self.deck.draw())
            self.Player2.hand.draw(self.deck.draw())
        self.discardPile.discard(self.deck.draw())    
    
    def PlayPvP(self):
        CurrentPlayer=random.choice([1,2])
        self.turn=0
        while(True):
            self.Play(CurrentPlayer)
            self.turn+=1
            if CurrentPlayer==1:
                if self.Player1.hand.checkMelds()==True:
                    break
                CurrentPlayer=2
            elif CurrentPlayer==2:
                if self.Player2.hand.checkMelds()==True:
                    break
                CurrentPlayer=1
            print("Turn:",self.turn)

    
    def Play(self, CurrentPlayer):
        print(int(CurrentPlayer), "\'s turn:")
        if CurrentPlayer==1:
            
            print("Hand:", self.Player1.hand)
            print()
            print("Where do you want to?\n Enter \n'D' to draw from Deck \n 'P' to draw from discard pile")
            
            loc=input()
            if loc=='D':
                self.Player1.hand.draw(self.deck.draw())
            elif loc=='P':
                self.Player1.hand.draw(self.discardPile.draw())
            print("index: ", "".join([str(x)+"   " for x in range(0, len(self.Player1.hand.cards))]))
            print("Hand:", self.Player1.hand)
            print("enter index of card to disard:")
            ind=int(input())
            self.discardPile.discard(self.Player1.hand.discard(ind))
            print("Hand:", self.Player1.hand)
        
        if CurrentPlayer==2:
            
            print("Hand:", self.Player2.hand)
            print()
            print("Where do you want to?\n Enter \n'D' to draw from Deck \n 'P' to draw from discard pile")
            
            loc=input()
            if loc=='D':
                self.Player2.hand.draw(self.deck.draw())
            elif loc=='P':
                self.Player2.hand.draw(self.discardPile.draw())
            print("index: ", "".join([str(x)+"   " for x in range(0, len(self.Player1.hand.cards))]))
            print("Hand:", self.Player2.hand)
            print("enter index of card to disard:")
            ind=int(input())
            self.discardPile.discard(self.Player2.hand.discard(ind))
            print("Hand:", self.Player2.hand)

class Player:
    def __init__(self):
        self.hand = Hand()
    

class BasicAgent(Player):
    pass

class AdvancedAgent(Player):
    pass


if __name__ == "__main__":
    GameMgr(123)