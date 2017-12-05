
import pickle
import numpy as np
import random
from util import *


data_length = 316
def train(trainX, trainY):


    epoch = 100
    eta = 0.3
    mini_batch_size = 20
    # training_data = list(zip(trainX, trainY))

    # w1 = [0.5] * 300
    # w2 = [0.5] * 300
    w1 = 2*np.random.random(300)-1
    # print(len(w1[1,:]))
    w2 = 2*np.random.random(300)-1

    b1 = 2*np.random.random(300)-1
    
    
    # print(w1.shape)
    # print(w2.shape)
    # print(b1.shape)
    # print(b2)
    training_data = list(zip(trainX, trainY))
    global training_length
    training_length = len(trainX)
    
    mini_batches = [ training_data[k:k+mini_batch_size] for k in range(0, len(trainX), mini_batch_size)]
    
    # for i in range (epoch):
    	# print(mini_batch_size)

    for i in range (epoch):
        loss=0
        for mini_batch in mini_batches:

            #updating the weights
            del_w1 = np.zeros(300)
            del_w2 = np.zeros(300)
            del_b1 = np.zeros(300)

            for x,y in mini_batch:
                a=np.multiply(w1,x[0])
                c=np.multiply(w2,x[1])
                a=np.add(a,c)
                out=np.tanh(np.add(a,b1))
                err=np.multiply(out-y,1-np.multiply(out,out))
                f=out-y
                loss+=0.5*np.dot(f,f)
                del_w1 += np.multiply(err,x[0])
                del_w2 += np.multiply(err,x[1])
                del_b1 +=err

            # print ((eta/mini_batch_size)*del_w1)
            w1 = w1 - (eta/mini_batch_size)*del_w1
            w2 = w2 - (eta/mini_batch_size)*del_w2
            b1 = b1 - (eta/mini_batch_size)*del_b1
            # print "in "
    	
        # print w1
        # print w2
        # print str(i)+"  loss= "+str(loss)
    with open('param3.pkl','wb') as f:
        pickle.dump([w1,w2,b1],f)
    


def test(testX,testY):

    print("Test started")
    w1,w2,b1=pickle.load(open('param3.pkl','rb'))
    
    test_data = list(zip(testX, testY))
    sum1=0
    loss=0
    for x,y in test_data:
        a=np.multiply(w1,x[0])
        c=np.multiply(w2,x[1])
        a=np.add(a,c)
        out=np.tanh(np.add(a,b1))
        word=getOutput(out,  (x[0], x[1]))
        initialwords = [getClosest(x[0]), getClosest(x[1])]
        actualword=getClosest(y)
        f=out-y
        loss+=0.5*np.dot(f,f)
        # print word + "  "+actualword
        if word==actualword:
            sum1 +=1
        print(initialwords , '=' , actualword, word)
    print(sum1, len(testX))
    print ("Accuracy = ", sum1*1.0/len(testX))
    print ("Test done")
    

X=pickle.load(open('data_vec_in.pkl','rb'))
Y=pickle.load(open('data_vec_out.pkl','rb'))
p=int(data_length *0.8)
# print p
train(X[:p],Y[:p])
test(X[p:],Y[p:])
# test(X[:p],Y[:p])

