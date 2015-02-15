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

def findCroppedScoreToFrequency(scoreToFrequency, maxGoals):
    return { score: frequency for (score, frequency) in scoreToFrequency.items()
             if max(score) <= maxGoals }

def plotScorelineFrequencyGraph(name, matchList):
    maxGoals = 8
    scoreToFrequency = findCroppedScoreToFrequency(findScoreToFrequency(matchList), maxGoals)
    frequencyMatrix = convertFrequencyMapToMatrix(scoreToFrequency, maxGoals)

    # http://matplotlib.org/users/colormaps.html
    # summer, afmhot, hot
    pyplot.figure()
    pyplot.matshow(frequencyMatrix, cmap=pyplot.cm.summer, interpolation="nearest")
    for (i, j), z in numpy.ndenumerate(frequencyMatrix):
        pyplot.text(j, i, '{:0.3f}'.format(z), ha='center', va='center', size="x-small")
    pyplot.xlabel("Away")
    pyplot.ylabel("Home")
    pyplot.xticks(numpy.arange(0, maxGoals + 1, 1))
    pyplot.yticks(numpy.arange(0, maxGoals + 1, 1))
    pyplot.title("Scorelines frequencies of " + name + " top division")
    pyplot.savefig("scorelinesFrequencies_" + name + ".png", dpi=300)

def findResultFrequency(matchList):
    homeWinString = "Home win"
    drawString = "Draw"
    awayWinString = "Away win"

    resultToOccurrences = {
        homeWinString: 0,
        drawString: 0,
        awayWinString: 0
    }
    for match in matchList:
        homeGoals = match.getHomeSide().getFullTimeGoals()
        awayGoals = match.getAwaySide().getFullTimeGoals()
        if homeGoals > awayGoals:
            result = homeWinString
        elif homeGoals < awayGoals:
            result = drawString
        else:
            result = awayWinString
        resultToOccurrences[result] += 1

    totalOccurrences = sum(resultToOccurrences.values())
    assert totalOccurrences > 0

    resultToFrequency = dict()
    for result, occurrenceCount in resultToOccurrences.items():
        resultToFrequency[result] = occurrenceCount / totalOccurrences

    return resultToFrequency

def plotResultsFrequencyPie(name, matchList):
    resultToFrequency = findResultFrequency(matchList)
    resultFrequencyPairList = sorted(resultToFrequency.items(),
                                     key=lambda resultFrequencyPair: resultFrequencyPair[0])

    pieLabels = [ resultFrequencyPair[0] for resultFrequencyPair in resultFrequencyPairList ]
    pieSizes = [ resultFrequencyPair[1] for resultFrequencyPair in resultFrequencyPairList ]
    pieColors = [ "blue", "red", "green" ]
    pyplot.figure()
    patches, textList, autoTextList = pyplot.pie(pieSizes, colors=pieColors, labels=pieLabels,
                                                 autopct="%1.1f%%", startangle=90)
    for text in textList:
        text.set_size("x-large")
    for text in autoTextList:
        text.set_size("xx-large")
    pyplot.axis("equal")
    pyplot.title("Results frequencies of " + name + " top division")
    pyplot.savefig("resultsFrequencies_" + name + ".png", dpi=200)

def work():
    countryToFolder = {
        "English": ["../../dataset/actual/England"],
        "French": ["../../dataset/actual/France"],
        "Italian": ["../../dataset/actual/Italy"],
        "Spanish": ["../../dataset/actual/Spain"],
        "German": ["../../dataset/actual/Germany"]
    }

    countryToMatchList = {
        country: MatchUtils.findMatchListInFolders(folder)
        for (country, folder)
        in countryToFolder.items()
    }

    for country, matchList in countryToMatchList.items():
        plotResultsFrequencyPie(country, matchList)
        plotScorelineFrequencyGraph(country, matchList)

# Bonus, for French fans
def workZeroDraws():
    countryToFolder = {
        "England": ["../../dataset/actual/England"],
        "France": ["../../dataset/actual/France"],
        "Italy": ["../../dataset/actual/Italy"],
        "Spain": ["../../dataset/actual/Spain"],
        "Germany": ["../../dataset/actual/Germany"]
    }

    countryToZeroDrawFrequency = dict()
    for country, folder in countryToFolder.items():
        countryMatches = MatchUtils.findMatchListInFolders(folder)
        zeroScore = 0, 0
        countryToZeroDrawFrequency[country] = findScoreToFrequency(countryMatches)[zeroScore]

    print(countryToZeroDrawFrequency)

def test():
    matchList = MatchUtils.findMatchListInFolders(["../../dataset/actual/France"])
    [
      print(match.toShortString())
      for match in matchList
      if match.getHomeSide().getFullTimeGoals() == 5
      and match.getAwaySide().getFullTimeGoals() == 3
    ]

test()