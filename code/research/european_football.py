# Stats about european football

from api.match_utils import MatchUtils

import numpy
from matplotlib import pyplot

def findScoreToFrequency(matchList):
    scoreToOccurrenceCount = dict()
    for match in matchList:
        score = match.getHomeSide().getFullTimeGoals(), match.getAwaySide().getFullTimeGoals()
        if score not in scoreToOccurrenceCount.keys():
            scoreToOccurrenceCount[score] = 0
        scoreToOccurrenceCount[score] += 1

    totalOccurrences = sum(scoreToOccurrenceCount.values())
    assert totalOccurrences != 0

    scoreToFrequency = dict()
    for score, occurrenceCount in scoreToOccurrenceCount.items():
        scoreToFrequency[score] = occurrenceCount / totalOccurrences

    return scoreToFrequency

def findMaxGoals(scoreToFrequency):
    return max([max(score[0], score[1]) for score in scoreToFrequency.keys()])

def convertFrequencyMapToMatrix(scoreToFrequency, maxGoals):
    frequencyMatrix = numpy.zeros((maxGoals + 1, maxGoals + 1))
    for score, frequency in scoreToFrequency.items():
        frequencyMatrix[score[0]][score[1]] = frequency
    return frequencyMatrix

def printMostCommonScorelines(scoreToFrequency, limitCount):
    print(sorted(scoreToFrequency.items(),
                 key=lambda scoreFrequencyPair: scoreFrequencyPair[1],
                 reverse=True)[:limitCount])

def plotFrequencyGraph(scoreToFrequency):
    maxGoals = findMaxGoals(scoreToFrequency)
    frequencyMatrix = convertFrequencyMapToMatrix(scoreToFrequency, maxGoals)

    # http://matplotlib.org/users/colormaps.html
    # summer, afmhot, hot
    pyplot.matshow(frequencyMatrix, cmap=pyplot.cm.summer, interpolation="nearest")
    pyplot.xlabel("Away")
    pyplot.ylabel("Home")
    pyplot.title('Scoreline frequency')
    pyplot.xticks(numpy.arange(0, maxGoals + 1, 1))
    pyplot.yticks(numpy.arange(0, maxGoals + 1, 1))
    pyplot.show()

def findCroppedScoreToFrequency(scoreToFrequency, maxGoals):
    return { score: frequency for (score, frequency) in scoreToFrequency.items()
             if max(score) <= maxGoals }

def workEnglishScorelines():
    latestEnglishSeason = ["../../dataset/actual/England/PL-2013-2014"]

    englishFolderList = ["../../dataset/actual/England/PL-2013-2014",
                          "../../dataset/actual/England/PL-2012-2013",
                          "../../dataset/actual/England/PL-2011-2012",
                          "../../dataset/actual/England/PL-2010-2011",
                          "../../dataset/actual/England/PL-2009-2010",
                          "../../dataset/actual/England/PL-2008-2009",
                          "../../dataset/actual/England/PL-2007-2008"]

    matchList = MatchUtils.findMatchListInFolders(englishFolderList)
    scoreToFrequency = findScoreToFrequency(matchList)
    plotFrequencyGraph(findCroppedScoreToFrequency(scoreToFrequency, 5))
    #printMostCommonScorelines(findScoreToFrequency(matchList, 5))

def workAllScorelines():
    allMatchesList = ["../../dataset/actual"]
    scoreToFrequency = findScoreToFrequency(MatchUtils.findMatchListInFolders(allMatchesList))
    plotFrequencyGraph(findCroppedScoreToFrequency(scoreToFrequency, 3))

workAllScorelines()