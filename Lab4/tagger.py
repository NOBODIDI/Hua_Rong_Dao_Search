import os
import sys
import argparse
from copy import deepcopy
import numpy as np
import time

e = 0.00101

TAGS = ["AJ0", "AJC", "AJS", "AT0", "AV0", "AVP", "AVQ", "CJC", "CJS", "CJT", "CRD",
        "DPS", "DT0", "DTQ", "EX0", "ITJ", "NN0", "NN1", "NN2", "NP0", "ORD", "PNI",
        "PNP", "PNQ", "PNX", "POS", "PRF", "PRP", "PUL", "PUN", "PUQ", "PUR", "TO0",
        "UNC", 'VBB', 'VBD', 'VBG', 'VBI', 'VBN', 'VBZ', 'VDB', 'VDD', 'VDG', 'VDI',
        'VDN', 'VDZ', 'VHB', 'VHD', 'VHG', 'VHI', 'VHN', 'VHZ', 'VM0', 'VVB', 'VVD',
        'VVG', 'VVI', 'VVN', 'VVZ', 'XX0', 'ZZ0', 'AJ0-AV0', 'AJ0-VVN', 'AJ0-VVD',
        'AJ0-NN1', 'AJ0-VVG', 'AVP-PRP', 'AVQ-CJS', 'CJS-PRP', 'CJT-DT0', 'CRD-PNI', 'NN1-NP0', 'NN1-VVB',
        'NN1-VVG', 'NN2-VVZ', 'VVD-VVN', 'AV0-AJ0', 'VVN-AJ0', 'VVD-AJ0', 'NN1-AJ0', 'VVG-AJ0', 'PRP-AVP',
        'CJS-AVQ', 'PRP-CJS', 'DT0-CJT', 'PNI-CRD', 'NP0-NN1', 'VVB-NN1', 'VVG-NN1', 'VVZ-NN2', 'VVN-VVD']


# read the training file
def read_training_files(training_list):
    """

    """
    fileToWord = time.time()

    words = []
    counter = 0
    for file in training_list:
        # print("Reading training file: {}\n".format(file))
        f = open(file)
        lines = f.readlines()
        for l in lines:
            # if counter < 40: # db
            l = str.strip(str(l))
            words.append(l.split(" : "))
            counter += 1
        f.close()
    # print(words)

    # time
    # print("Time to read training files: {}\n".format(time.time() - fileToWord))
    
    return words

def getM_fTag(words):
    """
    
    """
    wordToDict = time.time()

    M = dict()
    fTag = [0] * len(TAGS)
    knownWds = dict()

    for i in range(len(TAGS)): 
        M[TAGS[i]] = dict()
        M[TAGS[i]]["TOT"] = 0
    
    for i in range(len(words)):
        knownWds[words[i][0]] = 0
        POSWord = TAGS.index(words[i][1])
        fTag[POSWord] += 1
        if words[i][0] not in M[TAGS[POSWord]]:
            for POS in TAGS:
                M[POS][words[i][0]] = e
            # M[TAGS[POSWord]][words[i][0]] = 1
        M[TAGS[POSWord]][words[i][0]] += 1
        M[TAGS[POSWord]]["TOT"] += 1
            

    for POS in TAGS:
        for word in M[POS]:
            if M[POS]["TOT"] != 0:
                M[POS][word] = M[POS][word] / M[POS]["TOT"]
    # time 
    # print("Time to create dictionary: {}\n".format(time.time() - wordToDict))
    return M, fTag, knownWds

def getI(words):
    """
    
    """
    wordToInit = time.time()

    wCount = 0
    initArr = [e]*len(TAGS)
    for i in range(len(words)):
        if  (i == 0 or (words[i][0] in [".", "?", "!", "-"]) and i != len(words) - 1):
            # initialWords[words[i + 1][0]] = words[i + 1][1]
            initArr[TAGS.index(words[i + 1][1])] += 1
            wCount += 1
    for i in range(len(TAGS)):
        initArr[i] = initArr[i] / wCount
    
    I = np.zeros((1, len(TAGS)))
    for i in range(len(TAGS)): 
        I[0, i] = max(initArr[i], e)
    # print(I)
    # print(I.shape)
    # print("Time to create initial POS matrix: {}\n".format(time.time() - wordToInit))
    return I

def getT(words):
    """
    
    """
    wordToTrans = time.time()

    tran = [[e for i in range(len(TAGS) + 1)] for j in range(len(TAGS))]
    # count = 0
    for k in range(len(words) - 1):
        # count += 1
        word = words[k][1]
        next_word = words[k + 1][1]
        # if word in TAGS and next_word in TAGS:
        i = TAGS.index(word)
        j = TAGS.index(next_word)
        tran[i][j] += 1
        tran[i][len(TAGS)] += 1 + e * len(TAGS)
    
    T = np.zeros((len(TAGS), len(TAGS)))
    for i in range(len(tran)):
        for j in range(len(tran) - 1):
            tran[i][j] = tran[i][j] / tran[i][len(TAGS)]
            T[i][j] = tran[i][j]
            # if T[i][j] == 0:
            #     print("mark")

    # print(T)
    # print(T.shape)
    # time
    # print("Time to create transition matrix: {}\n".format(time.time() - wordToTrans))

    return T

def getDistTag(fTag, nbWords):
    for i in range(len(fTag)):
        fTag[i] = fTag[i] / nbWords
        # print(fTag[i])
    # print(sum(fTag))
    return fTag


# read the testing file
def read_testing_file(file):
    """
    
    """
    with open(file, 'r') as f:
        testWds = f.read().splitlines()
    E = []
    numWords = 0
    temp = []
    for j in range (len(testWds)): #len(testWds) #2132
        temp.append(testWds[j])
        if testWds[j] in ['.', '?', '!', '-']:
            # numWords += len(temp)
            E.append(deepcopy(temp))
            temp = []            
    # print(numWords)
    return E

def Viterbi(distTag, E, S, I, T, M, knownWds): 
    """
    """
    count = 0
    for t in range(len(E)):
        prob = [[0]* len(TAGS) for x in range(len(E[t]))] 
        prev = [[0]* len(TAGS) for x in range(len(E[t]))]

        p1 = []
        for j in range(len(TAGS)):
            # print(TAGS[j])
            if E[t][0] in M[TAGS[j]]:
                # print(M[TAGS[j]][E[i][0]])
                p1.append(j)

        if len(p1) == 0:
            for j in range(len(TAGS)):
                prob[0][j] = I[j] * distTag[j]
        else: 
            for j in range(len(p1)):
                # print(E[t][0])
                prob[0][p1[j]] = I[p1[j]] * M[TAGS[p1[j]]][E[t][0]]    
                # print(prob[0][p1[j]])

        # print(prob)
        p2 = [[] for x in range(len(E[t]))]
        # print(p2)
        for i in range(1, len(E[t])):
            for k in range(len(TAGS)):
                if E[t][i] in M[TAGS[k]]:
                    # print(E[t][i])
                    # print(k)
                    p2[i].append(k)
        # p2.pop(0)
        # print(p2)
        if len(p2) == 0:
            for i in range(1, len(E[t])):
                for k in range(len(TAGS)):
                    # print('unknown')
                    prob[i][k] = max(prob[i - 1][j] * T[j][k] * distTag[k] for j in range(len(TAGS)))
        else:
            for i in range(1, len(E[t])):
                for k in p2[i]: 
                    # print("k: {}".format(k))
                    x = d = 0
                    for j in p2[i - 1]:
                        # print("j: {}".format(j))
                        # print((prob[i - 1][j] * T[j][k] * M[TAGS[k]][E[t][i]]))
                        # print(E[t][i]) # db
                        if d < (prob[i - 1][j] * T[j][k] * M[TAGS[k]][E[t][i]]):
                            d = prob[i - 1][j] * T[j][k] * M[TAGS[k]][E[t][i]]
                            x = j
                    # print(x)
                    prob[i][k] = prob[i - 1][x] * T[x][k] * M[TAGS[k]][E[t][i]]
                    prev[i][k] = x

                # print() #db
    # print(prob)
    return S

def doViterbi(distTag, sent, I, T, M, knownWds): 
    tagsForSent = []
    prob = np.zeros((len(sent), len(TAGS)))
    prev = np.zeros((len(sent), len(TAGS)))

    for i in range(len(TAGS)):
        if sent[0] in M[TAGS[i]]:
            prob[0,i] = I[0,i] * M[TAGS[i]][sent[0]]
        else:
            prob[0, i] = I[0, i] * (1 / len(TAGS))   
        prev[0, i] = None

    for t in range(1, len(sent)):
        if sent[t] in knownWds:
            for i in range(len(TAGS)):
                m = M[TAGS[i]][sent[t]] if sent[t] in M[TAGS[i]] else ((1 / (len(TAGS)-1)))
                temp = prob[t - 1, :] * T[:, i] * m
                maxP = np.max(temp)
                x = np.argmax(temp)
                prob[t, i] = maxP
                prev[t, i] = x
        else:
            for i in range(len(TAGS)):
                m = distTag[i]
                temp = prob[t - 1, :] * T[:, i] * m
                maxP = np.max(temp)
                x = np.argmax(temp)
                prob[t,i] = maxP
                prev[t,i] = x
        prob[t, :] = prob[t, :] / np.sum(prob[t, :])

    xP = np.argmax(prob[len(sent) - 1, :])
    tagsForSent.append(TAGS[int(xP)])
    for i in range(len(sent) - 1, 0, -1):
        xP = prev[i, int(xP)]
        tagsForSent.append(TAGS[int(xP)])
    tagsForSent.reverse()
    return tagsForSent


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--trainingfiles",
        action="append",
        nargs="+",
        required=True,
        help="The training files."
    )
    parser.add_argument(
        "--testfile",
        type=str,
        required=True,
        help="One test file."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file."
    )
    args = parser.parse_args()

    print("Starting the tagging process.")
    training_list = args.trainingfiles[0]
    print("training files are {}".format(training_list))
    print("test file is {}".format(args.testfile))
    print("output file is {}".format(args.outputfile))
    
    startTime = time.time()

    words = read_training_files(training_list)
    M, fTag, knownWds = getM_fTag(words)
    I = getI(words)
    T = getT(words)
    distTag = getDistTag(fTag, len(words))
    # print(T.shape)
    # print(len(M))
    # print(I.shape)


    # print("Time to learn the model: {} seconds".format(time.time() - startTime))
    startTag = time.time()

    E = read_testing_file(args.testfile)
    S = []

    for sent in E: 
        S.append(doViterbi(distTag, [wd for wd in sent], I, T, M, knownWds))

    outFile = open(args.outputfile, "w")
    for i in range(len(E)):
        for j in range(len(E[i])):
                    outFile.write("{} : {}\n".format(E[i][j], S[i][j]))
    outFile.close()
    
    # for i in range(len(E)):
    #     for j in range(len(E[i])):
    #         print("{} : {}".format(E[i][j], S[i][j]))
    # print("Time to tag the test file: {} seconds".format(time.time() - startTag))

