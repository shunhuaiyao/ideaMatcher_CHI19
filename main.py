import re
import sys
import csv
import operator
import os.path
from os import listdir
from gensim.models import KeyedVectors

rePattern = '[^A-Za-z]'

def readKeyphrase(fileName):
    allIdea = list()
    ideaIndex = 0
    with open(fileName) as f:
        lines = f.readlines()
        for line in lines:
            ideaHash = dict()
            for word in line.strip().split(", "):
                keyWord = word.lower()
                if keyWord != "":
                    ideaHash[keyWord] = ideaIndex
            allIdea.append(ideaHash)
            ideaIndex += 1
    return allIdea

def ideaMapping(allIdea, fileName):
    ideas = [False] * len(allIdea)
    note = ""
    with open(fileName) as f:
        lines = f.readlines()
        for line in lines:
            note += (re.sub(rePattern, " ", line).lower() + " ")
    
    for ideaHash in allIdea:
        for idea in ideaHash.keys():
            if idea in note:
                ideas[ideaHash[idea]] = True
    
    ideaCount = 0
    for idea in ideas:
        if idea:
            ideaCount += 1

    return ideaCount/len(ideas)

def calNoteTF(course, filePath):
    termFrequencies = dict()
    for fileName in listdir(filePath):
        if course in fileName.split('-'):
            with open(filePath+fileName) as f:
                lines = f.readlines()
                for line in lines:
                    line = re.sub(rePattern, " ", line).lower()
                    for word in line.split():
                        if word not in termFrequencies.keys():
                            termFrequencies[word] = 1
                        else:
                            termFrequencies[word] += 1
    
    print(sorted(termFrequencies.items(), key=operator.itemgetter(1)))

if __name__ == '__main__':
    '''
    python3 main.py psychologyConcepts psychologyDetails Psychology Turkers_Notes/
    '''
    course = sys.argv[3]
    allConcepts = readKeyphrase(sys.argv[1])
    allDetails = readKeyphrase(sys.argv[2])
    with open('keyPointsResults.csv', mode='w') as outputFile:
        output_writer = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(['course (UX, Psychology)', 'workerID', 'condition', 'coverage of concepts', 'converage of details'])
        for fileName in listdir(sys.argv[4]):
            if course in fileName.split('-'):
                COC = ideaMapping(allConcepts, sys.argv[4]+fileName)
                COD = ideaMapping(allDetails, sys.argv[4]+fileName)
                output_writer.writerow([course, fileName.split('-')[2], fileName.split('-')[0], str(COC), str(COD)])
    '''
    python3 main.py Psychology Turkers_Notes/
    calNoteTF(sys.argv[1], sys.argv[2])
    '''