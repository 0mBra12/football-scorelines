#!/usr/bin/python3

import numpy
import matplotlib.pyplot as plt
import scipy.cluster.vq as clustering

import experiment_utils


def getDataOfIndex(obsList, index):
    indexDataList = list()
    for obs in obsList:
        indexDataList.append(obs[index])
    return indexDataList

def findCentroids(obsList, centroidCount):
    standardobsList = numpy.array(obsList)
    # Choose k random observations
    centroidList, labelList = clustering.kmeans2(data = standardobsList, k = centroidCount, minit = 'points')

    return centroidList, labelList

def displayPlot(obsList, centroidList, labelList):
    for centroid in centroidList:
        print("Centroid : " + str(centroid))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = [ ([ 'r', 'g', 'b', 'y', 'm', 'k' ])[i] for i in labelList ]
    ax.scatter(getDataOfIndex(obsList, 0), getDataOfIndex(obsList, 1), getDataOfIndex(obsList, 2), c = colors)

    ax.set_xlabel('Shots')
    ax.set_ylabel('Goals')
    ax.set_zlabel('Points')

    plt.show()

def getMatchVector(teamToPoints, match, meanVarianceValues):
    # Ratio regarding season's average values
    relativeShotCount = (match.getShotCount() - meanVarianceValues["shotMean"]) / meanVarianceValues["shotStd"]
    relativeGoalCount = (match.getRiggedGoalCount() - meanVarianceValues["goalMean"]) / meanVarianceValues["goalStd"]
    pointCount = teamToPoints[match.getHomeTeamName()] + teamToPoints[match.getAwayTeamName()]
    relativePointCount = (pointCount - meanVarianceValues["pointMean"]) / meanVarianceValues["pointStd"]

    shotsWeight = 1
    goalsWeight = 5
    pointsWeight = 4
    return [ relativeShotCount * shotsWeight, relativeGoalCount * goalsWeight, relativePointCount * pointsWeight ]

def computeMatchDistance(teamToPoints, match, meanVarianceValues, centroidVector):
    matchVector = getMatchVector(teamToPoints, match, meanVarianceValues)
    distanceVector = [ a_i - b_i for a_i, b_i in zip(matchVector, centroidVector) ]
    return numpy.linalg.norm(distanceVector)

def processMatches(matchList):
    # For each match, find shot count, goal count and point sum
    shotCountList = [ match.getShotCount() for match in matchList ]
    goalCountList = [ match.getRiggedGoalCount() for match in matchList ]
    teamToPoints = experiment_utils.findTeamToPointCount(matchList)
    pointCountList = [ teamToPoints[match.getHomeTeamName()] + teamToPoints[match.getAwayTeamName()] for match in matchList ]

    # For the lists of values, find mean and variance
    meanVarianceValues = {
        "shotMean": numpy.mean(shotCountList),
        "shotStd": numpy.std(shotCountList),
        "goalMean": numpy.mean(goalCountList),
        "goalStd": numpy.std(goalCountList),
        "pointMean": numpy.mean(pointCountList),
        "pointStd": numpy.std(pointCountList)
    }

    # Create observation list for clustering algorithm
    observationList = list()
    for i, match in enumerate(matchList):
        observationList.append(getMatchVector(teamToPoints, match, meanVarianceValues))
    
    centroidCount = 3
    centroidList, labelList = findCentroids(observationList, centroidCount)

    clusterHash = dict()
    for observationIndex, clusterIndex in enumerate(labelList):
        if clusterIndex not in clusterHash.keys():
            clusterHash[clusterIndex] = list()
        clusterHash[clusterIndex].append(matchList[observationIndex])

    for clusterIndex, clusterMatchList in clusterHash.items():
        clusterHash[clusterIndex] = list(reversed(sorted(clusterMatchList, key = lambda match: computeMatchDistance(teamToPoints, match, meanVarianceValues, centroidList[clusterIndex]))))

    print("Clusters")
    for clusterIndex, clusterMatchList in clusterHash.items():
        print("Cluster" + str(clusterIndex) + ", size " + str(len(clusterMatchList)))
        for match in clusterMatchList[:5]:
            print(match.toShortString())
            #print(computeMatchDistance(teamToPoints, match, meanVarianceValues, centroidList[clusterIndex]))
        print("")

    print("Top high scores")
    matchListByScore = list(
        reversed(
            sorted(matchList,
                   key = lambda match:
                        computeMatchDistance(teamToPoints,
                                             match,
                                             meanVarianceValues,
                                             [0] * centroidCount))))
    for match in matchListByScore[:20]:
        print(match.toShortString())

    #displayPlot(observationList, centroidList, labelList)


# http://bleacherreport.com/articles/2064414-20-best-matches-of-the-201314-premier-league-season
# X  14.12.2013: Manchester City 6 - 3 Arsenal
#   22.3.2014: Cardiff City 3 - 6 Liverpool
# X  12.1.2014: Stoke City 3 - 5 Liverpool
#   29.1.2014: Tottenham Hotspur 1 - 5 Manchester City
# X  29.1.2014: Aston Villa 4 - 3 West Bromwich Albion
#   4.12.2013: Sunderland 3 - 4 Chelsea
#   23.2.2014: Liverpool 4 - 3 Swansea City
# X  23.11.2013: Everton 3 - 3 Liverpool
# X  8.2.2014: Liverpool 5 - 1 Arsenal
# X  13.4.2014: Liverpool 3 - 2 Manchester City
#   23.12.2013: Arsenal 0 - 0 Chelsea
#   22.3.2014: Chelsea 6 - 0 Arsenal
#   29.3.2014: West Bromwich Albion 3 - 3 Cardiff City
#   3.2.2014: Manchester City 0 - 1 Chelsea
# X  15.12.2013: Tottenham Hotspur 0 - 5 Liverpool
#   28.12.2013: West Ham United 3 - 3 West Bromwich Albion
#   24.11.2013: Manchester City 6 - 0 Tottenham Hotspur
#   3.5.2014: Everton 2 - 3 Manchester City
#   26.10.2013: Norwich City 0 - 0 Cardiff City
# X  2.11.2013: Manchester City 7 - 0 Norwich City


# http://www.telegraph.co.uk/sport/football/competitions/premier-league/10814226/Premier-League-10-best-matches-of-season-2013-14-in-pictures.html?frame=2907283
# X  14.12.2013: Manchester City 6 - 3 Arsenal
#   22.3.2014: Cardiff City 3 - 6 Liverpool
#   12.1.2014: Stoke City 3 - 5 Liverpool
#   29.1.2014: Tottenham Hotspur 1 - 5 Manchester City
# X  29.1.2014: Aston Villa 4 - 3 West Bromwich Albion
#   4.12.2013: Sunderland 3 - 4 Chelsea
#   23.2.2014: Liverpool 4 - 3 Swansea City
# X  23.11.2013: Everton 3 - 3 Liverpool
# X  8.2.2014: Liverpool 5 - 1 Arsenal
# X  13.4.2014: Liverpool 3 - 2 Manchester City