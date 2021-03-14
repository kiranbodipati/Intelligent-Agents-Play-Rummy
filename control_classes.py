from entity_classes import *
import random

class GameMgr:
    def __init__(self, seed=None):
        self.deck = Deck()
        self.discardPile = DiscardPile()
        # self.Player1 = Player()
        # self.Player2 = Player()
        # initializes game state
        self.Players = [Player(), Player()]
        
        self.DealGame(seed)

        print("Hand 1:", self.Players[0].hand)
        print()
        print("Hand 2:", self.Players[1].hand)
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
        self.Players[0].hand.setJoker(self.deck.joker.value)
        self.Players[0].hand.setJoker(self.deck.joker.value)
        for _ in range(13):
            self.Players[0].hand.draw(self.deck.draw())
            self.Players[1].hand.draw(self.deck.draw())
        self.discardPile.discard(self.deck.draw())    
    
    def PlayPvP(self):
        CurrentPlayer=random.choice([0,1])
        self.turn=0
        while(True):
            self.Play(CurrentPlayer)
            self.turn+=1
            if self.Players[CurrentPlayer].hand.checkMelds()==True:
                break
            if CurrentPlayer==0:
                CurrentPlayer=1
            elif CurrentPlayer==1:
                CurrentPlayer=0
            print("Turn:",self.turn)

    
    def Play(self, CurrentPlayer):
        print(int(CurrentPlayer+1), "\'s turn:")
            
        print("Hand:", self.Players[CurrentPlayer].hand)
        print()
        print("Where do you want to?\nEnter \n'D' to draw from Deck \n'P' to draw from discard pile")
        
        loc=input()
        if loc=='D':
            self.Players[CurrentPlayer].hand.draw(self.deck.draw())
        elif loc=='P':
            self.Players[CurrentPlayer].hand.draw(self.discardPile.draw())
        print("index: ", "".join([str(x)+"   " for x in range(0, len(self.Players[CurrentPlayer].hand.cards))]))
        print("Hand:", self.Players[CurrentPlayer].hand)
        print("enter index of card to disard:")
        ind=int(input())
        self.discardPile.discard(self.Players[CurrentPlayer].hand.discard(ind))
        print("Hand:", self.Players[CurrentPlayer].hand)
        

class Player:
    def __init__(self):
        self.hand = Hand()
    

class BasicAgent(Player):
    pass

class AdvancedAgent(Player):
    pass


if __name__ == "__main__":
    GameMgr(123)