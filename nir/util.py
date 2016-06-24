#coding: utf-8

def loadDataSet(filename, split = "::"):
    dataSet = dict()
    file = open(filename, "r")
    for line in file.readlines():
        userID, itemID, rating, timestamp = line.split(split)
        dataSet.setdefault(int(userID), dict())[int(itemID)] = int(rating)
    file.close()
    return dataSet

def loadDataSet2(filename, split = "::"):

    dataSet = []
    trainSet = dict()
    testSet = dict()
    file = open(filename, "r")
    for line in file.readlines():
        userID, itemID, rating = line.split(split)
        dataSet.append((int(userID), int(itemID), int(float(rating))))
    file.close()
    from sklearn.cross_validation import train_test_split
    trainSet1, testSet1 = train_test_split(dataSet, test_size=0.2, random_state=42)
    for line in trainSet1:
        trainSet.setdefault(line[0], dict())[line[1]] = line[2]
    for line in testSet1:
        testSet.setdefault(line[0], dict())[line[1]] = line[2]
    return trainSet, testSet

def recall(trainSet, testSet, recoSet):
    hit = 0
    all = 0
    for userID in trainSet:
        testItems = testSet.get(userID, { })
        recoItems = recoSet.get(userID, { })

        for itemID in recoItems:
            if itemID in testItems:
                hit += 1
        all += len(testItems)
    return 1.0 * hit / all

def precision(trainSet, testSet, recoSet):
    hit = 0
    all = 0
    for userID in trainSet:
        testItems = testSet.get(userID, { })
        recoItems = recoSet.get(userID, { })

        for itemID in recoItems:
            if itemID in testItems:
                hit += 1
        all += len(recoItems)
    return 1.0 * hit / all

def coverage(trainSet, testSet, recoSet):
    allItems = set()
    recItems = set()

    for userID in trainSet:
        for itemID in trainSet[userID]:
            allItems.add(itemID)
    for userID in recoSet:
        for itemID in recoSet[userID]:
            recItems.add(itemID)

    return 1.0 * len(recItems) / len(allItems)

def popularity(trainSet, testSet, recoSet):
    import math

    itemPopularity = dict()
    for userID in trainSet:
        for itemID in trainSet[userID]:
            itemPopularity.setdefault(itemID, 0)
            itemPopularity[itemID] += 1

    ret = 0
    all = 0
    for userID in recoSet:
        for itemID in recoSet[userID]:
            ret += math.log(1 + itemPopularity[itemID])
            all += 1

    return 1.0 * ret / all

def recall2(trainSet, testSet, recoSet):
    hit = 0
    all = 0
    import numpy as np

    for userID in trainSet:
        testItems = testSet.get(userID, { })
        recoItems = recoSet.get(userID, { })
        mean = np.mean(np.array(testItems.values()))

        for itemID in recoItems:
            if itemID in testItems:
                hit += 1
        all += len(testItems)
    return 1.0 * hit / all

def precision2(trainSet, testSet, recoSet):
    hit = 0
    all = 0
    for userID in trainSet:
        testItems = testSet.get(userID, { })
        recoItems = recoSet.get(userID, { })
        mean = np.mean(np.array(testItems.values()))

        for itemID in recoItems:
            if itemID in testItems:
                hit += 1
        all += len(recoItems)
    return 1.0 * hit / all