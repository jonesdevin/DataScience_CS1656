"""

Created on Tue Oct  9 16:46:11 2018

@author: devin jones
@email: daj59@pitt.edu

"""

"""
############# IMPORTS ##############
"""
import json
import math
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize




"""
############ getWeight #############
"""
def getWeight(freq, totalDocs, numDocs):

    weight = (math.log2(totalDocs / numDocs) * (1+ math.log2(freq)))
    
    return (weight)




"""
############### SORT ###############
"""
def sort(kDict):
    
    

    keys = list(kDict.keys())
    limit = len(keys)
    sortedDicts = [] 
    
    x = 0
    C1 = 0
    C2 = 1
    same = 0
    
        
    while(x < limit):
        
        keys = list(kDict.keys())
        maxScore = kDict[keys[C1]]
        
        if(len(keys) == 1):
            kDict[keys[0]]['pos'] = x + 1
            sortedDicts.insert(x, (keys[0] , kDict[keys[0]]))
            x = limit
            
            
        #Store Dict in list at x position
        elif C2 >= len(keys):
                
                #create key to store its importance with 1 being the most important
                kDict[keys[C1]]['pos'] = x + 1
                
                #insert (key, Dict) into our sorted array of dictionaries by kDict['score'] value
                sortedDicts.append((keys[C1], maxScore))
                
                #Store score of inserted dict before destroying it
                sameScore = maxScore['score']
                
                #remove used dict, no use for it in this function
                kDict.pop(keys[C1], None)
                
                
                while same > 0:
                    keys = list(kDict.keys())
                    
                    for items in keys:
                        
                        if kDict[items]['score'] == sameScore:
                            
                            #create key to store its importance with 1 being the most important
                            kDict[keys[C1]]['pos'] = x + 1
                            
                            #insert (key, Dict) into our sorted array of dictionaries by kDict['score'] value
                            sortedDicts.append((keys[C1], maxScore))
                            
                            #remove used dict, no use for it in this function
                            kDict.pop(keys[C1], None)
                            
                            #Decrement to account for getting rid of dict with same score
                            same -= 1
                            
                            #popped key from kDict so need to reinstatiate keys
                            keys = list(kDict.keys())
                            
                            #if we checked all keys set exit condition
                            if len(keys) == 0:
                                x = limit
                
                #increment X
                x += 1
                
                #reset counter variables C1 & C2
                C1 = 0
                C2 = 1
        
        
        
        else:
            
            #Set variable to compare scores
            maxScore = kDict[keys[C1]]
            nextScore = kDict[keys[C2]]           
            
            #if its max score move onto next keys score
            if maxScore['score'] > nextScore['score']:
                C2 += 1
    
            
            elif maxScore['score'] < nextScore['score']:
                C1 = C2
                C2 += 1
                same = 0
            
            #If score are equal
            if maxScore['score'] == nextScore['score']:
                    C2 += 1
                    same += 1
               
                
    #RETURN OUR SORTED ARRAY OF DICTS BY SCORE VALUE
    return sortedDicts







"""
############### MAIN ###############
"""

def main():
    print('Information Retrieval Engine - Devin Jones (daj59@pitt.edu)')
    
    with open('inverted-index.json', 'r') as file:
        words = json.load(file)
    
    
    with open('keywords.txt', 'r') as keywords:
        
        for keyword in keywords:
           

            
            listOfWords = word_tokenize(keyword)
            #Go through each word in the line
            
            
            keywordData = {}
            
            ps = PorterStemmer()
                    
                    
            stemmedListOfWords = []
            for z in listOfWords:
                stemmedListOfWords.append(ps.stem(z))
                    
            
            printedKeyword = False
            
            for x in listOfWords:
                
                #check if word is in the alphabet(no punctuation)
                if(x.isalpha()):
    
                    
                    ps = PorterStemmer()
                    
                    stemmedWord = ps.stem(x)
                    
                    #Store related data and Sort the data   
                    freq = []
                    
                    if stemmedWord not in words:
                        continue
                    
                    if not printedKeyword:
                        print("\n\n--------------------------------------------")
                        print("keywords = {}".format(keyword.lower()))
                        printedKeyword = True
                    
                    
                    #Get frequency of stemmed keyword in the documents it is in
                    for key in words[stemmedWord]:
                        
                        if key == 'numOfDocs':
                            numDocs = words[stemmedWord][key]
                        elif key == 'totalDocs':
                            totalDocs = words[stemmedWord][key]
                        
                        else:
                            freq.append((key, x.lower(), words[stemmedWord][key]))
                            
                    
                    for item in freq:
                        
                        if item[0] not in keywordData:
                            
                            keywordData[item[0]] = {}
                            
                            #initialize other keywords weights to be 0 for this .txt file
                            for x in listOfWords:
                                keywordData[item[0]][x.lower()] = 0.000000
                            
                            #initialize score to be 0
                            keywordData[item[0]]['score'] = 0.000000
                        
                        
                        keywordData[item[0]][item[1]] = getWeight(item[2], totalDocs, numDocs)   
                        
                        keywordData[item[0]]['score'] += keywordData[item[0]][item[1]]
                        
                    
            #SORT dicts in DESC order by score and label them by importance 1 - X
            # *ATTENTION* - Dicts with same score have same importance
            
            sDict = sort(keywordData)
            
             
            for dicts in sDict:
                
                print("\n[{}] file={} score={:.6f}".format(dicts[1]['pos'], dicts[0], dicts[1]['score']))
                
                keys = list(dicts[1].keys())
                
                for key in keys:
                    if key != 'score' and key != 'pos':
                        print("    weight({})={:.6f}".format(key, dicts[1][key]))
                    
                   
           

   
    
    
    
"""
############ CALL MAIN #############
"""
  
main()