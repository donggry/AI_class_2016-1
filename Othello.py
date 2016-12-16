# -*- coding: utf-8 -*-
from gamePlay import valid, doMove
from copy import deepcopy
import random

opColor = "W" #상대방 돌색
myColor = "B" #내 돌색
count=1 #내가 두는 횟수

def allPossibleMoves(cboard, color): #현재 내가 둘 수 있는 곳 들의 리스트
    moves = []
    for i in range(8):
        for j in range(8):
            if valid(cboard, color, (i, j)):
                moves.append((i, j))
    return moves


def evaluationfuntion(board):#evaluation 함수
    point = 0

    for i in range(8):#기본적인 오델로 기보를 분석해서 점수를 매기는 단계,가장자리 그전가장자리등등 세분화하여 점수를 냄
        for j in range(8):
            state = board[i][j]
            if i >= 2 and i <= 5 and j >= 2 and j <= 5:
                if state == ".":
                    point = point + 0.5

                elif state == myColor:
                    point = point + 2

                else:
                    if (j == 2 and (i == 2 or i == 5)) or (j == 5 and (i == 2 or i == 5)):
                        point = point - 1

            elif i == 1 or i == 6 or (i == 2 and (j == 1 or j == 6)) or (i == 3 and (j == 1 or j == 6)) or (
                    i == 4 and (j == 1 or j == 6)) or (i == 5 and (j == 1 or j == 6)):
                if state == ".":
                    point = point + 0.5

                elif state == myColor:
                    if ((i == 6 or i == 1) and j == 1) or ((i == 6 or i == 1) and j == 6):
                        point = point - 3
                    else:
                        point = point - 1
                elif state == opColor:
                    if i == 1 and j == 1:
                        if board[0][0] == ".":
                            if board[2][2] == myColor:
                                point = point + 3
                            elif board[2][2] == opColor:
                                if board[3][3] == myColor:
                                    point = point + 4
                                elif board[4][4] == myColor:
                                    point = point + 4.5
                                elif board[5][5] == myColor:
                                    point = point + 5
                                elif board[6][6] == myColor:
                                    point = point + 6
                        else:
                            point = point + 2
                    if i == 1 and j == 6:
                        if board[7][7] == ".":
                            if board[2][5] == myColor:
                                point = point + 3
                            elif board[2][5] == opColor:
                                if board[3][4] == myColor:
                                    point = point + 4
                                elif board[4][3] == myColor:
                                    point = point + 4.5
                                elif board[5][2] == myColor:
                                    point = point + 5
                                elif board[6][1] == myColor:
                                    point = point + 6

                        else:
                            point = point + 2
                    if i == 6 and j == 1:
                        if board[7][0] == ".":
                            if board[5][2] == myColor:
                                point = point + 3
                            elif board[5][2] == opColor:
                                if board[4][3] == myColor:
                                    point = point + 4
                                elif board[3][4] == myColor:
                                    point = point + 4.5
                                elif board[2][5] == myColor:
                                    point = point + 5
                                elif board[1][6] == myColor:
                                    point = point + 6

                        else:
                            point = point + 2
                    if i == 6 and j == 6:
                        if board[7][7] == ".":
                            if board[5][5] == myColor:
                                point = point + 3
                            elif board[5][5] == opColor:
                                if board[4][4] == myColor:
                                    point = point + 4
                                elif board[3][3] == myColor:
                                    point = point + 4.5
                                elif board[2][2] == myColor:
                                    point = point + 5
                                elif board[1][1] == myColor:
                                    point = point + 6

                        else:
                            point = point + 2

                    if i == 1 and j >= 2 and j <= 5:
                        if board[i - 1][j] == ".":
                            if board[i + 1][j] == myColor:
                                point = point + 3
                            elif board[i + 1][j] == opColor:
                                if board[i + 2][j] == myColor:
                                    point = point + 4

                        else:
                            point = point + 2
                    if i == 6 and j >= 2 and j <= 5:
                        if board[i + 1][j] == ".":
                            if board[i - 1][j] == myColor:
                                point = point + 3
                            elif board[i - 1][j] == opColor:
                                if board[i - 2][j] == myColor:
                                    point = point + 4

                        else:
                            point = point + 2
                    if j == 1 and i >= 2 and i <= 5:
                        if board[i][j - 1] == ".":
                            if board[i][j + 1] == myColor:
                                point = point + 3
                            elif board[i][j + 1] == opColor:
                                if board[i][j + 2] == myColor:
                                    point = point + 4

                        else:
                            point = point + 2
                    if j == 6 and i >= 2 and i <= 5:
                        if board[i][j + 1] == ".":
                            if board[i][j - 1] == myColor:
                                point = point + 3
                            elif board[i][j - 1] == opColor:
                                if board[i][j - 2] == myColor:
                                    point = point + 4

                        else:
                            point = point + 2

            else:
                if state == myColor:
                    if (j == 0 and (i == 0 or i == 7)) or (j == 7 and (i == 0 or i == 7)):
                        point = point + 10
                    else:
                        point = point + 5
                elif state == ".":
                    point = point + 0.5

    if board[0][0] == "." and board[1][0] == myColor:
        point = point - 6
    if board[0][0] == "." and board[1][1] == myColor:
        point = point - 6
    if board[0][0] == "." and board[0][1] == myColor:
        point = point - 6
    if board[7][0] == "." and board[6][0] == myColor:
        point = point - 6
    if board[7][0] == "." and board[6][1] == myColor:
        point = point - 6
    if board[7][0] == "." and board[7][1] == myColor:
        point = point - 6
    if board[0][7] == "." and board[0][6] == myColor:
        point = point - 6
    if board[0][7] == "." and board[1][6] == myColor:
        point = point - 6
    if board[0][7] == "." and board[1][7] == myColor:
        point = point - 6
    if board[7][7] == "." and board[6][6] == myColor:
        point = point - 6
    if board[7][7] == "." and board[6][7] == myColor:
        point = point - 6
    if board[7][7] == "." and board[7][6] == myColor:
        point = point - 6

    point = point + len(allPossibleMoves(deepcopy(board), myColor)) - len(allPossibleMoves(deepcopy(board), opColor))
    return point


def changeB(cboard, Color, NextMove):#그수를 뒀다면 뒤집어지는 모든 상황들을 반영시키기

    changeB = deepcopy(cboard)
    doMove(changeB, Color, NextMove)
    return changeB



def alphabeta(cboard, MaxDepth, CurrentDepth, Color,alpha,beta,maximizingPlayer):#알파베타프루닝 알고리즘
     #강의록의 알고리즘을 이용
    cmove = "pass"
    values = []
    moves = []
    states = []
    moves.append(cmove)
    states.append(cboard)
    actions = allPossibleMoves(cboard, Color)
    if CurrentDepth == MaxDepth or len(actions) == 0: #리프노드에 도착하여 평가함수의 값을 받아와야한다.
        return evaluationfuntion(cboard), cmove
    else:
        if maximizingPlayer:
            Value = float("-inf")
            values.append(Value)
            actions = allPossibleMoves(cboard, Color)
            for move in actions:
                orignalBoard = deepcopy(cboard)
                changedBoard = changeB(orignalBoard, Color, move)
                minColor = "B" if Color == "W" else "W"
                newValue, newMove = alphabeta(changedBoard, MaxDepth, CurrentDepth + 1, minColor, alpha, beta, False)
                values.append(newValue)
                moves.append(move)
                states.append(changedBoard)

                if newValue >= beta:
                    return newValue, move

                alpha = alpha if (alpha > newValue) else newValue  # MAX(alpha, newValue)

            if len(values) > 0:
                Value = max(values)
                index = values.index(Value)
                cmove = moves[index]

            if Value == float("-inf"):
                cmove = "pass"
            return Value, cmove
        else:
            Value = float("inf")
            values.append(Value)
            actions = allPossibleMoves(cboard, Color)
            for move in actions:
                orignalBoard = deepcopy(cboard)
                changedBoard = changeB(orignalBoard, Color, move)
                maxColor = "B" if Color == "W" else "W"
                newValue, newMove = alphabeta(changedBoard, MaxDepth, CurrentDepth + 1, maxColor, alpha, beta, True)

                values.append(newValue)
                moves.append(move)
                states.append(changedBoard)

                if newValue <= alpha:
                    return newValue, move

                beta = beta if (beta < newValue) else newValue  # MIN(beta,newValue)

            if len(values) > 0:
                Value = min(values)
                index = values.index(Value)
                cmove = moves[index]

            if Value == float("inf"):
                cmove = "pass"
            return Value, cmove



def nextMove(board, color, time): #다음에 둘 수를 찾아내는 실제 함수
    #2번째 수는 고정적으로 무조건 지는 상황을 피하기 위해 고정적으로 수를 선택
    global opColor
    global myColor
    global count  # 전체 게임을 내가 두는 횟수
    myColor = color
    opColor = "W" if (color == "B") else "B"
    alpha = float("-inf")
    beta = float("inf")
    if count==1:
        if myColor=="B":
            count = count + 1
            return (3,2)
        else:
            if board[2][3]=="B":
                count = count + 1
                randnum=random.randint(2,4)
                if randnum==2:
                    return (2,2)
                else:
                    return(2,4)
            if board[3][2]=="B":
                count = count + 1
                return (2,2)
            if board[4][5]=="B":
                count = count + 1
                randnum = random.randint(3,5)
                if randnum == 3:
                    return (5,3)
                else:
                    return (5,5)
            if board[5][4]=="B":
                count = count + 1
                randnum = random.randint(3, 5)
                if randnum == 3:
                    return (5, 3)
                else:
                    return (5, 5)
    elif count==2 :

        if myColor=="W" :
            if board[2][2]=="W" and board[3][2]=="B" and board[3][3]=="W" and board[4][5]=="B" and board[4][3]=="B" and board[3][4]=="B" and board[4][4]=="B":
                count = count + 1
                return (3,1)
            else:
                best_move = alphabeta(board, 1, 0, color, alpha, beta, True)
        else:
            if board[2][2] == "W" and board[3][2] == "B" and board[4][4] == "W" and board[3][3]=="W" and board[3][4]=="B" and board[4][3]=="B":
                count = count + 1
                randnum = random.randint(4, 5)
                if randnum == 4:
                    return (4,5)
                else:
                    return (5,4)
            #if board[2][4]=="W":
             #   count=count+1
              #  return (4,5)
            #if board[4][2]=="W":
             #   count=count+1
              #  return (5,4)
            else:
                best_move = alphabeta(board, 1, 0, color, alpha, beta, True)
    elif count>=3 and count<=10:
        best_move = alphabeta(board, 1, 0, color, alpha, beta, True)
    elif count>=11 and count <=15:
        best_move = alphabeta(board, 2, 0, color, alpha, beta, True)
    elif count>=16 and count<=20:
        best_move = alphabeta(board, 3, 0, color, alpha, beta, True)
    else:
        best_move = alphabeta(board, 4, 0, color, alpha, beta, True)
    count = count + 1
    return best_move[1] #(2,3)이런 형식으로 반환



