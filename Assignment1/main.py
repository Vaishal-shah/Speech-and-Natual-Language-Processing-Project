import decision
from decision import Node
import csv

with open ('test.txt') as f:
	content = f.readlines()
content = [x.strip() for x in content]

f.close()

f = open('testoutput.txt', 'w')
writer = csv.writer(open('testoutput.csv' , 'w'), delimiter = ',')
out = ["Id", "Prediction"]
writer.writerow(out)
decision.loadtrees()
score = 0
sno = 1
for x in content:
	solution = x
	maskedWord = ""
	for i in range(len(x)):
		maskedWord+='_'
	decision.initializeRoot(maskedWord)
	wrongGuess = 0
	guesses = []
	
	while 1:
		char = decision.getCharacterFromModel(maskedWord, guesses)
		while char in guesses:
			char = decision.getCharacterFromModel(maskedWord, guesses)
		# print(char)
		guesses.append(char)
		if char in solution:
			occurrences = [x for x, v in enumerate(solution) if v == char]
			# print ("Word is : ", solution, " with wrongGuesses = ", wrongGuess)
			# print (char , " in these places: ", occurrences)
			tempMaskedWord = ""
			for i in range(len(maskedWord)):
				if i in occurrences:
					tempMaskedWord+=char
				else:
					tempMaskedWord+=maskedWord[i]
			maskedWord = tempMaskedWord
		else:
			wrongGuess += 1

		if wrongGuess == 8 or '_' not in maskedWord:
			print(solution , " ", maskedWord)
			f.write(solution + "    " + maskedWord + '\n')
			out = [sno, maskedWord]
			writer.writerow(out)
			sno+=1
			for x in maskedWord:
				if(x == '_'):
					score+=1
			break

LevensteinDistance = score / len(content)
print("Levenstein distance = ", LevensteinDistance)
