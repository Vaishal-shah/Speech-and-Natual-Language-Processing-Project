
import string
import operator
import pickle
from itertools import groupby

class Node:
    def __init__(self, val):
        self.l = None
        self.r = None
        self.v = val

class Tree:
    def __init__(self):
        self.root = None

    def getRoot(self):
        return self.root

    def add(self, val):
        if(self.root == None):
            self.root = Node(val)
        else:
            self._add(val, self.root)

    def _add(self, val, node):
        if(val < node.v):
            if(node.l != None):
                self._add(val, node.l)
            else:
                node.l = Node(val)
        else:
            if(node.r != None):
                self._add(val, node.r)
            else:
                node.r = Node(val)

    def find(self, val):
        if(self.root != None):
            return self._find(val, self.root)
        else:
            return None

    def _find(self, val, node):
        if(val == node.v):
            return node
        elif(val < node.v and node.l != None):
            self._find(val, node.l)
        elif(val > node.v and node.r != None):
            self._find(val, node.r)

    def deleteTree(self):
        # garbage collector will do this for us. 
        self.root = None

    def printTree(self):
        if(self.root != None):
            self._printTree(self.root)

    def _printTree(self, node):
        if(node != None):
            self._printTree(node.l)
           # print (str(node.v) + ' ', end='')
            self._printTree(node.r)
# with open('train.txt') as f:
#   content = f.readlines()

# content = [x.strip() for x in content]
# print(len(content))

# f.close()

# f6 = open('train6.txt', 'r+')


# for x in content:
#   if(len(x) == 6):
#       f6.write(x + '\n')


# f6.close()
twogramDict = {}
treedict = {}
tree = Node('')
trees = [Node('')] * 14
words = {}
root = Node('')
alphabet = list(string.ascii_lowercase)
prevMaskedWord = ""
wrongGuesses = 0
def createDecisionTree(content, node, height, lenword):

    if(height == (lenword + 8) or content == []):
        return None
    for a in alphabet:
        words[a] = 0;

    for x in content:
        for a in alphabet:
            if  a in x:
                words[a] += 1
    #words = sorted(words.items(), key=operator.itemgetter(1))
    value = (max(words.items(), key=operator.itemgetter(1))[0])
    node = Node(value)
    print(value)
    presentcontent = []
    notpresentcontent = []

    for x in content:
        if value in x:
            presentcontent.append(x.replace(value, ""))
        else:
            notpresentcontent.append(x)

    node.l = createDecisionTree(presentcontent, node.l, height+1, lenword)
    node.r = createDecisionTree(notpresentcontent, node.r, height+1, lenword)
    return node



def makedecision(i):
    # for i in range(3, 12):
    
    filename = 'train'+str(i)+'.txt'
    pklfile = 'tree' + str(i) + '.pkl'
    with open (filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    print (len(content) )
    global tree 
    tree = Node('')
    tree = createDecisionTree(content, tree, 1, i)
    output = open(pklfile, 'wb')
    pickle.dump(tree, output)
    output.close()


def loadtrees():

    global twogramDict
    global threegramDict
    global fourgramDict
    global fivegramDict
    global sixgramDict
    
    with open("2gramDict.pkl", "rb") as myFile:
        twogramDict = pickle.load(myFile)
    with open("3gramDict.pkl", "rb") as myFile:
        threegramDict = pickle.load(myFile)
    with open("4gramDict.pkl", "rb") as myFile:
        fourgramDict = pickle.load(myFile)
    with open("5gramDict.pkl", "rb") as myFile:
        fivegramDict = pickle.load(myFile)
    # with open("sixgramDict.pkl", "rb") as myFile:
    #     fivegramDict = pickle.load(myFile)
       
 
    global trees
    for i in range(3, 13):
        filename = 'treespicklefile/tree' + str(i) + '.pkl'
        pkl_file = open(filename, 'rb')
        trees[i] = pickle.load(pkl_file)
        pkl_file.close()


#loadtrees()

def initializeRoot(maskedWord):
    global trees
    global root
    global prevMaskedWord
    global wrongGuesses
    length = len(maskedWord)
    if length >= 12 : 
        length = 12
    root = trees[length]
    prevMaskedWord = ""
    wrongGuesses = 0

def UseNgramModel(maskedWord, guesses):
    listofcharacters = []
    listofcharacters2 = []
    maxletter = {}
    probability = {}
    maxProbability=0
    answer = None
    global twogramDict
    global threegramDict
    #print(threegramDict)
    #print(threegramDict['a']['b']['c'])
    tempmaskedword = '#'+maskedWord+'!'

    #x_
    for i in range(0,len(tempmaskedword)-1):
        if tempmaskedword[i]!='_' and tempmaskedword[i+1]=='_':
            maxcount = max(twogramDict[tempmaskedword[i]][x] for x in alphabet if x not in guesses)
            sumcount = 1 + sum(twogramDict[tempmaskedword[i]][x] for x in alphabet)
            if(maxProbability < 2*maxcount / sumcount):
                answer = [ x for x in alphabet if x not in guesses and twogramDict[tempmaskedword[i]][x] == maxcount][0]
                maxProbability = 2*maxcount / sumcount
    #_x
    for i in range(0,len(tempmaskedword)-1):
        if tempmaskedword[i]=='_' and tempmaskedword[i+1]!='_':
            maxcount = max(twogramDict[x][tempmaskedword[i+1]] for x in alphabet if x not in guesses)
            sumcount = 1 + sum(twogramDict[x][tempmaskedword[i+1]] for x in alphabet)
            if(maxProbability < 2*maxcount / sumcount):
                answer = [ x for x in alphabet if x not in guesses and twogramDict[x][tempmaskedword[i+1]] == maxcount][0]
                maxProbability = 2*maxcount / sumcount

    # xy_
    for i in range(0,len(tempmaskedword)-2):
        if tempmaskedword[i]!='_' and tempmaskedword[i+1]!='_' and tempmaskedword[i+2]=='_':
            maxcount = max(threegramDict[tempmaskedword[i]][tempmaskedword[i+1]][x] for x in alphabet if x not in guesses)
            sumcount = 1 + sum(threegramDict[tempmaskedword[i]][tempmaskedword[i+1]][x] for x in alphabet)
            if(maxProbability < 3*maxcount / sumcount):
                answer = [ x for x in alphabet if x not in guesses and threegramDict[tempmaskedword[i]][tempmaskedword[i+1]][x] == maxcount][0]
                maxProbability = 3*maxcount / sumcount
    #x_y
    for i in range(0,len(tempmaskedword)-2):
        if tempmaskedword[i]!='_' and tempmaskedword[i+1]=='_' and tempmaskedword[i+2]!='_':
            maxcount = max(threegramDict[tempmaskedword[i]][x][tempmaskedword[i+2]] for x in alphabet if x not in guesses)
            sumcount = 1 + sum(threegramDict[tempmaskedword[i]][x][tempmaskedword[i+2]] for x in alphabet)
            if(maxProbability < 4*maxcount / sumcount):
                answer = [ x for x in alphabet if x not in guesses and threegramDict[tempmaskedword[i]][x][tempmaskedword[i+2]] == maxcount][0]
                maxProbability = 4*maxcount / sumcount

    #_xy
    for i in range(0,len(tempmaskedword)-2):
        if tempmaskedword[i]=='_' and tempmaskedword[i+1]!='_' and tempmaskedword[i+2]!='_':
            maxcount = max(threegramDict[x][tempmaskedword[i+1]][tempmaskedword[i+2]] for x in alphabet if x not in guesses)
            sumcount = 1 + sum(threegramDict[x][tempmaskedword[i+1]][tempmaskedword[i+2]] for x in alphabet)
            if(maxProbability < 3*maxcount / sumcount):
                answer = [ x for x in alphabet if x not in guesses and threegramDict[x][tempmaskedword[i+1]][tempmaskedword[i+2]] == maxcount][0]
                maxProbability = 3*maxcount / sumcount
    

    #_xyz
    for i in range(0,len(tempmaskedword)-3):
        if tempmaskedword[i]=='_' and tempmaskedword[i+1]!='_' and tempmaskedword[i+2]!='_' and tempmaskedword[i+3]!='_':
            maxcount = max(fourgramDict[x][tempmaskedword[i+1]][tempmaskedword[i+2]][tempmaskedword[i+3]] for x in alphabet if x not in guesses)
            sumcount = 1 + sum(fourgramDict[x][tempmaskedword[i+1]][tempmaskedword[i+2]][tempmaskedword[i+3]] for x in alphabet)
            if(maxProbability < 4*maxcount / sumcount):
                answer = [ x for x in alphabet if x not in guesses and fourgramDict[x][tempmaskedword[i+1]][tempmaskedword[i+2]][tempmaskedword[i+3]] == maxcount][0]
                maxProbability = 4*maxcount / sumcount

    #x_yz
    for i in range(0,len(tempmaskedword)-3):
        if tempmaskedword[i]!='_' and tempmaskedword[i+1]=='_' and tempmaskedword[i+2]!='_' and tempmaskedword[i+3]!='_':
            maxcount = max(fourgramDict[tempmaskedword[i]][x][tempmaskedword[i+2]][tempmaskedword[i+3]] for x in alphabet if x not in guesses)
            sumcount = 1 + sum(fourgramDict[tempmaskedword[i]][x][tempmaskedword[i+2]][tempmaskedword[i+3]] for x in alphabet)
            if(maxProbability < 5*maxcount / sumcount):
                answer = [ x for x in alphabet if x not in guesses and fourgramDict[tempmaskedword[i]][x][tempmaskedword[i+2]][tempmaskedword[i+3]] == maxcount][0]
                maxProbability = 5*maxcount / sumcount

    #xy_z
    for i in range(0,len(tempmaskedword)-3):
        if tempmaskedword[i]!='_' and tempmaskedword[i+1]!='_' and tempmaskedword[i+2]=='_' and tempmaskedword[i+3]!='_':
            maxcount = max(fourgramDict[tempmaskedword[i]][tempmaskedword[i+1]][x][tempmaskedword[i+3]] for x in alphabet if x not in guesses)
            sumcount = 1 + sum(fourgramDict[tempmaskedword[i]][tempmaskedword[i+1]][x][tempmaskedword[i+3]] for x in alphabet)
            if(maxProbability < 5*maxcount / sumcount):
                answer = [ x for x in alphabet if x not in guesses and fourgramDict[tempmaskedword[i]][tempmaskedword[i+1]][x][tempmaskedword[i+3]] == maxcount][0]
                maxProbability = 5*maxcount / sumcount

    #xyz_
    for i in range(0,len(tempmaskedword)-3):
        if tempmaskedword[i]!='_' and tempmaskedword[i+1]!='_' and tempmaskedword[i+2]!='_' and tempmaskedword[i+3]=='_':
            maxcount = max(fourgramDict[tempmaskedword[i]][tempmaskedword[i+1]][tempmaskedword[i+2]][x] for x in alphabet if x not in guesses)
            sumcount = 1 + sum(fourgramDict[tempmaskedword[i]][tempmaskedword[i+1]][tempmaskedword[i+2]][x] for x in alphabet)
            if(maxProbability < 4*maxcount / sumcount):
                answer = [ x for x in alphabet if x not in guesses and fourgramDict[tempmaskedword[i]][tempmaskedword[i+1]][tempmaskedword[i+2]][x] == maxcount][0]
                maxProbability = 4*maxcount / sumcount

    #xyzp_
    for i in range(0,len(tempmaskedword)-4):
        if tempmaskedword[i]!='_' and tempmaskedword[i+1]!='_' and tempmaskedword[i+2]!='_' and tempmaskedword[i+3]!='_' and tempmaskedword[i+4]=='_':
            maxcount = max(fivegramDict[tempmaskedword[i]][tempmaskedword[i+1]][tempmaskedword[i+2]][tempmaskedword[i+3]][x] for x in alphabet if x not in guesses)
            sumcount = 1+sum(fivegramDict[tempmaskedword[i]][tempmaskedword[i+1]][tempmaskedword[i+2]][tempmaskedword[i+3]][x] for x in alphabet)
            if(maxProbability < 5*maxcount / sumcount):
                answer = [ x for x in alphabet if x not in guesses and fivegramDict[tempmaskedword[i]][tempmaskedword[i+1]][tempmaskedword[i+2]][tempmaskedword[i+3]][x] == maxcount][0]
                maxProbability = 5*maxcount / sumcount
    #xyz_p
    for i in range(0,len(tempmaskedword)-4):
        if tempmaskedword[i]!='_' and tempmaskedword[i+1]!='_' and tempmaskedword[i+2]!='_' and tempmaskedword[i+3]=='_' and tempmaskedword[i+4]!='_':
            maxcount = max(fivegramDict[tempmaskedword[i]][tempmaskedword[i+1]][tempmaskedword[i+2]][x][tempmaskedword[i+4]] for x in alphabet if x not in guesses)
            sumcount = 1+sum(fivegramDict[tempmaskedword[i]][tempmaskedword[i+1]][tempmaskedword[i+2]][x][tempmaskedword[i+4]] for x in alphabet)
            if(maxProbability < 6*maxcount / sumcount):
                answer = [ x for x in alphabet if x not in guesses and fivegramDict[tempmaskedword[i]][tempmaskedword[i+1]][tempmaskedword[i+2]][x][tempmaskedword[i+4]] == maxcount][0]
                maxProbability = 6*maxcount / sumcount
    #xy_zp
    for i in range(0,len(tempmaskedword)-4):
        if tempmaskedword[i]!='_' and tempmaskedword[i+1]!='_' and tempmaskedword[i+2]=='_' and tempmaskedword[i+3]!='_' and tempmaskedword[i+4]!='_':
            maxcount = max(fivegramDict[tempmaskedword[i]][tempmaskedword[i+1]][x][tempmaskedword[i+3]][tempmaskedword[i+4]] for x in alphabet if x not in guesses)
            sumcount = 1+sum(fivegramDict[tempmaskedword[i]][tempmaskedword[i+1]][x][tempmaskedword[i+3]][tempmaskedword[i+4]] for x in alphabet)
            if(maxProbability < 6*maxcount / sumcount):
                answer = [ x for x in alphabet if x not in guesses and fivegramDict[tempmaskedword[i]][tempmaskedword[i+1]][x][tempmaskedword[i+3]][tempmaskedword[i+4]] == maxcount][0]
                maxProbability = 6*maxcount / sumcount
    #x_yzp
    for i in range(0,len(tempmaskedword)-4):
        if tempmaskedword[i]!='_' and tempmaskedword[i+1]=='_' and tempmaskedword[i+2]!='_' and tempmaskedword[i+3]!='_' and tempmaskedword[i+4]!='_':
            maxcount = max(fivegramDict[tempmaskedword[i]][x][tempmaskedword[i+2]][tempmaskedword[i+3]][tempmaskedword[i+4]] for x in alphabet if x not in guesses)
            sumcount = 1+sum(fivegramDict[tempmaskedword[i]][x][tempmaskedword[i+2]][tempmaskedword[i+3]][tempmaskedword[i+4]] for x in alphabet)
            if(maxProbability < 6*maxcount / sumcount):
                answer = [ x for x in alphabet if x not in guesses and fivegramDict[tempmaskedword[i]][x][tempmaskedword[i+2]][tempmaskedword[i+3]][tempmaskedword[i+4]] == maxcount][0]
                maxProbability = 6*maxcount / sumcount
    #_xyzp
    for i in range(0,len(tempmaskedword)-4):
        if tempmaskedword[i]=='_' and tempmaskedword[i+1]!='_' and tempmaskedword[i+2]!='_' and tempmaskedword[i+3]!='_' and tempmaskedword[i+4]!='_':
            maxcount = max(fivegramDict[x][tempmaskedword[i+1]][tempmaskedword[i+2]][tempmaskedword[i+3]][tempmaskedword[i+4]] for x in alphabet if x not in guesses)
            sumcount = 1+sum(fivegramDict[x][tempmaskedword[i+1]][tempmaskedword[i+2]][tempmaskedword[i+3]][tempmaskedword[i+4]] for x in alphabet)
            if(maxProbability < 5*maxcount / sumcount):
                answer = [ x for x in alphabet if x not in guesses and fivegramDict[x][tempmaskedword[i+1]][tempmaskedword[i+2]][tempmaskedword[i+3]][tempmaskedword[i+4]] == maxcount][0]
                maxProbability = 5*maxcount / sumcount
    
# 2 Blanks

   #_x_
    # for i in range(0,len(tempmaskedword)-2):
    #     if tempmaskedword[i]=='_' and tempmaskedword[i+1]!='_' and tempmaskedword[i+2]=='_':
    #         localmax = 0
    #         for k1 in alphabet:
    #             for k2 in alphabet:
    #                 if k1 not in guesses and k2 not in guesses:
    #                     ak1k2 = threegramDict[k1][tempmaskedword[i+1]][k2] / float(1 + sum(threegramDict[x][tempmaskedword[i+1]][y] for x,y in zip( alphabet,alphabet) ))  
    #                     if localmax < ak1k2:
    #                         localmax = ak1k2
    #                         ak1 = twogramDict[k1][tempmaskedword[i+1]]/ float(1+ sum(twogramDict[x][tempmaskedword[i+1]] for x in alphabet))
    #                         k2b = twogramDict[tempmaskedword[i+1]][k2]/ float(1+ sum(twogramDict[tempmaskedword[i+1]][x] for x in alphabet))
    #                         if ak1 >= k2b:
    #                             localanswer = k1
    #                         else:
    #                             localanswer = k2
                              

    #         if localmax > maxProbability:
    #             maxProbability = localmax
    #             answer = localanswer 

    #x__y
    # for i in range(0,len(tempmaskedword)-3):
    #     if tempmaskedword[i]!='_' and tempmaskedword[i+1]=='_' and tempmaskedword[i+2]=='_'and tempmaskedword[i+3]!='_':
    #         localmax = 0
    #         for k1 in alphabet:
    #             for k2 in alphabet:
    #                 if k1 not in guesses and k2 not in guesses:
    #                     ak1k2 = fourgramDict[tempmaskedword[i]][k1][k2][tempmaskedword[i+3]] / float(1 + sum(fourgramDict[tempmaskedword[i]][x][y][tempmaskedword[i+3]] for x,y in zip( alphabet,alphabet) ))  
    #                     if localmax < ak1k2:
    #                         localmax = ak1k2
    #                         ak1 = twogramDict[tempmaskedword[i]][k1]/ float(1+ sum(twogramDict[tempmaskedword[i]][x] for x in alphabet))
    #                         k2b = twogramDict[k2][tempmaskedword[i+3]]/ float(1+ sum(twogramDict[x][tempmaskedword[i+3]] for x in alphabet))
    #                         if ak1 >= k2b:
    #                             localanswer = k1
    #                         else:
    #                             localanswer = k2
                              

    #         if localmax > maxProbability:
    #             maxProbability = localmax
    #             answer = localanswer 

#x__yz
    for i in range(0,len(tempmaskedword)-4):
        if tempmaskedword[i]!='_' and tempmaskedword[i+1]=='_' and tempmaskedword[i+2]=='_'and tempmaskedword[i+3]!='_' and tempmaskedword[i+4]!='_':
            localmax = 0
            for k1 in alphabet:
                for k2 in alphabet:
                    if k1 not in guesses and k2 not in guesses:
                        k1k2 = fivegramDict[tempmaskedword[i]][k1][k2][tempmaskedword[i+3]][tempmaskedword[i+4]] / float(1 + sum(fivegramDict[tempmaskedword[i]][x][y][tempmaskedword[i+3]][tempmaskedword[i+4]] for x,y in zip( alphabet,alphabet) ))  
                        if localmax < k1k2:
                            localmax = k1k2
                            ak1 = twogramDict[tempmaskedword[i]][k1]/ float(1+ sum(twogramDict[tempmaskedword[i]][x] for x in alphabet))
                            k2b = twogramDict[k2][tempmaskedword[i+3]]/ float(1+ sum(twogramDict[x][tempmaskedword[i+3]] for x in alphabet))
                            if ak1 >= k2b:
                                localanswer = k1
                            else:
                                localanswer = k2
                              

            if 5*localmax > maxProbability:
                maxProbability = 5*localmax
                answer = localanswer 
    
#xy__z
    for i in range(0,len(tempmaskedword)-4):
        if tempmaskedword[i]!='_' and tempmaskedword[i+1]!='_' and tempmaskedword[i+2]=='_'and tempmaskedword[i+3]=='_' and tempmaskedword[i+4]!='_':
            localmax = 0
            for k1 in alphabet:
                for k2 in alphabet:
                    if k1 not in guesses and k2 not in guesses:
                        k1k2 = fivegramDict[tempmaskedword[i]][tempmaskedword[i+1]][k1][k2][tempmaskedword[i+4]] / float(1 + sum(fivegramDict[tempmaskedword[i]][tempmaskedword[i+1]][x][y][tempmaskedword[i+4]] for x,y in zip( alphabet,alphabet) ))  
                        if localmax < k1k2:
                            localmax = k1k2
                            ak1 = twogramDict[tempmaskedword[i+1]][k1]/ float(1+ sum(twogramDict[tempmaskedword[i+1]][x] for x in alphabet))
                            k2b = twogramDict[k2][tempmaskedword[i+4]]/ float(1+ sum(twogramDict[x][tempmaskedword[i+4]] for x in alphabet))
                            if ak1 >= k2b:
                                localanswer = k1
                            else:
                                localanswer = k2
                              

            if 5*localmax > maxProbability:
                maxProbability = 5*localmax
                answer = localanswer 


#x_y_z
    for i in range(0,len(tempmaskedword)-4):
        if tempmaskedword[i]!='_' and tempmaskedword[i+1]=='_' and tempmaskedword[i+2]!='_'and tempmaskedword[i+3]=='_' and tempmaskedword[i+4]!='_':
            localmax = 0
            for k1 in alphabet:
                for k2 in alphabet:
                    if k1 not in guesses and k2 not in guesses:
                        k1k2 = fivegramDict[tempmaskedword[i]][k1][tempmaskedword[i+2]][k2][tempmaskedword[i+4]] / float(1 + sum(fivegramDict[tempmaskedword[i]][x][tempmaskedword[i+2]][y][tempmaskedword[i+4]] for x,y in zip( alphabet,alphabet) ))  
                        if localmax < k1k2:
                            localmax = k1k2
                            ak1 = threegramDict[tempmaskedword[i]][k1][tempmaskedword[i+2]]/ float(1+ sum(threegramDict[tempmaskedword[i]][x][tempmaskedword[i+2]] for x in alphabet))
                            k2b = threegramDict[tempmaskedword[i+2]][k2][tempmaskedword[i+4]]/ float(1+ sum(threegramDict[tempmaskedword[i+2]][x][tempmaskedword[i+4]] for x in alphabet))
                            if ak1 >= k2b:
                                localanswer = k1
                            else:
                                localanswer = k2
                              

            if 5*localmax > maxProbability:
                maxProbability = 5*localmax
                answer = localanswer 

#x_y_
    # for i in range(0,len(tempmaskedword)-3):
    #     if tempmaskedword[i]!='_' and tempmaskedword[i+1]=='_' and tempmaskedword[i+2]!='_'and tempmaskedword[i+3]=='_':
    #         localmax = 0
    #         for k1 in alphabet:
    #             for k2 in alphabet:
    #                 if k1 not in guesses and k2 not in guesses:
    #                     ak1bk2 = fourgramDict[tempmaskedword[i]][k1][tempmaskedword[i+2]][k2] / float(1 + sum(fourgramDict[tempmaskedword[i]][x][tempmaskedword[i+2]][y] for x,y in zip( alphabet,alphabet) ))  
    #                     if localmax < ak1bk2:
    #                         localmax = ak1bk2
    #                         ak1 = twogramDict[tempmaskedword[i]][k1]/ float(1+ sum(twogramDict[tempmaskedword[i]][x] for x in alphabet))
    #                         k1b = twogramDict[k1][tempmaskedword[i+2]]/ float(1+ sum(twogramDict[x][tempmaskedword[i+2]] for x in alphabet))
    #                         bk2 = twogramDict[tempmaskedword[i+2]][k2]/ float(1+ sum(twogramDict[tempmaskedword[i+2]][x] for x in alphabet))
    #                         if ak1 >= k1b:
    #                             if ak1 >= bk2:
    #                                 localanswer = k1
    #                             else:
    #                                 localanswer = k2    
    #                         else:
    #                             if k1b >= bk2:
    #                                 localanswer = k1
    #                             else:
    #                                 localanswer = k2
                              

    #         if localmax > maxProbability:
    #             maxProbability = localmax
    #             answer = localanswer 

#_xy_
    # for i in range(0,len(tempmaskedword)-3):
    #     if tempmaskedword[i]=='_' and tempmaskedword[i+1]!='_' and tempmaskedword[i+2]!='_'and tempmaskedword[i+3]=='_':
    #         localmax = 0
    #         for k1 in alphabet:
    #             for k2 in alphabet:
    #                 if k1 not in guesses and k2 not in guesses:
    #                     ak1bk2 = fourgramDict[k1][tempmaskedword[i+1]][tempmaskedword[i+2]][k2] / float(1 + sum(fourgramDict[x][tempmaskedword[i+1]][tempmaskedword[i+2]][y] for x,y in zip( alphabet,alphabet) ))  
    #                     if localmax < ak1bk2:
    #                         localmax = ak1bk2
    #                         k1b = threegramDict[k1][tempmaskedword[i+1]][tempmaskedword[i+2]]/ float(1+ sum(threegramDict[x][tempmaskedword[i+1]][tempmaskedword[i+2]] for x in alphabet))
    #                         bk2 = threegramDict[tempmaskedword[i+1]][tempmaskedword[i+2]][k2]/ float(1+ sum(threegramDict[tempmaskedword[i+1]][tempmaskedword[i+2]][x] for x in alphabet))
    #                         if k1b >= bk2:
    #                             localanswer = k1
    #                         else:
    #                             localanswer = k2
                              

    #         if localmax > maxProbability:
    #             maxProbability = localmax
    #             answer = localanswer 


#_xyz_
    # for i in range(0,len(tempmaskedword)-4):
    #     if tempmaskedword[i]=='_' and tempmaskedword[i+1]!='_' and tempmaskedword[i+2]!='_'and tempmaskedword[i+3]!='_' and tempmaskedword[i+4]=='_':
    #         localmax = 0
    #         for k1 in alphabet:
    #             for k2 in alphabet:
    #                 if k1 not in guesses and k2 not in guesses:
    #                     k1k2 = fivegramDict[k1][tempmaskedword[i+1]][tempmaskedword[i+2]][tempmaskedword[i+3]][k2] / float(1 + sum(fivegramDict[x][tempmaskedword[i+1]][tempmaskedword[i+2]][tempmaskedword[i+3]][y] for x,y in zip( alphabet,alphabet) ))  
    #                     if localmax < k1k2:
    #                         localmax = k1k2
    #                         ak1 = fourgramDict[k1][tempmaskedword[i+1]][tempmaskedword[i+2]][tempmaskedword[i+3]]/ float(1+ sum(fourgramDict[x][tempmaskedword[i+1]][tempmaskedword[i+2]][tempmaskedword[i+3]] for x in alphabet))
    #                         k2b = fourgramDict[tempmaskedword[i+1]][tempmaskedword[i+2]][tempmaskedword[i+3]][k2]/ float(1+ sum(fourgramDict[tempmaskedword[i+1]][tempmaskedword[i+2]][tempmaskedword[i+3]][x] for x in alphabet))
    #                         if ak1 >= k2b:
    #                             localanswer = k1
    #                         else:
    #                             localanswer = k2
                              

    #         if localmax > maxProbability:
    #             maxProbability = localmax
    #             answer = localanswer 


    return answer, maxProbability


def getCharacterFromModel(maskedWord, guesses):
    global prevMaskedWord
    global root
    global wrongGuesses
    global alphabet
    if(prevMaskedWord == ""):
        root = root

    elif(maskedWord == prevMaskedWord):
        wrongGuesses+=1
        if(root != None):
            root = root.r
    else:
        if(root != None):
            root = root.l
    prevMaskedWord = maskedWord

    # ### this part is for the continuous _ if greater than 4 or 5
    # continuouslist = [[k, len(list(g))] for k, g in groupby(maskedWord)]
    # count = max(group[1] for group in continuouslist if group[0] == '_')
    # if count >= 5:
    #     if(root != None):
    #         return root.v
    #     else:
    #         answer, maxProbability = UseNgramModel(maskedWord, guesses)
    #         return answer

    if (maskedWord.count('_') <= (len(maskedWord) - 4)) and (wrongGuesses >= 3):
        answer, maxProbability = UseNgramModel(maskedWord, guesses)
        # print(maxProbability)
        return answer
    if(root != None):
        return root.v
    else:
        
        for a in alphabet:
            if a not in guesses:
                return a
