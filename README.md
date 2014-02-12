Cribalyzer
==========

Python 3.2.3

DISCLAIMER: This is not "pythonic" and there are no coding standards. Just trying to get a working base and then
will go back and fix things up. If you're a Python guru, please feel free to help clean up code. If you're a 
statistician, please feel free to school me on math that might be wrong.

Current functionality:
- Checks every permutation of 4 cards and scores them. Then runs through every remaining card and gives
a probability of possible scores.

Usage:
> python main.py AH,2D,7C,10D,JH,KH
- Need to pass in 6 cards. 


Goal:
- Create engine to advise on which to discard
- Teach probabilities to players
- Add functionality to let user enter in pone/deal, score, etc
- Add functionality to speed up/slow down play in order to maximize chances of winning



A few websites I've used to help guide the project, some items were shamelessly reused :)

https://github.com/maowen/cribbage

http://www.codeproject.com/Articles/15468/Cribbage-Hand-Counting-Library

http://www.math.cornell.edu/~mec/2006-2007/Probability/Cribbagesol.htm
