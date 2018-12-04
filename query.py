import json, re
from nltk.stem import PorterStemmer 

def stemList(listOfTokens):  
    Porter = PorterStemmer()
    for i in range(len(listOfTokens)):
        listOfTokens[i] = Porter.stem(listOfTokens[i])

#queryList = ['informatics', 'mondego', 'irvine', 'artificial', 'computer']

def init():
    # get user input and split it on white space and stemm it
    queryList = input("Enter Search word:").strip().split()
    stemList(queryList)

    result = []
    #load the index as dict
    data = json.load(open("one.json"))

    for query in queryList:
        try:
            # get the posting list for the query if in index
            postingList = data[query.lower()]
        except:
            #query not in index, who care move on!
            print("WE DONT HAVE IT!")
            continue
        # list of Url sets (for every query) 
        result.append(setOfURLS(postingList))
    
    print(result)    
    x = result[0].intersection(*result[1:])
    for x in x:
        print(x)
        with open('r.txt','a') as w:
            w.write(x)   
            w.write("\n") 



def setOfURLS(postingList):
    rset = set()
    #load bookkeeping file as dict
    bookkeepingJson = json.load(open('./WEBPAGES_RAW/bookkeeping.json'))
    # i is list of ti-dfi and docId
    for i in postingList:
            # match bookkeeping ID
            print(i)
            docDirNum, docFileNum = divmod(int(i[0]), 1000)
            docID = str(docDirNum) + "/" + str(docFileNum)

            # once we have docID it alawys exists in bookkeeping dict
            targetURL = bookkeepingJson[docID]
            rset.add(targetURL)
            #print("DocID: %s URL: %s"  %(str(docID),targetURL))
    return rset

init()
