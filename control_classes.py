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
        for player in self.Players:
            player.hand.setJoker(self.deck.joker.value)
            if player.isObserving():
                player.initializeHeatmap(self.deck.joker.value)
            for _ in range(13):
                player.hand.draw(self.deck.draw())
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
                if self.Players[1-CurrentPlayer].isObserving:
                    self.Players[1-CurrentPlayer].opponentDiscards(self.discardPile.cards[-1])
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

    def updateMeldsAndChances(self, card, RemoveFlag=False): # updates melds and chances without modifying hand
        # TODO: needs to be written by Abhishek
        # RemoveFlag: True - remove card, False - add card
        pass

    def calculatePickup(self, openCard):  # same logic for both agents so I'm coding it here. Not used by user.
        # return 'D' or 'P'
        ## Calculate all flags first before picking up....
        flag4carder=0
        for meld in self.melds:  
            if len(meld)>=4:
                flag4carder+=1
        
        flagPureSeq=0
        for meld in self.melds:  
            if meld[0].value!=meld[0].value:
                flagPureSeq+=1
        
        countMelds=len(self.melds)
        countChances=len(self.chances)
        
        #cases for picking up from discard pile
        #priority 1: Check if the card on top of discard pile is a Joker, pickup
        if(openCard.value==-1 or openCard.value==self.hand.rummyJokerVal):
            return 'P'

        #Assume we pickup a card that is not joker. Recalculate the melds and chances, if the recalculated satisfies, we pickup from the pile
        self.updateMeldsAndChances(openCard)

        #priority 2: Check if the card on top of discard pile forms a pure Sequence:
        flagPureSeqUpd=0
        for meld in self.melds:  
            if meld[0].value!=meld[0].value:
                flagPureSeqUpd+=1
        
        if (flagPureSeqUpd>flagPureSeq):
            return "P"

        #priority 3: Check if the card on top of discard pile forms a 4 carder Sequence  
        flag4carderUpd=0
        for meld in self.melds:  
            if len(meld)>=4:
                flag4carderUpd+=1
        
        if (flag4carderUpd>flag4carder):
            return "P"
        #priority 4: Check if there is any new Sequences created
        countMeldsUpd=len(self.melds)
        if (countMeldsUpd>countMelds):
            return "P"
        #priority 5: Check any new chance is created
        countChancesUpd=len(self.chances)
        if (countMeldsUpd>countChances):
            return "P"
        # Else Pickup from Deck(return D). 
        # Remove the card that we picked up from the discard pile
        self.updateMeldsAndChances(openCard, True)
        return "D"
        
        
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
    
    def getDiscardChoice(self):  # TODO: update melds and chances at the end
        useful = [item for sublist in self.melds+self.chances for item in sublist]
        useful = list(set(useful))
        junk = [card for card in self.hand.cards if (card not in useful and card.value != -1 and card.value != self.hand.rummyJokerVal)]

        if len(junk):
            junk.sort(key=lambda x: x.points, reverse=True)
            return self.hand.cards.index(junk[0])  # discards junk card of highest value
        
        # if no junk cards, needs to break chances in following order of priority:
        # 1. 4-carder chance if 4-carder already exists (discard the single card on one side of the gap)
        # 2. same number chance card that isn't in a straight chance, but the other card of the chance is, of highest value
        # 3. same number chance where neither card is in a straight chance, of highest value
        # 4. straight sequence chance with a gap, of highest value
        # 5. highest card not in a sequence

        discardOptions = []

        # -------------------------------------- Priority #1 -----------------------------------------------
        flag4carder = 0
        for meld in self.melds:
            if len(meld) == 4:
                flag4carder = 1
                break
        if flag4carder:
            for chance in self.chances:
                if len(chance) == 3:
                    chanceCopy = sorted(chance, key=lambda x: x.value)
                    # figuring out which of the 3 is alone on one side of the gap in this 4-carder straight chance
                    i = chanceCopy[0].value
                    if chanceCopy[1].value != i+1:
                        discardOptions.append(chanceCopy[0])
                    else:
                        discardOptions.append(chanceCopy[2])
        if len(discardOptions):
            discardOptions = list(set(discardOptions)).sort(key=lambda x: x.points, reverse=True)
            return self.hand.cards.index(discardOptions[0])
        
        # -------------------------------------- Priority #2 -----------------------------------------------
        sameNumChanceCards = []
        straightChanceCards = []
        for chance in self.chances:
            if chance[0].value == chance[1].value:
                sameNumChanceCards.extend(chance)
            else:
                straightChanceCards.extend(chance)
        sameNumChanceCards = list(set(sameNumChanceCards)).sort(key=lambda x: x.value, reverse=True)
        straightChanceCards = list(set(straightChanceCards)).sort(key=lambda x: x.value, reverse=True)

        for card in sameNumChanceCards:
            if card not in straightChanceCards:
                for card2 in sameNumChanceCards:
                    if card2.value == card.value and card != card2:
                        if card2 in straightChanceCards:
                            discardOptions.append(card)
                            break
        if len(discardOptions):
            discardOptions = list(set(discardOptions)).sort(key=lambda x: x.points, reverse=True)
            return self.hand.cards.index(discardOptions[0])
        
        # -------------------------------------- Priority #3 -----------------------------------------------
        discardOptions = sameNumChanceCards.copy()
        if len(discardOptions):
            discardOptions = list(set(discardOptions)).sort(key=lambda x: x.points, reverse=True)
            return self.hand.cards.index(discardOptions[0])
        
        # -------------------------------------- Priority #4 -----------------------------------------------
        for chance in self.chances:
            if len(chance) == 2 and abs(chance[0].value - chance[1].value) in [2, 11, 12]:  # includes AQ and AK as gap chances
                discardOptions.extend(chance)
        if len(discardOptions):
            discardOptions = list(set(discardOptions)).sort(key=lambda x: x.points, reverse=True)
            return self.hand.cards.index(discardOptions[0])
        
        # -------------------------------------- Priority #5 -----------------------------------------------
        discardOptions = straightChanceCards.copy()
        if len(discardOptions):
            discardOptions = list(set(discardOptions)).sort(key=lambda x: x.points, reverse=True)
            return self.hand.cards.index(discardOptions[0])
        
        # ------------------------------------ Error Handling ----------------------------------------------
        # if it got this far, there are no chances, no junk cards, only melds.
        # since there are 14 cards, there's either two melds of 4 cards or one meld with 5+.
        # so, we can remove one card from the end of the longest meld and win regardless.
        # extra error handling - if all lists are empty, just return 0, though it'll probably break anyway.

        try:
            meldCopy = sorted(self.melds, key=lambda x: len(x), reverse=True)
            longestMeld = meldCopy[0]
            longestMeld.sort(key=lambda x: x.value, reverse=True)
            return self.hand.cards.index(longestMeld[0])
        except:
            return 0



class AdvancedAgent(Player):  # TODO: override getDiscardChoice()
    def __init__(self):
        super().__init__()
        self.heatmap = np.zeros((4, 13))  # keeps track of the cards the opponent needs, +ve means opponent needs it more

    def getPickupChoice(self, openCard):
        return self.calculatePickup(openCard)
    
    def isObserving(self):
        return True
    
    def initializeHeatmap(self, jokerVal):
        if jokerVal == -1:  # joker card is rummy joker drawn at start of round
            return
        for i in range(4):
            # setting as large value because agent absolutely cannot throw jokers away. Not np.inf because it's used to track opponent's cards
            self.heatmap[i][jokerVal-1] = 10**5
            self.heatmap[i][jokerVal-1] = 10**5
    
    def opponentPickChoice(self, openCard, action):  # action is boolean for whether opponent picked up open card
        # TODO: update heatmap
        if openCard.value == -1 or openCard.value == self.hand.rummyJokerVal:
            return
        if action:  # opponent picks up open card
            # update heatmap to show that opponent has that card, also increase value of surrounding cards
            # if opponent has nearby card, increase value for that chance more
            self.heatmap[suitDict[openCard.suit]][openCard.value-1] = np.inf

            # horizontal increments
            immLeft = (openCard.value - 2) % 13
            immRight = openCard.value % 13
            skipLeft = (openCard.value - 3) % 13
            skipRight = (openCard.value + 1) % 13
            # when we know opponent has cards on immediate right or immediate left, increase value of first unknown card on left and right
            if self.heatmap[suitDict[openCard.suit]][immLeft] == np.inf or self.heatmap[suitDict[openCard.suit]][immRight] == np.inf:
                k = immLeft
                while k>=0:
                    if self.heatmap[suitDict[openCard.suit]][k] != np.inf:
                        self.heatmap[suitDict[openCard.suit]][k] += 50
                        break
                    k -= 1
                k = immRight
                while k<=13:
                    if self.heatmap[suitDict[openCard.suit]][k%13] != np.inf:
                        self.heatmap[suitDict[openCard.suit]][k%13] += 50
                        break
                    k += 1
            # when a gap chance is created, increase value for gap by a lot, and surroundings by a bit (4-carder chance)
            elif (immLeft != 0 and self.heatmap[suitDict[openCard.suit]][skipLeft] == np.inf) or (immRight != 0 and self.heatmap[suitDict[openCard.suit]][skipRight] == np.inf):
                if immLeft != 0 and self.heatmap[suitDict[openCard.suit]][skipLeft] == np.inf:
                    self.heatmap[suitDict[openCard.suit]][immLeft] += 50
                    self.heatmap[suitDict[openCard.suit]][immRight] += 5
                    self.heatmap[suitDict[openCard.suit]][(skipLeft-1)%13] += 5
                if immRight != 0 and self.heatmap[suitDict[openCard.suit]][skipRight] == np.inf:
                    self.heatmap[suitDict[openCard.suit]][immRight] += 50
                    self.heatmap[suitDict[openCard.suit]][immLeft] += 5
                    if immRight<=11:
                        self.heatmap[suitDict[openCard.suit]][(skipRight+1)%13] += 5
            # nothing known in two card horizontal surrounding, increment all by a small amount
            else:
                self.heatmap[suitDict[openCard.suit]][immRight] += 2
                self.heatmap[suitDict[openCard.suit]][immLeft] += 2
                if immLeft != 0:
                    self.heatmap[suitDict[openCard.suit]][skipLeft] += 1
                if immRight != 0:
                    self.heatmap[suitDict[openCard.suit]][skipRight] += 1
            

            # Vertical increments
            vert = [(i, openCard.value-1) for i in range(4) if i!=suitDict[openCard.suit]]
            flag = False
            for index in vert:
                if self.heatmap[index[0]][index[1]] == np.inf:
                    flag = True
                    break
            if flag:
                # another card of the same value is known to be in the opponent's hand
                for index in vert:
                    self.heatmap[index[0]][index[1]] += 10
            else:
                for index in vert:
                    self.heatmap[index[0]][index[1]] += 2

        else:  # opponent does not pick up open card
            # update heatmap to show that the card is buried till the end of the deck
            # decrease value of surrounding cards
            # if opponent has a nearby card, increase value of the cards related to that card but unrelated to this one
            self.opponentDiscards(openCard)  # assuming that the opponent not picking up a card is the same as discarding it

    def opponentDiscards(self, openCard):
        # TODO: update heatmap
        # decrease value of surrounding cards
        # if opponent has a nearby card, increase value of the cards related to that card but unrelated to this one
        if self.heatmap[suitDict[openCard.suit]][openCard.value-1] != -np.inf:
            self.heatmap[suitDict[openCard.suit]][openCard.value-1] = -np.inf
        else:  # error handling, prevents a previously ignored/discarded card from counting twice
            return

        immLeft = (openCard.value - 2) % 13
        immRight = openCard.value % 13

        if self.heatmap[suitDict[openCard.suit]][immLeft] == np.inf:
            self.heatmap[suitDict[openCard.suit]][immRight] -= 2
            for k in range(4):
                self.heatmap[k][immLeft] += 10
        else:
            self.heatmap[suitDict[openCard.suit]][immLeft] -= 2
        if self.heatmap[suitDict[openCard.suit]][immRight] == np.inf:
            self.heatmap[suitDict[openCard.suit]][immLeft] -= 2
            for k in range(4):
                self.heatmap[k][immRight] += 10
        else:
            self.heatmap[suitDict[openCard.suit]][immRight] -= 2
        for k in range(4):
            if self.heatmap[k][openCard.value-1] == np.inf:
                self.heatmap[k][immLeft] += 10
                self.heatmap[k][immRight] += 10
            else:
                self.heatmap[k][openCard.value-1] -= 10
    
    # EXACTLY THE SAME AS BASIC AGENT EXCEPT IT DISCARDS BY LOWEST HEATMAP VALUE, NOT HIGHEST CARD VALUE
    def getDiscardChoice(self):  # TODO: update melds and chances at the end
        useful = [item for sublist in self.melds+self.chances for item in sublist]
        useful = list(set(useful))
        junk = [card for card in self.hand.cards if (card not in useful and card.value != -1 and card.value != self.hand.rummyJokerVal)]

        if len(junk):
            junk.sort(key=lambda x: (self.heatmap[suitDict[x.suit]][x.value-1], -x.points), reverse=False)
            return self.hand.cards.index(junk[0])  # discards junk card of highest value
        
        # if no junk cards, needs to break chances in following order of priority:
        # 1. 4-carder chance if 4-carder already exists (discard the single card on one side of the gap)
        # 2. same number chance card that isn't in a straight chance, but the other card of the chance is, of lowest heatmap value
        # 3. same number chance where neither card is in a straight chance, of lowest heatmap value
        # 4. straight sequence chance with a gap, of lowest heatmap value
        # 5. lowest heatmap value card not in a sequence

        discardOptions = []

        # -------------------------------------- Priority #1 -----------------------------------------------
        flag4carder = 0
        for meld in self.melds:
            if len(meld) == 4:
                flag4carder = 1
                break
        if flag4carder:
            for chance in self.chances:
                if len(chance) == 3:
                    chanceCopy = sorted(chance, key=lambda x: x.value)
                    # figuring out which of the 3 is alone on one side of the gap in this 4-carder straight chance
                    i = chanceCopy[0].value
                    if chanceCopy[1].value != i+1:
                        discardOptions.append(chanceCopy[0])
                    else:
                        discardOptions.append(chanceCopy[2])
        if len(discardOptions):
            discardOptions = list(set(discardOptions)).sort(key=lambda x: (self.heatmap[suitDict[x.suit]][x.value-1], -x.points), reverse=False)
            return self.hand.cards.index(discardOptions[0])
        
        # -------------------------------------- Priority #2 -----------------------------------------------
        sameNumChanceCards = []
        straightChanceCards = []
        for chance in self.chances:
            if chance[0].value == chance[1].value:
                sameNumChanceCards.extend(chance)
            else:
                straightChanceCards.extend(chance)
        sameNumChanceCards = list(set(sameNumChanceCards)).sort(key=lambda x: x.value, reverse=True)
        straightChanceCards = list(set(straightChanceCards)).sort(key=lambda x: x.value, reverse=True)

        for card in sameNumChanceCards:
            if card not in straightChanceCards:
                for card2 in sameNumChanceCards:
                    if card2.value == card.value and card != card2:
                        if card2 in straightChanceCards:
                            discardOptions.append(card)
                            break
        if len(discardOptions):
            discardOptions = list(set(discardOptions)).sort(key=lambda x: (self.heatmap[suitDict[x.suit]][x.value-1], -x.points), reverse=False)
            return self.hand.cards.index(discardOptions[0])
        
        # -------------------------------------- Priority #3 -----------------------------------------------
        discardOptions = sameNumChanceCards.copy()
        if len(discardOptions):
            discardOptions = list(set(discardOptions)).sort(key=lambda x: (self.heatmap[suitDict[x.suit]][x.value-1], -x.points), reverse=False)
            return self.hand.cards.index(discardOptions[0])
        
        # -------------------------------------- Priority #4 -----------------------------------------------
        for chance in self.chances:
            if len(chance) == 2 and abs(chance[0].value - chance[1].value) in [2, 11, 12]:  # includes AQ and AK as gap chances
                discardOptions.extend(chance)
        if len(discardOptions):
            discardOptions = list(set(discardOptions)).sort(key=lambda x: (self.heatmap[suitDict[x.suit]][x.value-1], -x.points), reverse=False)
            return self.hand.cards.index(discardOptions[0])
        
        # -------------------------------------- Priority #5 -----------------------------------------------
        discardOptions = straightChanceCards.copy()
        if len(discardOptions):
            discardOptions = list(set(discardOptions)).sort(key=lambda x: (self.heatmap[suitDict[x.suit]][x.value-1], -x.points), reverse=False)
            return self.hand.cards.index(discardOptions[0])
        
        # ------------------------------------ Error Handling ----------------------------------------------
        # if it got this far, there are no chances, no junk cards, only melds.
        # since there are 14 cards, there's either two melds of 4 cards or one meld with 5+.
        # so, we can remove one card from the end of the longest meld and win regardless.
        # extra error handling - if all lists are empty, just return 0, though it'll probably break anyway.

        try:
            meldCopy = sorted(self.melds, key=lambda x: len(x), reverse=True)
            longestMeld = meldCopy[0]
            longestMeld.sort(key=lambda x: x.value, reverse=True)
            return self.hand.cards.index(longestMeld[0])
        except:
            return 0



if __name__ == "__main__":
    GameMgr(123)