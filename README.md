### Abstract
Gambling in Indian Rummy has become increasingly popular over the last few years. While researches have been conducted on the impact on society, no significant studies were conducted on the strategies involving the game. We propose a novel study exploring the statistical effectiveness of the card counting strategy on various aspects of the game. A large number of games were simulated with the help of Intelligent Agents and the game statistics were obtained. Statistical tests were conducted on the data to obtain further understanding of the results. The study suggests that the card counting strategy does indeed increase the chances of winning in the game. However, we find that there is no significant difference in the points won per game or lost per game by a card counting strategy as compared to a non counting one, implying that the card counting strategy is not significantly risky in comparison to the more basic strategy. Further we found that it takes shorter to complete games involving the advanced agent, which means that it has potential to lead towards larger earnings on the long run. Considering the various advantages of the card counting strategies, it is recommended that a player picks up the card counting strategy before gambling in the game. 

### How to use:
 - install the requirements using the ```requirements.txt``` file. 
 - The default configuration is developed for a single simulation. To run the script:
``` python control_classes.py  ```
 - get help about arguments with 
 ``` python control_classes.py --help ```

 Optional arguments:
  - seed :  ```-seed``` variable used to set the deck of the game. Default is None (ie the deck is randomly shuffled)
  - gameMode: ```-gm``` or ```--gameMode``` to set game mode. p represents player, b represents basic agent, a represents advanced agent. Can be one of: pva, pvb, avb, bvb, ava, pvp
  - verbose: ```-v``` or ```--verbose``` to enable logging on terminal. 0 for no logs, 1 for logging each iteration.

  Example usage:
  ```
  python control_classes.py -seed 1000 -gm pva -v 1 
  ```

  Additionally each time the program is run, the final results of the game is written to resultData.csv
 Edit the main function to run multiple simulations and reproduce the expreiment. The csv sheets of our experiment have already been provided

