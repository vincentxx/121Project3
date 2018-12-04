import os, sys, math, json, io,time
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords 
from bs4 import BeautifulSoup, SoupStrainer  
from pathlib import Path
from operator import itemgetter
from nltk.stem import PorterStemmer  

INDEX = dict()  # INDEX = {keyword: {set of (docID, tf-idf score)}}
posting_list = dict()  # = { 'keyword' : (doc1,doc2, ....) }
docLocation = dict()  # = { "docID" : path}
NUM_OF_FOLDERS = 75 # 0-74, 0-499
NUM_OF_FILES_PER_FOLDER = 100 # 500        #0-74, 0-499
MAXWORDLENGTH = 20
MINWORDLENGTH = 2
TOTAL_NUM_OF_DOC = 37497 #37497 #total documents


def buildINDEX(rootFolder):
   
    for i in range(0, NUM_OF_FOLDERS):
        for j in range(0, NUM_OF_FILES_PER_FOLDER):
            filePath = rootFolder + "/" + str(i) + "/" + str(j)  # WEBPAGES_RAW/0/12
            docID = i * 1000 + j
            docLocation[str(docID)] = filePath
    # print (docLocation)

    # Traverse each file docID and processing
    for docID in docLocation:
        try:
            buildPostingList(docID)
            print(docID,"<--------------------------------------------")
        except:
            continue

#Hoang modified this fuction to print the posting list without frequency at the beginning
def buildPostingList(docID):
    tokenList = getTokensList(docLocation[docID])
    for keyword in tokenList:
        # todo here
        if keyword not in posting_list:
            tmpSet = list()
            tmpSet.append(docID)
            posting_list[keyword] = tmpSet  # posting_list = {keyword : (doc1, doc2, ...)}
        else:
            posting_list[keyword].add(docID)
    
#Hoang added code ----------------START-------------------------
def build_list_with_IDF_score(tokenList):
    count = 0
    for keyword in tokenList:
        tokenList[keyword] = math.log(TOTAL_NUM_OF_DOC/len(tokenList[keyword]),10)
        #print("Calculating idf keyword: " + keyword + " - keys left: " + str(len(tokenList)-count))
        count += 1
    return tokenList

def updating_INDEX():
    idf_score_list = build_list_with_IDF_score(posting_list)

    # Traverse each file docID and processing
    for docID in docLocation:
        try:
            processOneDoc(docID, idf_score_list)
            #print("Populating complete INDEX file: " + docID)
        except:
            continue


def processOneDoc(docID, idf_score_list):
    dictList = buildDict(docLocation[docID])  #dictList is a dict of (keyword : freq)
    dictList_length = len(dictList)

    title_list = buildDict_title(docLocation[docID])
    for keyword in dictList:
        
        tmpTuple = (docID, int((dictList[keyword] / dictList_length * idf_score_list[keyword]) * 10000), title_list[keyword])  # Calculate tf-idf score
        if keyword not in INDEX:
            tmpSet = list()
            tmpSet.append(tmpTuple)
            INDEX[keyword] = tmpSet  # INDEX = {keyword: {set of (docID, if-tdf score)}}
        else:
            INDEX[keyword].append(tmpTuple)
            INDEX[keyword].sort(key=itemgetter(1,2),reverse=True)
            #x= sorted(INDEX[keyword],key=itemgetter(1,2),reverse=True)
            #print(INDEX[keyword])
#Hoang added code -------------------------------------- END-------------------------

def runQuery(searchKeyword, numOfDocs):
    if searchKeyword in INDEX:
        tmpSet = INDEX[searchKeyword]  # = {(docID, freq), ...}
        sortedList = sorted(tmpSet, key=lambda item: item[1], reverse=True)
        # print ("Query result of " + str(searchKeyword))
        # for i in sortedList[0:numOfDocs]:
        #     print(i)
        if numOfDocs < len(sortedList):
            queryResult = sortedList[0:numOfDocs]
        else:
            queryResult = sortedList
    else:
        queryResult = set()
    return queryResult  # Return a list of (docID,freq)


def locateTSV(docID, fileName):  # For milestone 1, I doing with tsv file, todo with json library later on
    docDirNum, docFileNum = divmod(docID, 1000)
    docTag = str(docDirNum) + "/" + str(docFileNum)
    # print(docTag)
    foundURL = "URL Not Found"
    try:
        with open(fileName, "r") as f:  # todo: multi-threading
            for line in f:
                pattern = line.split('\t', maxsplit=2)
                for pat in pattern:
                    # print(pat)
                    if pat == docTag and len(pattern) > 1:
                        foundURL = pattern[1]
    except:
        foundURL = "Error-Finding-URL"
    return foundURL


def reportMilestone1():
    # Build & store INDEX database
    # Need to change / to \ if using WINDOW
    if sys.platform.startswith('win32'):
        slash = "\\"
    else:
        slash = "/"

    rootFolderPath = os.getcwd() + slash + "WEBPAGES_RAW"
    TSVFile = rootFolderPath + slash + "bookkeeping.tsv"
    indexFilePath = rootFolderPath + slash + "INDEX"
    buildINDEX(rootFolderPath)
    updating_INDEX() #Hoang added code
    writeINDEXToFile(indexFilePath)
    writeJSONFile() #Hoang added code

    

##################### Text Processing #################################################################
def getTokensList(fileName):

    
    tokensList = []
    pattern = re.compile('[a-z0-9]+', re.IGNORECASE)
    stopWords = set(stopwords.words('english'))  # Init here for the performance

    
    with open(fileName, "r") as f:  # todo: multi-threading
        soupObj = BeautifulSoup(f, "html.parser") #parse every tag in a html
        for script in soupObj(["head","script", "style"]): 
            script.decompose()
 
        vipList = [i.get_text() for i in soupObj.find_all(['h1', 'h2', 'h3','b'])] 
        vipList.append(soupObj.title.text.strip())

        #print(vipList)
        #print("<----------------------------")
        #content = soupObj.get_text(" ",strip=True)
        content = soupObj.find_all(text=True)

        #print(content)
        #print("<----------------------------")

        tokenLine = pattern.findall(content.lower()) # Tokenize
        tokensList = filterPattern(tokenLine, stopWords) # stopWord + stemming
        #print(tokensList)

    return sorted(tokensList)  # to ensure later sorted(dictList) return descending by value and ascending by key

def buildDict(fileName):
    """ Returns a list of pairs (key,value)
        [("keys" -> "number of appearance of the key")] and sorted by the highest appearance
        Complexity: O(nlgn)    """
    tokenList = getTokensList(fileName)
    dictList = Counter()  # faster
    for token in tokenList:
        dictList[token] += 1
    return dictList

#Hoang added code -------------------------- START ---------------------------
def getTokensList_title(fileName): #only parse title, meta data and header from html
    tokensList = []
    pattern = re.compile('[a-z0-9]+', re.IGNORECASE)
    stopWords = set(stopwords.words('english'))  # Init here for the performance

   
    parsingTags = ['title', 'strong','h1', 'h2', 'h3']
    parsingOnly = SoupStrainer(parsingTags)
    with open(fileName, "r") as f: 
        soupObj = BeautifulSoup(f, features="html.parser", parse_only=parsingOnly)
        content = soupObj.get_text(" ")
        tokenLine = pattern.findall(content.lower())
        tokensList = filterPattern(tokenLine, stopWords)
    return sorted(tokensList)

def buildDict_title(fileName):
    tokenList = getTokensList_title(fileName)
    dictList = Counter()  # faster
    for token in tokenList:
        dictList[token] += 1
    return dictList
#Hoang added code -------------------------- END ---------------------------




def filterPattern(tokenList, stopWords):  # Applying all possible rules to filtering out non-sense keywords
    filteredList = []
    Porter = PorterStemmer()
    for pattern in tokenList:
        selectPattern = True
        if (re.compile('^[0-9].*', re.IGNORECASE)).match(str(pattern)) \
                or (re.compile('^[0-9]+', re.IGNORECASE)).match(str(pattern)) \
                or (pattern in stopWords) \
                or (len(str(pattern)) > MAXWORDLENGTH) \
                or (len(str(pattern)) <= MINWORDLENGTH):
            selectPattern = False

        if selectPattern:
            stemPattern = Porter.stem(pattern)  # stemming it before adding
            filteredList.append(stemPattern)
            #filteredList.append(pattern)

    return filteredList


def stemList(listOfTokens):  # Applying stemming rules for each keywords
    Porter = PorterStemmer()
    for i in range(len(listOfTokens)):
        # applying the stemmer of each item in the list
        listOfTokens[i] = Porter.stem(listOfTokens[i])



def writeJSONFile():
    with open('one.json', 'w') as fp:
        json.dump(INDEX, fp, separators=(',', ':'), ensure_ascii=False)


def writeINDEXToFile(fileName):
    with open(fileName, "w") as f:
        for keyword in INDEX:
            f.write(keyword)
            f.write('\t')
            f.write(str(INDEX[keyword]))
            f.write('\n')
##################################################


if __name__ == '__main__':
    start = time.time()
    reportMilestone1()
    print("ELIPSED TIME: ", time.time()-start)
