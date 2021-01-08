''' Here I'm trying to apply Markov Chains' concept in order to beat 4 bots achieving 60+% of winning plays
    Unfortunately it's not working well, it does not reach the goal with all bots.
'''
import random

choices = {'R': 0, 'P': 1, 'S': 2}
buildTMatrix = {'RR': 1, 'RP': 1, 'RS': 1, 'PR': 1, 'PP': 1, 'PS': 1, 'SR': 1, 'SP': 1, 'SS': 1}
buildTMatrixL = {'RR': 1, 'RP': 1, 'RS': 1, 'PR': 1, 'PP': 1, 'PS': 1, 'SR': 1, 'SP': 1, 'SS': 1}
buildTMatrixT = {'RR': 1, 'RP': 1, 'RS': 1, 'PR': 1, 'PP': 1, 'PS': 1, 'SR': 1, 'SP': 1, 'SS': 1}

n = 3
m = 3
tMatrix = [[0] * m for i in range(n)]
tMatrixL = [[0] * m for i in range(n)]
tMatrixT = [[0] * m for i in range(n)]
probabilitiesRPS = [1 / 3, 1 / 3, 1 / 3]


def checker(player, computer):
    if player == computer:
        return 'tie'
    elif (player == 'R' and computer == 'S') or (player == 'S' and computer == 'P') or (
            player == 'P' and computer == 'R'):
        return 'win'
    else:
        return 'lose'


def buildTransitionProbabilities(pC, c, winloss):
    global buildTMatrix
    global buildTMatrixL
    global buildTMatrixT

    if winloss == "win":
        for i, x in buildTMatrix.items():
            if ('%s%s' % (pC, c) == i):
                buildTMatrix['%s%s' % (pC, c)] += 1
    elif winloss == "tie":
        for i, x in buildTMatrixT.items():
            if ('%s%s' % (pC, c) == i):
                buildTMatrixT['%s%s' % (pC, c)] += 1
    else:
        for i, x in buildTMatrixL.items():
            if ('%s%s' % (pC, c) == i):
                buildTMatrixL['%s%s' % (pC, c)] += 1

    return buildTransitionMatrix(winloss)


def buildTransitionMatrix(winlosstwo):
    global tMatrix
    global tMatrixL
    global tMatrixT

    if winlosstwo == "win":
        rock = buildTMatrix['RR'] + buildTMatrix['RS'] + buildTMatrix['RP']
        paper = buildTMatrix['PR'] + buildTMatrix['PS'] + buildTMatrix['PP']
        scissors = buildTMatrix['SR'] + buildTMatrix['SS'] + buildTMatrix['SP']
        choi = ['R', 'P', 'S']
        for row_index, row in enumerate(tMatrix):
            for col_index, item in enumerate(row):
                a = int(buildTMatrix['%s%s' % (choi[row_index], choi[col_index])])
                if (row_index == 0):
                    c = a / rock
                elif (row_index == 1):
                    c = a / paper
                else:
                    c = a / scissors
                row[col_index] = float(c)
        return (tMatrix)
    elif winlosstwo == "tie":
        rock = buildTMatrixT['RR'] + buildTMatrixT['RS'] + buildTMatrixT['RP']
        paper = buildTMatrixT['PR'] + buildTMatrixT['PS'] + buildTMatrixT['PP']
        scissors = buildTMatrixT['SR'] + buildTMatrixT['SS'] + buildTMatrixT['SP']
        choi = ['R', 'P', 'S']
        for row_index, row in enumerate(tMatrixT):
            for col_index, item in enumerate(row):
                a = int(buildTMatrixT['%s%s' % (choi[row_index], choi[col_index])])
                if (row_index == 0):
                    c = a / rock
                elif (row_index == 1):
                    c = a / paper
                else:
                    c = a / scissors
                row[col_index] = float(c)
        return (tMatrixT)
    else:
        rock = buildTMatrixL['RR'] + buildTMatrixL['RS'] + buildTMatrixL['RP']
        paper = buildTMatrixL['PR'] + buildTMatrixL['PS'] + buildTMatrixL['PP']
        scissors = buildTMatrixL['SR'] + buildTMatrixL['SS'] + buildTMatrixL['SP']
        choi = ['R', 'P', 'S']
        for row_index, row in enumerate(tMatrixL):
            for col_index, item in enumerate(row):
                a = int(buildTMatrixL['%s%s' % (choi[row_index], choi[col_index])])
                if (row_index == 0):
                    c = a / rock
                elif (row_index == 1):
                    c = a / paper
                else:
                    c = a / scissors
                row[col_index] = float(c)
        return (tMatrixL)


def player(prev_play, opponent_history=[], my_history=[]):
    opponent_history.append(prev_play)

    if len(opponent_history) > 0:
        result = checker(my_history[-1], opponent_history[-1])
        transMatrix = buildTransitionProbabilities(opponent_history[-2], opponent_history[-1], result)
        machineChoice = random.randint(1, 100)
        probabilitiesRPS[0] = transMatrix[choices[opponent_history[-1]]][0]
        probabilitiesRPS[1] = transMatrix[choices[opponent_history[-1]]][1]
        probabilitiesRPS[2] = transMatrix[choices[opponent_history[-1]]][2]
        rangeR = probabilitiesRPS[0] * 100
        rangeP = probabilitiesRPS[1] * 100 + rangeR
        if (machineChoice <= rangeR):
            guess = 'P'
        elif (machineChoice <= rangeP):
            guess = 'S'
        else:
            guess = 'R'
        print(guess)
        my_history.append(guess)
    else:
        guess = "R"
        my_history.append(guess)

    return guess
