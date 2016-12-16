#"""
#-*- coding: utf-8 -*-
import os
import gzip
import numpy as np
from urllib import urlretrieve
np.seterr(all = 'ignore')

def load_mnist_set() :

    def download(filename, source='http://yann.lecun.com/exdb/mnist/'):
        urlretrieve(source + filename, filename)

    def load_mnist_images(filename):
        if not os.path.exists(filename):
            download(filename)
        with gzip.open(filename, 'rb') as f:
            data = np.frombuffer(f.read(), np.uint8, offset=16)
        data = data.reshape(-1, 1, 28, 28)
        return data / np.float32(256)

    def load_mnist_labels(filename):
        if not os.path.exists(filename):
            download(filename)
        with gzip.open(filename, 'rb') as f:
            data = np.frombuffer(f.read(), np.uint8, offset=8)
        return data

    X_train = load_mnist_images('train-images-idx3-ubyte.gz')
    y_train = load_mnist_labels('train-labels-idx1-ubyte.gz')
    X_test = load_mnist_images('t10k-images-idx3-ubyte.gz')
    y_test = load_mnist_labels('t10k-labels-idx1-ubyte.gz')

    return X_train, y_train, X_test, y_test

print("Loading data...")
X_train, y_train, X_test, y_test = load_mnist_set()
print("Loading complete!")

global input,hidden,output,weight1,weight2,errorsum,alpha1,alpha2,y
input = np.zeros(784)
hidden = np.zeros(100)
output = np.zeros(10)
weight1 = np.random.uniform(-1, 1, [100, 784])
weight2 = np.random.uniform(-1, 1, [10, 100])
errorsum = 0;
alpha1 = 0.06
alpha2 = 0.05
y = np.full((10,), -1)

def Sigmoidfunction(arrays):
    s=np.negative(arrays)
    s=np.exp(s)
    s=np.add(1.0, s)
    s=np.divide(1.0, s)
    return s

def DifferentiableS(h):
    return np.multiply(h,(1.0-h))


def FeedForward(parameter):
    global input,hidden,output
    input = parameter.ravel()
    net2=np.dot(weight1, input)
    hidden = Sigmoidfunction(net2)
    net3=np.dot(weight2, hidden)
    output = Sigmoidfunction(net3)

def BackPropagation(parameter,y_train,errsum):
    FeedForward(parameter)
    global y,weight1,weight2
    y.fill(0.0)
    y[y_train] = 1.0
    temp1 = np.zeros(10)
    temp2 = np.zeros(10)
    net3 = np.dot(weight2, hidden)

    for k in range(0,10):
        error = np.subtract(output[k] ,y[k])
        errsum = errsum + np.square(error)/2.0
        weightsum3 = DifferentiableS(Sigmoidfunction(net3[k]))
        temp1[k] = np.multiply(error,weightsum3)
        weight2[k] = weight2[k] - np.multiply(alpha2 , temp1[k]) * hidden
    temp = np.zeros(100)
    for k in range(0, 10):
        temp = temp + np.multiply(temp1[k],weight2[k])
    net2 = np.dot(weight1, input)
    weightsum2 = DifferentiableS(Sigmoidfunction(net2))
    temp2 = np.multiply(temp,weightsum2)
    for j in range(0, 100):
        weight1[j] = weight1[j] - np.multiply(alpha1 ,temp2[j]) * input
    return errsum

for epoch in range(15):
    errorsum = 0
    sum=0
    for i in range(0, 60000):
        sum=sum+BackPropagation( X_train[i][0], y_train[i],errorsum)
    print  "epoch:"
    print(epoch + 1)
    print sum
    print '\n'

success=0
for i in range(0, 10000):
    FeedForward(X_test[i][0])
    print y_test[i], "->",np.argmax(output)
    if(y_test[i]==np.argmax(output)):
        success=success+1
print "percentage!!!!!!!!!!!!!!:"
print (success / 10000.0) * 100
