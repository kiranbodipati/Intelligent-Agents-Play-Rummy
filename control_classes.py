from entity_classes import *
import numpy as np
import random

class GameMgr:
    def __init__(self, seed=None, gameMode="user"):
        self.deck = Deck()
        self.discardPile = DiscardPile()
        # self.Player1 = Player()
        # self.Player2 = Player()
        # initializes game state
        if gameMode == "agents":
            self.Players = [BasicAgent(), AdvancedAgent()]
        else:
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
                print("Player", CurrentPlayer+1, "wins!")
                break
            CurrentPlayer = 1 - CurrentPlayer  # switches between 0 and 1
            print("Turn:",self.turn)

    
    def Play(self, CurrentPlayer):
        print(int(CurrentPlayer+1), "\'s turn:")
        print("Hand:", self.Players[CurrentPlayer].hand)
        print(self.discardPile)
        print()
        print("Joker:", self.deck.joker)
        print()
        print("Where do you want to?\nEnter \n'D' to draw from Deck \n'P' to draw from discard pile")
        
        openCard = self.discardPile.cards[-1]
        while True:
            try:
                loc = self.Players[CurrentPlayer].getPickupChoice(openCard)
                if loc=='D':
                    if self.Players[1-CurrentPlayer].isObserving:
                        self.Players[1-CurrentPlayer].opponentPickChoice(openCard, False)
                    self.Players[CurrentPlayer].hand.draw(self.deck.draw())  # assumes the agent does not pick up and discard the open card, remember to test later
                elif loc=='P':
                    if self.Players[1-CurrentPlayer].isObserving:
                        self.Players[1-CurrentPlayer].opponentPickChoice(openCard, True)
                    self.Players[CurrentPlayer].hand.draw(self.discardPile.draw())
                else:
                    raise ValueError
                break
            except ValueError:
                print("Error - incorrect input, try again:")
                continue
        print("index: ", "".join([str(x)+"     " for x in range(0, len(self.Players[CurrentPlayer].hand.cards))]))
        print("Hand:", self.Players[CurrentPlayer].hand)
        print("Enter index of card to disard:")
        while True:
            try:
                ind=int(self.Players[CurrentPlayer].getDiscardChoice())
                self.discardPile.discard(self.Players[CurrentPlayer].hand.discard(ind))
                break
            except:
                print("Error - invalid choice, try again:")
                continue
        print("Hand:", self.Players[CurrentPlayer].hand)
        

class Player:  # by default, it's a real user. Agents inherit from this class.
    def __init__(self):
        self.hand = Hand()
        self.melds = []
        self.chances = []
    
    def getPickupChoice(self, openCard):
        print("Top of discard pile:", openCard)
        return input()
    
    def getDiscardChoice(self):
        return input()
    
    def calculateMeldsAndChances(self):  # populates melds and chances without modifying hand
        # TODO: needs to be written by Abhishek
        pass

    def calculatePickup(self, openCard):  # same logic for both agents so I'm coding it here. Not used by user.
        # TODO: complete this function
        pass

    def isObserving(self):  # info is passed to player if it is "observing", true for only advanced agent
        return False
    
    # dummy function for inheritance purposes (used by AdvancedAgent)
    def opponentPickChoice(self, openCard, action):
        pass

    # dummy function for inheritance purposes (used by AdvancedAgent)
    def opponentDiscards(self, openCard):
        pass
    

class BasicAgent(Player):
    
    def getPickupChoice(self, openCard):
        return self.calculatePickup(openCard)

class AdvancedAgent(Player):  # TODO: override getDiscardChoice()
    def __init__(self):
        super().__init__()
        self.heatmap = np.zeros((4, 13))  # keeps track of the cards the opponent needs

    def getPickupChoice(self, openCard):
        return self.calculatePickup(openCard)
    
    def isObserving(self):
        return True
    
    def opponentPickChoice(self, openCard, action):  # action is boolean for whether opponent picked up open card
        # TODO: update heatmap
        pass

    def opponentDiscards(self, openCard):
        # TODO: update heatmap
        pass


if __name__ == "__main__":
    GameMgr(123)