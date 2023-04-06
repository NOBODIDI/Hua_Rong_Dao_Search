import os
import sys
import argparse
import numpy as np
import time

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
    words = []
    counter = 0

    for file in training_list:
        print("Reading training file: {}".format(file))
        f = open(file)
        lines = f.readlines()
        for l in lines:
            # if counter < 40: # db
            l = str.strip(str(l))
            words.append(l)
            counter += 1

    M = dict()
    for i in range(len(TAGS)): 
        M[TAGS[i]] = dict()
    
    frequencyOfTag = [0] * len(TAGS)
    for i in range(len(words)):
        words[i] = words[i].split(" : ")
        POSWord = TAGS.index(words[i][1])
        frequencyOfTag[POSWord] += 1
        if words[i][0] in M[TAGS[POSWord]]:
            M[TAGS[POSWord]][words[i][0]] += 1
        else:
            M[TAGS[POSWord]][words[i][0]] = 1

    # wordsInPOS = []
    # for i in range(len(M)): 
    #     wordsInPOS.append(len(M[TAGS[i]]))
    # print(wordsInPOS)

    for i in range(len(M)):
        for key in M[TAGS[i]]:
            M[TAGS[i]][key] = M[TAGS[i]][key] / frequencyOfTag[i]

    for i in range(len(frequencyOfTag)):
        frequencyOfTag[i] = frequencyOfTag[i] / len(words)

    initialWords = dict()
    for i in range(len(words)):
        if  i == 0 or (words[i][0] in [".", "?", "!", "-"] and i != len(words) - 1):
            # print(words[i + 1][0])
            # print(words[i + 1][1])
            initialWords[words[i + 1][0]] = words[i + 1][1]

    words = np.array(words) # keep this? 

    I = [None]*len(TAGS)
    for i in range(len(TAGS)):
        I[i] = sum(value == TAGS[i] for value in initialWords.values()) / len(initialWords)
    # print(I)

    T = [[0 for i in range(len(TAGS))] for j in range(len(TAGS))]
    # print(len(T))
    # print(len(T[0]))
    for i in range(len(TAGS)):
        for j in range(len(TAGS)): 
            for k in range(len(words)):
                if words[k][1] == TAGS[i] and k != len(words) - 1 and words[k + 1][1] == TAGS[j]:
                    T[i][j] += 1
    # print (T[19][19])        

    # print(I)
    # print(T)
    # print(M)
    f.close()
    return frequencyOfTag, I, M, T

# read the testing file
def read_testing_file(file):
    """
    
    """
    countWords = 0
    e = []
    f = open(file)
    lines = f.readlines()
    for l in lines:
        if countWords < 47: # db
            l = str.strip(str(l))
            e.append(l)
            countWords += 1
    # print(e)
    temp = []
    numSentences = 0
    
    E = []

    for i in range(len(e)):
        # print(e[i])
        if (i == len(e) - 1 and i != 0): 
            E[numSentences - 1].append(e[i])
        if  i == 0 or (e[i] in ['.', '?', '!', '-'] and i != len(e) - 1):
            if i == 0: j = 0
            else: 
                j = i + 1
                # print(numSentences)
                E[numSentences - 1].append(e[i])

            while e[j] not in ['.', '?', '!', '-'] and j != len(e) - 1:
                # print(j)
                # print(e[j])
                temp.append(e[j])
                j += 1
            E.append(temp)
            numSentences += 1
            temp = []
    # print(E)
    f.close()
    return E



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
    startTime = time.time()

    training_list = args.trainingfiles[0]
    print("training files are {}".format(training_list))
    # read the training files 
    frequencyOfTag, I, M, T = read_training_files(training_list)
    # convert T and I to numpy array? 

    print("test file is {}".format(args.testfile))
    E = read_testing_file(args.testfile)
    # convert E to numpy array? 

    S = [] 
    for i in range(len(E)):
        S.append([])
        for j in range(len(E[i])):
            S[i].append("NP0")     # change when implementing Viterbi
    # print(S)
    # print(len(S))
    # print(len(S[0]) + len(S[1]))

    learningTime = time.time() - startTime
    print("Time to learn the model: {} seconds".format(learningTime))

    # Implement Viterbi algorithm for each sentence in E
    # S = Viterbi(E, S, I, T, M): 

    print("output file is {}".format(args.outputfile))

    outFile = open(args.outputfile, "w")
    for i in range(len(E)):
        for j in range(len(E[i])):
                    outFile.write("{} : {}\n".format(E[i][j], S[i][j]))
    outFile.close()
    # for i in range(len(E)):
    #     for j in range(len(E[i])):
    #         print("{} : {}".format(E[i][j], S[i][j]))
