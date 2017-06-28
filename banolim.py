#-*- coding: utf-8 -*-

import random
import numpy as np
import pandas as pd
np.seterr(all = 'ignore')


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
    input = np.array(parameter)
    #print input
    net2=np.dot(weight1, input)
    hidden = Sigmoidfunction(net2)
    net3=np.dot(weight2, hidden)
    output = Sigmoidfunction(net3)

def BackPropagation(parameter,y_train,errsum):
    FeedForward(parameter) #피드포워드를 먼저 진행하고 그 값을 실제 값과 비교해 에러값을 이용해 백프롭게이션을 진행!
    global y,weight1,weight2
    y.fill(0.0)
    y[y_train] = 1.0
    temp1 = np.zeros(2)
    temp2 = np.zeros(2)
    net3 = np.dot(weight2, hidden)

    for k in range(0,2):
        error = np.subtract(output[k] ,y[k])
        errsum = errsum + np.square(error)/2.0
        weightsum3 = DifferentiableS(Sigmoidfunction(net3[k]))
        temp1[k] = np.multiply(error,weightsum3)
        weight2[k] = weight2[k] - np.multiply(alpha2 , temp1[k]) * hidden
    temp = np.zeros(nodenum)
    for k in range(0,2):
        temp = temp + np.multiply(temp1[k],weight2[k])
    net2 = np.dot(weight1, input)
    weightsum2 = DifferentiableS(Sigmoidfunction(net2))
    temp2 = np.multiply(temp,weightsum2)
    for j in range(0, nodenum):
        weight1[j] = weight1[j] - np.multiply(alpha1 ,temp2[j]) * input
    return errsum


def test(rate_rate):
    success = 0
    dic = {0: {0: 0, 1: 0}, 1: {0: 0, 1: 0}}
    for i in range(0, len(X_test)):

        FeedForward(X_test[i])
        #output에는 [0으로 분류될 가능성값,1로 분류될 가능성 값]이 저장되어 있음 argmax를 이용해서 두 값중 값이 큰 것의 인덱스(0또는1)를 반환해줌!!
        # y_test[i] : 실제 정답 / np.argmax(output): 예측 값
        dic[y_test[i]][np.argmax(output)]=dic[y_test[i]][np.argmax(output)]+1 #여러가지 비율을 구하기 위한 데이터 (재현율 등)
        if(y_test[i]==np.argmax(output)):#정답일 경우
            success=success+1
        else:#틀릴 경우
            print (i)#엑셀 열의 인덱스
            print (y_test[i], "->", np.argmax(output))

            print (X_test[i])#x1~x22까지의 값

    print ("accracy rate")
    print ((success / float(len(X_test))) * 100.0)
    print ("specificity rate")
    print (100.0*dic[0][0]/(dic[0][0]+dic[0][1]))
    print ("sensitivity rate")
    print (100.0*dic[1][1]/(dic[1][0]+dic[1][1]))
    resulttxt = open("resulttxt_average_yes_7580.txt", "a")
    resulttxt.write(str(rate_rate)+","+str(nodenum)+","+str(epoch)+","+str(((success / float(len(X_test))) * 100.0))+","+str(100.0*dic[0][0]/(dic[0][0]+dic[0][1]))+","+str(100.0*dic[1][1]/(dic[1][0]+dic[1][1])))
    resulttxt.write('\n')


if __name__ == "__main__":

    #dataframe_validation = pd.read_csv("testdata.csv")
    dataframe_train = pd.read_csv("train_vali_total.csv")
    meandic = {1: 4.0402105263157893, 2: 4.6472573839662443, 3: 4.2231283981597656, 4: 0.42160571668768387,
               5: 5.756256572029443, 6: 3.4733081126523748, 7: 2.7367755532139095, 8: 5.3248784612132738,
               9: 1.5676017717781059, 10: 3.4347007115948096, 11: 3.5100274435296601, 12: 3.4299302473050095,
               13: 6.466947368421053, 14: 6.4112970711297068, 15: 1.0, 16: 2.9668496621621623, 17: 2.0714285714285716,
               18: 4.3046776232616937, 19: 2.9493029150823826, 20: 1.1614880574931303, 21: 1.3033235170382835,
               22: 5.797804981004643}

    total_x = []
    total_y = []


    # 엑셀에서 값 추출해서 리스트로 만들기 X_train,y_train,X_test,y_test 4개의 리스트 만듬
    for a in dataframe_train.iterrows():
        temp = []
        for i in range(1, 23):
            #temp.append((a[1][i]))
            ###############################################
            # 각 -1 값을 해당 요인의 평균값으로 바꿔주는 부분
            if a[1][i]==-1:
                #temp.append(meandic[i])
            # 만약 반올림 값을 쓰고싶으면 위의 것 대신
                temp.append(int(round(meandic[i])))# 로 변경!!!
            else:
                temp.append((a[1][i]))
            ###############################################
        temp.append(a[1][0])
        total_x.append(temp)
        # total_y.append((a[1][0]))
    rates=[0.65,0.75,0.8]
    for rate in rates:
        nodeepochlist = [[50, 15],[50,30],[75,15],[75,30],[100,15],[100,30],[125,15],[125,30]]  # [[5, 15], [15, 15], [25, 15], [35, 15], [45, 15], [55, 15], [65, 15], [75, 15], [85, 15], [95, 15],
        # [100, 15],
        # [110, 15], [120, 15], [130, 15]]
        for nodeepoch in nodeepochlist:
            for repeat in range(10):
                random.shuffle(total_x)
                t = len(total_x)
                X_train = []
                y_train = []
                X_test = []
                y_test = []
                for count, data in enumerate(total_x):
                    temp = []
                    if count >= int(t *rate):
                        X_test.append(data[0:22])
                        y_test.append(data[22])
                    else:
                        X_train.append(data[0:22])
                        y_train.append(data[22])

                global input, hidden, output, weight1, weight2, errorsum, alpha1, alpha2, y, nodenum, epochnum
                input = np.zeros(22)
                nodenum = nodeepoch[0]
                hidden = np.zeros(nodenum)
                output = np.zeros(2)
                weight1 = np.random.uniform(-1, 1, [nodenum, 22])
                weight2 = np.random.uniform(-1, 1, [2, nodenum])
                errorsum = 0
                alpha1 = 0.06
                alpha2 = 0.05
                y = np.full((2,), -1)
                epochnum = nodeepoch[1]

                for epoch in range(epochnum+1):  # 학습횟수 30번
                    errorsum = 0
                    sum = 0
                    for i in range(0, len(X_train)):  # 학습데이터셋
                        sum = sum + BackPropagation(X_train[i], y_train[i], errorsum)  # 에러의 합을 반환
                    print("epoch:")
                    print(epoch + 1)
                    print (sum)
                    print ('\n')

                test(rate)
