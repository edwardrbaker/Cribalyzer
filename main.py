# python 3.2.3

import sys, random, collections, itertools, operator

SUITS = ["H", "S", "D", "C"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9 , 10, 10, 10, 10]
val_dict = dict(zip(RANKS, VALUES))

def buildDeck():
	tempDeck = []
	for suit in SUITS:
		for rank in RANKS:
			tempDeck.append( str(rank) + str(suit) )

	return tempDeck

def scoreHand(hand):
	_handRanks = [x[:-1] for x in hand]
	_handSuits = [x[-1:] for x in hand]

	score = 0

	## pairs, trips, quads
	duplicates = {x:y for x, y in collections.Counter(_handRanks).items() if y > 1}
	for v in duplicates:
		if duplicates[v] == 2:
			score = score + 2
		elif duplicates[v] == 3:
			score = score + 6
		elif duplicates[v] == 4:
			score = score + 12

	#print("Score from pairs: "+str(score))

	handCombinations = []
	for i in range(2, 5):
		els = [list(x) for x in itertools.combinations(_handRanks, i)]
		handCombinations.extend(els)

	## 15s
	fifteenScore = 0
	for combo in handCombinations:
		comboScore = 0
		for i in range(0, len(combo)):
			cardValue = val_dict[combo[i]]
			comboScore = comboScore + cardValue

		if comboScore == 15:
			#print("Fifteen for 2: " + str(combo))
			score = score + 2
			fifteenScore = fifteenScore + 2

	#print("Score from 15s: "+str(fifteenScore))

	# flush
	if all(x == _handSuits[0] for x in _handSuits):
		score = score + len(_handSuits)
	elif all(x == _handSuits[0] for x in _handSuits[0:4]):
		score = score + len(_handSuits[0:4])


	# Nob can be calculated here, but I'm not really sure we need that .. yet?

	## runs ... oh god why
	start = len(hand)
	runFound = 0

	while start > 2:
		runCombinations = []
		for i in range(start, start+1):
			els = [list(x) for x in itertools.combinations(_handRanks, i)]
			runCombinations.extend(els)

		for hand in runCombinations:

			localRun = 1
			member = 0
			while member < len(hand) - 1:
				firstCardIndex = RANKS.index(hand[member])
				secondCardIndex = RANKS.index(hand[member + 1])

				member = member + 1

				if secondCardIndex - firstCardIndex != 1:
					localRun = 0
					break


			if localRun == 1:
				score = score + len(hand)
				runFound = 1

		if runFound:
			break

		start = start - 1

	return score

def flipProbability(remainingDeck):
	remainingCards = len(remainingDeck)
	for card in remainingDeck:
		print("Probability of flipping: "+card+": "+str(1/46))

def flipScoring(hand, remainingDeck):
	flipScoreList = []
	flipCardScoreDict = {}

	for card in remainingDeck:
		handLocal = hand[:]
		handLocal.append(card)

		handScore = scoreHand(handLocal)
		flipScoreList.append(handScore)

		if handScore not in flipCardScoreDict:
			flipCardScoreDict[handScore] = [card]
		else:
			flipCardScoreDict[handScore].append(card)

	# key = score, value = probability
	duplicates = {x:y for x, y in collections.Counter(flipScoreList).items() if y > 1}
	x = list(reversed(sorted(duplicates.items(), key=operator.itemgetter(1))))

	return x,flipCardScoreDict


def expectedScore(hand, remainingDeck):
	pass

class Hand():
	score = 0
	cards = []

def main():
	_CARDS_AFTER_DEAL = 46

	if len(sys.argv) <= 1:
		print("You need to use an argument of your cards, bro.")
	else:
		deal = sys.argv[1].split(',')

		if len(deal) < 6 or len(deal) > 6:
			print("Stop screwing around. 6 cards.")
		else:
			## todo: validity of entered deadl (ie; can't have 5 4s or whatever)
			# setup the deck, find out what is left.
			deck = buildDeck()
			remainingDeck = [c for c in deck if c not in deal]

			# take the full deal and split it into hands of 4
			# this is every combination of 4 from a set of 6; range[4,6] (15 differenct combinations)
			# which has the best score?
			dealSets = []
			for i in range(4, 5):
				els = [list(x) for x in itertools.combinations(deal, i)]
				dealSets.extend(els)

			# score hand
			for hand in dealSets:

				handObject = Hand()
				handObject.cards = hand
				handObject.discard = [c for c in deal if c not in hand]
				handObject.score = scoreHand(hand)


				print(handObject.cards, "tossing", handObject.discard, "=", handObject.score)
				print("---------")
				#print( "Score: " + str(handObject.score) )
				print( "Flip Statistics: " )

				x,y = flipScoring(handObject.cards, remainingDeck)

				for k,v in x:
					if k != handObject.score:
						pcnt = float( (v / 46) * 100 )
						print("You have a ", pcnt,"% chance of scoring "+str(k), "(",y[k],")")

				print("\n\n")

			print( handObject )
			
			# discard which two cards (maximum points-in-hand)

if __name__ == '__main__':
    main()

## references
# https://github.com/maowen/cribbage
# http://www.codeproject.com/Articles/15468/Cribbage-Hand-Counting-Library