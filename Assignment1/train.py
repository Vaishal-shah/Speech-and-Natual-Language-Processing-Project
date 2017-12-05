import decision
import collections
import pickle
alpha = {'#','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','!'}

with open('train.txt') as f:
	content = f.readlines()
content = [x.strip() for x in content]
cont = []
for x in content:
	x = x.lower()
	flag = 0 
	for letter in x:
		 if letter not in alpha :
		 	flag = 1
	if flag == 0:
		cont.append(x)	 	
f.close()

two_gram = {}
for kk in alpha:
 	two_gram[kk] = {}

for kk in alpha:
 	for ky in alpha:
 		two_gram[kk][ky] = 0

three_gram = {}
for kk in alpha:
 	three_gram[kk] = {}
 	for ky in alpha:
 		three_gram[kk][ky] = {}
for kk in alpha:
 	for ky in alpha:
 		for kz in alpha:
 			three_gram[kk][ky][kz] = 0

four_gram = {}
for kk in alpha:
 	four_gram[kk] = {}
 	for ky in alpha:
 		four_gram[kk][ky] = {}
 		for kz in alpha:
 			four_gram[kk][ky][kz] = {}
for kk in alpha:
 	for ky in alpha:
 		for kz in alpha:
 			for kp in alpha:
 				four_gram[kk][ky][kz][kp] = 0

five_gram = {}
for kk in alpha:
 	five_gram[kk] = {}
 	for ky in alpha:
 		five_gram[kk][ky] = {}
 		for kz in alpha:
			five_gram[kk][ky][kz] = {}
 			for kp in alpha:
				five_gram[kk][ky][kz][kp] = {}
for kk in alpha:
	for ky in alpha:
 		for kz in alpha:
 			for kp in alpha:
 				for kq in alpha:
 					five_gram[kk][ky][kz][kp][kq] = 0

# six_gram = {}
# for kk in alpha:
# 	six_gram[kk] = {}
# 	for ky in alpha:
# 		six_gram[kk][ky] = {}
# 		for kz in alpha:
# 			six_gram[kk][ky][kz] = {}
# 			for kp in alpha:
# 				six_gram[kk][ky][kz][kp] = {}
# 				for kr in alpha:
# 					six_gram[kk][ky][kz][kp][kr]={}
# for kk in alpha:
# 	for ky in alpha:
# 		for kz in alpha:
# 			for kp in alpha:
# 				for kq in alpha:
# 					for kr in alpha:
# 						#print "hi"
# 						six_gram[kk][ky][kz][kp][kq][kr] = 0


for x in cont:
	x = x.lower()
	x = "#"+x+"!"
	print x
	
	this =	[ x[i:i+2] for i in range(len(x) - 1) ]
	print this
	for grp in this:
		chars = list(grp)
	 	two_gram[chars[0]][chars[1]] = two_gram[chars[0]][chars[1]] + 1 

	this =	[ x[i:i+3] for i in range(len(x) - 2) ]
	print this
	for grp in this:
 		chars = list(grp)
 		three_gram[chars[0]][chars[1]][chars[2]] = three_gram[chars[0]][chars[1]][chars[2]] + 1 
	 
	this =	[ x[i:i+4] for i in range(len(x) - 3) ]
	print this
	for grp in this:
	 	chars = list(grp)
	 	four_gram[chars[0]][chars[1]][chars[2]][chars[3]] = four_gram[chars[0]][chars[1]][chars[2]][chars[3]] + 1 

	this =	[ x[i:i+5] for i in range(len(x) - 4) ]
	print this
	for grp in this:
	 	chars = list(grp)
	 	five_gram[chars[0]][chars[1]][chars[2]][chars[3]][chars[4]] = five_gram[chars[0]][chars[1]][chars[2]][chars[3]][chars[4]] + 1 	

	# this =	[ x[i:i+6] for i in range(len(x) - 5) ]
	# print this
	# for grp in this:
	# 	chars = list(grp)
	# 	six_gram[chars[0]][chars[1]][chars[2]][chars[3]][chars[4]][chars[5]] = six_gram[chars[0]][chars[1]][chars[2]][chars[3]][chars[4]][chars[5]] + 1 	

# print "TWO"
# print two_gram
# print "THREE"
# print three_gram
# print "FOUR"
# print four_gram


with open("2gramDict.pkl", "wb") as myFile:
    pickle.dump(two_gram, myFile, protocol=2)
with open("3gramDict.pkl", "wb") as myFile:
    pickle.dump(three_gram, myFile, protocol=2)
with open("4gramDict.pkl", "wb") as myFile:
    pickle.dump(four_gram, myFile, protocol=2)
with open("5gramDict.pkl", "wb" ) as myFile:
    pickle.dump(five_gram, myFile, protocol=2)
# with open("6gramDict.pkl", "wb") as myFile:
#     pickle.dump(six_gram, myFile, protocol=2)
#to read the saved dictionary
# with open("mySavedDict.txt", "rb") as myFile:
#     myNewPulledInDictionary = pickle.load(myFile)



# with open('train.txt') as f:
# 	content = f.readlines()

# content = [x.strip() for x in content]
# print(len(content))

# f.close()

# arr=[2,3,4,5,6,7,8,9,10,11]
# for i in arr:
# 	f6 = open('train'+str(i)+'.txt', 'w')
# 	count=0
# 	for x in content:
# 		if(len(x) == i):
# 			count = count+1
# 			f6.write(x + '\n')
# 	print i,count		
# 	f6.close()
# f6 = open('train12.txt', 'w')
# for x in content:
# 	if(len(x) >= 12):
# 		f6.write(x + '\n')
# f6.close()


# for i in arr:
# 	decision.makedecision(i)
# decision.makedecision(12)

