#!/usr/bin/python3
#@Vu Tran
""" Team 55
    Vu Tran - 48894667
    Anas ??
    Hoang ??
    CS 121 - Project 3  """

""" Objective: 
    Build INDEX table from 37,497 files
    Parsing for keywords
    """

""" Data structure:
    INDEX is a dict= {keyword:(set of (docID,frequency)), ...}, works as main database
    docID = foldNum * 1000 + location file number of that folder, ex: 34/156 => docID = 34156
    """

""" Algorithm:
    For each docID do
        IF a "keyword" found not existing in the INDEX
            adding it to INDEX[keys]
            adding docID to the set of that "keywords" in INDEX
        ELSE
            adding docID to the set of that "keywords" in INDEX
    Store INDEX database on a file
    """
"""" Answer query:
    """

import os, sys
import re
from collections import Counter

INDEX           = dict()            # INDEX = {keyword: {set of (docID, frequency)}}
docLocation     = dict()            # = { "docID" : path}
NUM_OF_FOLDERS    = 75              #0-74, 0-499
NUM_OF_FILES_PER_FOLDER = 500       #0-74, 0-499

def buildINDEX(rootFolder):
    #0-74, 0-499
    #Build docID - filename mapping
    for i in range(0, NUM_OF_FOLDERS):
        for j in range(0, NUM_OF_FILES_PER_FOLDER):
            filePath = rootFolder + "/" + str(i) + "/" + str(j)  # WEBPAGES_RAW/0/12
            docID = i * 1000 + j
            docLocation[str(docID)] = filePath
    #print (docLocation)

    #Traverse each file docID and processing
    for docID in docLocation:
        try:
            processOneDoc(docID)
        except:
            continue
    return None

def processOneDoc(docID):
    dictList = buildDict(docLocation[docID])
    for keyword in dictList:
        #todo here
        if keyword not in INDEX:
            tmpTuple = (docID,dictList[keyword])
            tmpSet = set()
            tmpSet.add(tmpTuple)
            INDEX[keyword] = tmpSet # INDEX = {keyword: {set of (docID, frequency)}}
        else:
            tmpTuple = (docID,dictList[keyword])
            INDEX[keyword].add(tmpTuple)
    return None

def runQuery(searchKeyword, numOfDocs):
    if searchKeyword in INDEX:
        tmpSet = INDEX[searchKeyword]       # = {(docID, freq), ...}
        sortedList = sorted(tmpSet, key=lambda item: item[1], reverse=True)
        # print ("Query result of " + str(searchKeyword))
        # for i in sortedList[0:numOfDocs]:
        #     print(i)
    return sortedList[0:numOfDocs] #Return a list of (docID,freq)

def locateTSV(docID, fileName): #For milestone 1, I doing with tsv file, todo with json library later on
    docDirNum, docFileNum = divmod(docID, 1000)
    docTag= str(docDirNum) + "/" +str(docFileNum)
    #print(docTag)
    foundURL = "URL Not Found"
    try:
        with open(fileName, "r") as f:                  #todo: multi-threading
            for line in f:
                pattern = line.split('\t', maxsplit=2)
                for pat in pattern:
                    #print(pat)
                    if pat == docTag and len(pattern) > 1:
                        foundURL = pattern[1]
    except:
        foundURL = "Error-Finding-URL"
    return foundURL

def writeINDEXToFile(fileName):
    with open(fileName, "w") as f:
        for keyword in INDEX:
            f.write(keyword)
            f.write('\t')
            f.write(str(INDEX[keyword]))
            f.write('\n')
    return None

def reportMilestone1():
    #Build & store INDEX database
    #Need to change / to \ if using WINDOW
    if sys.platform.startswith('win32'):
        slash="\\"
    else:
        slash="/"

    rootFolderPath      = os.getcwd() + slash + "WEBPAGES_RAW"
    TSVFile             = rootFolderPath + slash + "bookkeeping.tsv"
    indexFilePath       = rootFolderPath + slash + "INDEX"
    buildINDEX(rootFolderPath)
    writeINDEXToFile(indexFilePath)

    #Query list
    queryList   = ['informatics', 'mondego', 'irvine', 'artificial', 'computer']
    queryReturn = list()
    numOfReturn = 10
    for query in queryList:
        print("Query result of " + str(query) + " :")
        result = runQuery(query, numOfReturn)
        for docIDItem in result:
            foundURL = locateTSV(int(docIDItem[0]), TSVFile)
            queryReturn.append((docIDItem[0], foundURL))
            docDirNum, docFileNum = divmod(int(docIDItem[0]), 1000)
            docTag = str(docDirNum) + "/" + str(docFileNum)
            print("\tDocID " + str(docTag) + " : " + str(foundURL))
        #print(queryReturn)
    return None

##################### Text Processing #################################################################
def getTokensList(fileName):
    """ Convert file name text contents into sorted list of tokens in alphabetically
        Reading lines in file: O(n)
        Sorting token list: O(nlgn)
        Thus, complexity: O(nlgn)    """
    tokensList = []
    pattern = re.compile('[a-z0-9]+', re.IGNORECASE)
    with open(fileName, "r") as f:                  #todo: multi-threading
        for line in f:
            tokenLine = pattern.findall(line.lower())
            tokensList += tokenLine
    #tokensList.sort(key=str.lower)
    #print(tokensList)
    return sorted(tokensList)       #to ensure later sorted(dictList) return descending by value and ascending by key

def buildDict(fileName):
    """ Returns a list of pairs (key,value)
        [("keys" -> "number of appearance of the key")] and sorted by the highest appearance
        Complexity: O(nlgn)    """
    tokenList = getTokensList(fileName)
    dictList = Counter() #faster
    for token in tokenList:
        dictList[token] += 1
    return dictList
######################################################################################################


#Main()
if __name__ == '__main__':
    reportMilestone1()