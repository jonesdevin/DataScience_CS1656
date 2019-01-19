"""

Created on Tue Oct  9 12:30:00 2018

@author: Devin Jones 
@email: daj59@pitt.edu

"""

import glob
import json
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize



def main():
    

    path = 'input\*.txt'
    files = glob.glob(path)
    
    allWords = {}
    docs = 0
    #Open Files
    for name in files:
        docs += 1
        try:
            with open(name, 'r') as file:
                ps = PorterStemmer()
                
                #remove input\ to get filename
                filename = name.replace("input\\", '' )
                
                #read each line in the file
                for line in file:
                   
                    #Split line into words
                    words = word_tokenize(line)
                    
                    #Go through each word in the line
                    for word in words:
                        
                        #check if word is in the alphabet(no punctuation)
                        if(word.isalpha()):
                            
                            #print(word + ":" + ps.stem(word))
                            
                            
                            stemmedWord = ps.stem(word)
                            
                            #check if the word has been added to dictionary
                            #Has been seen already
                            if stemmedWord in allWords:
                                
                                #if stemmedWord is there but from different file
                                if filename not in allWords[stemmedWord]:
                                    allWords[stemmedWord][filename] = 1
                                    allWords[stemmedWord]['numOfDocs'] += 1
                                     
                                
                                #if stemmedWord is there from same file
                                else:
                                    allWords[stemmedWord][filename] += 1
                                     
                            
                            #if stemmedWord is not there create dict 
                            #and initialize to 1
                            else:
                                allWords[stemmedWord] = {}
                                allWords[stemmedWord][filename] = 1
                                allWords[stemmedWord]['numOfDocs'] = 1
                                allWords[stemmedWord]['totalDocs'] = 1
                                
                              
                
                
                            
                   
                    
        except:
            print("Unable to open file '{}'" .format(name))
            
          
        for key in allWords:
            allWords[key]['totalDocs'] = docs
            
            
    with open('inverted-index.json', 'w') as writeFile:
        json.dump(allWords, writeFile)            
main()