#Alanna Pasco
#Project One

#####Code Flow:######
#readInput : reads in the input file
#Unknown : a series of functions that create the dictionary of noralized
#          trigrams for unknown documents, with document names as keys
#          (this design requires that in the input file where we have
#          "LanguageName txtfile.txt" the LanguageName part must include the
#          full word "Unknown" for it to be put into this dict, but can include
#          other characters, eg "Unknown2")
#Known : a series of functions that create the dictionary of normalized
#        trigrams for documents the language is known. Keys are langauge
#        names and values are all the trigrams of all files in that language
#        combined.
#Clean-up Functions : this group of functions take in a dictionary and do all
#                     the work for cleaning/combining/normalizing them
#Stats Tools : a group of functions that help calculate the cosine similarity
#Results Calculator / Store Scores : calculates the cosine similarity using the
#        above tools, orders them from most to least likely, and prints them
#        into a file.

import sys

#Reads an input file in this format:
# - LanguageName filename.txt etc...
#And returns a list where each item is a list of
#[LanguageName filename.txt] or [Unknown# filename.txt]
def readInput(inputfile):
    f = open(inputfile)
    langFileList = []
    for line in f:
        s = line.split()
        langFileList.append(s)
    f.close
    return langFileList

######UNKNOWNS######
#Takes in a list of list in format [[LanguageName, filename.txt], [...]]
#Returns a dictionary with Unknown documents' names in format "Unknown#" as
#keys and their file name as value
def unknownDict(langList):
    unknownDict = {}
    for line in langList:
        s = line[0] + line[1]
        if "Unknown" in s:
            unknownDict[line[0]] = line[1]
    return unknownDict

#Takes in an Unknown-File Dictionary and replaces the values with
#a single string containing every character from its corresponding file
def readUnknownFiles(unknownDict):
    for file in unknownDict:
        unknownDict[file] = readFile(str(unknownDict[file]))
    return unknownDict

######KNOWN######
#Takes in a list of list in format [[LanguageName, filename.txt], [...]]
#Returns a dictionary with LanguageName as key and multiple filenames as value
def langFileDict(langList):
    langFileDict = {}
    for line in langList:
        if (not "Unknown" in line[0] + line[1]):
            if (not line[0] in langFileDict.keys()):
                langFileDict[line[0]] = [line[1]]
            else:
                langFileDict[line[0]].append(line[1])
    return langFileDict

#This group of functions:
#Takes in a Language-File Dictionary and replaces the values with
#a single string containing every character from that language's files combined
def readFile(filename):
    file = open(filename)
    s = file.read()
    file.close
    return s

def readAllFiles(lfd):
    for lang in lfd:
        value = lfd[lang]
        for i in range(len(value)):
            value[i] = readFile(str(value[i]))
    return lfd

def readAndCombineFiles(lfd):
    langDict = readAllFiles(lfd)
    for lang in langDict:
        langDict[lang] = " ".join(langDict[lang])
    return langDict

#####Clean-Up Functions#####
###From:
##{Language: all files combined in a string
##{Unknown: the unknown file in a string
###TO: ->(cleans, calculates trigram freqs, noramalizes)->
##{Language: normalized values
##{Unknown: normalized values
#This group of functions:
#Takes in a dictionary and cleans the (string) values by:
# - removing numbers and punctuation from strings
# - replacing all sequences of whitespace with a single space and
# - converting all uppercase letters to lowercase letters
def cleanString(s):
    cleanstr = ""
    s = " ".join(s.strip(" "))
    for i in range(len(s)):
        if(s[i].isalpha()
           or s[i] == " "):
            cleanstr += s[i].lower()
    return cleanstr

def cleanDictionary(dict):
    for value in dict:
        dict[value] = cleanString(dict[value])
    return dict

#This group of functions:
#Takes a clean string-valued dictionary and returns a trigram dictionary where
# - keys are language/unknown names
# - values are another dictionary of all possible trigrams from files
def createTrigramDict(string):
    triDict = {}
    for i in range(len(string)):
        if(string[i:(i+3)] in triDict.keys()):
            triDict[string[i:(i+3)]] += 1
        else:
            triDict[string[i:(i+3)]] = 1
    return triDict

def langTrigramDict(Dict):
    for value in Dict:
        Dict[value] = createTrigramDict(Dict[value])
    return Dict

#This group of functions Normalizes data in a trigram dictionary
def total(triDict):
    count = 0
    for freq in triDict:
        count += triDict[freq]
    return count

def normalize(triDict):
    for trigram in triDict:
        triDict[trigram] = (triDict[trigram] / total(triDict))
    return triDict

def normalizeDict(CompleteTrigDict):
    for value in CompleteTrigDict:
        CompleteTrigDict[value] = normalize(CompleteTrigDict[value])
    return CompleteTrigDict

##########################################
#This function cleans, creates trigrams, and normalizes the unknown files
#It creates and returns the complete Unknown File Dictionary
def unknown(i):
    return normalizeDict(langTrigramDict(cleanDictionary(
        readUnknownFiles(unknownDict(i)))))

#This function cleans, creates trigrams, and normalizes the known files
#It creates and returns the complete Known Language Dictionary
def known(i):
    return normalizeDict(langTrigramDict(cleanDictionary(
        readAndCombineFiles(langFileDict(i)))))

##########################################
##########Tools to Calculate Stats########
#Creates a list of the Total Possible (TP) trigrams in the entire language
def allPossibleTrigrams():
    alphabet = [" ", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w",
                "x", "y", "z"]
    totalTriList = [x+y+z for x in alphabet for y in alphabet for z in alphabet]
    return totalTriList

#Creates a list with all normalized frequencies of TP trigrams in a given dict
def TPTrigrams(triDict):
    tri = allPossibleTrigrams()
    TPList = []
    for t in tri:
        if t in triDict.keys():
            TPList.append(triDict[t])
        else:
            TPList.append(0)
    return TPList

#Calculates the numerator of the Cosine Similarity equation
def numerator(ukTriDict, knowntriDict):
    AList = TPTrigrams(ukTriDict)
    BList = TPTrigrams(knowntriDict)
    sumList = []
    for i in range(len(AList)):
        result = AList[i] * BList[i]
        sumList.append(result)
    return sum(sumList)

#Calculates one side of the denominator of the Cosine Similarity equation
def denominator(dict):
    list = TPTrigrams(dict)
    sumList = []
    for nfreq in list:
        result = nfreq * nfreq
        sumList.append(result)
        den = (sum(sumList))**.5
    return den

#Calculates the cosine similarity of two single inputs
def cosineSimilarity(ukTriDict, knowntriDict):
    num = numerator(ukTriDict, knowntriDict)
    den = denominator(ukTriDict) * denominator(knowntriDict)
    return num / den


##########################################
##Brings together the Cosine Similarity##
#helps the resultsCalculator function order the results
def order(scoreList):
    scoreList.sort(key=lambda x: x[1], reverse=True)
    return scoreList

#calculates the cosine similarity
def resultsCalculator(completeUkDict, completeKnownDict):
    results = {}
    for ukfile in completeUkDict:
        scoreList = []
        for lang in completeKnownDict:
            result = cosineSimilarity(completeUkDict[ukfile],
                                      completeKnownDict[lang])
            scoreList.append([lang, result])
            #scoreList is a list of lists [[lang, score], [lang, score]...]
        orderedScoreList = order(scoreList)
        results[ukfile] = orderedScoreList
    return results

#stores the results into a file
def storeScores(output, results):
    file = open(output, 'w')
    for scoreList in results:
        file.write(scoreList.upper() + '\n')
        for score in results[scoreList]:
            file.write(score[0] + " " + str(score[1])[0:7] + '\n')
        file.write('\n')
    file.close()

def main():

    script, inputfile, outputfile = sys.argv

    fileList = readInput(inputfile)
    UK = unknown(fileList)
    K = known(fileList)
    res = resultsCalculator(UK, K)

    storeScores(outputfile, res)

    print(res)



main()
