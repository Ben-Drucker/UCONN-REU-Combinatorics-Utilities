#!/usr/bin/env python
# coding: utf-8

# In[407]:


from itertools import combinations


# In[543]:


pi = Permutation([8,3,2,5,7,4,6,1])


# In[557]:


PermInfo(pi)


# In[556]:


def PermInfo(Per):
    infolist = [["LamL: ",LamL_k(pi)],["AL's: ",AL_k(pi)],["MuL: ",MuL_k(pi)],["DL's: ",DL_k(pi)],["Ascents: ", getAscents(Per)]]
    for item in infolist:
        partialResult = ""
        partialResult += item[0]
        partialResult += str(item[1])
        print(partialResult)
    print("Hasse: ")
    g = pi.permutation_poset()
    g.show()


# In[496]:


def LamL_k(Per):
    return MuL_k(Per).conjugate()


# In[508]:


def AL_k(Par):
    imprt = LamL_k(Par)
    result = [0]
    total = 0
    for i in range(0,len(imprt)):
        total = imprt[i]+total
        result.append(total)
    return result


# In[498]:


def MuL_k(Per):
    result = []
    imprt = DL_k(Per)
    for i in range(1, len(imprt)):
        result.append(imprt[i]-imprt[i-1])
    return Partition(result)


# In[449]:


def DL_k(Per):
    asc = getAscents(Per)
    DL_i = [0]
    partitions = []
    num_of_bars = 0
    while len(partitions)<=(len(asc)):
        ### Add loop
        greatest = 0
        candidatePartitions = []
        indexCombs = chooseIndicies(asc, num_of_bars)
        for indexCom in indexCombs:
            candidatePartitions.append(partitionAfterIndex(Per, indexCom))
        partitions.append(candidatePartitions)
        num_of_bars += 1
    #return partitions
    for level in partitions:
        greatest = 0
        for candidatePartition in level:
            partSum = 0
            for partitionPiece in candidatePartition:
                partSum += longestDecr(partitionPiece)
            if partSum > greatest:
                greatest = partSum
        DL_i.append(greatest)
    return DL_i


# In[450]:


def longestDecr(Perm):
    if len(Perm)==1:
        return 1
    longest = 0
    candidates = []
    combs = []
    for j in range(1,len(Perm)+1):
        combs.append(list(combinations(Perm,j)))
    newlist = []
    for elt in combs:
        for lelt in elt:
            newlist.append(lelt)
    for com in newlist:
        decr = True
        for i in range(len(com)-1):
            if com[i] < com[i+1]:
                decr = False
        if decr == True:
            candidates.append(com)
    for can in candidates:
        if len(can)>longest:
            longest = len(can)
    return longest


# In[451]:


def partitionAfterIndex(Perm, indicies):
    returnList = []
    prevIndex = 0
    indicies.append(len(Perm))
    for index in indicies:
        returnList.append(Perm[prevIndex:(index+1)])
        prevIndex = index + 1
    return returnList


# In[435]:


def getAscents(Perm):
    asc = []
    for i in range(len(Perm)-1):
        if Perm[i]<Perm[i+1]:
            asc.append(i)
    return asc


# In[436]:


def chooseIndicies(ListOfIndicies, numberToChoose):
    tuples = list(combinations(ListOfIndicies, numberToChoose))
    returnList =[]
    for tup in tuples:
        returnList.append(list(tup))
    return returnList

