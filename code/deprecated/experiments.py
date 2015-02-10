#!/usr/bin/python3

from api import match_utils


def processExperiments(matchList):
    ownGoalSum = 0
    goalSum = 0
    for match in matchList:
        fullGoalList = match.sides["home"].goalList +\
                       match.sides["away"].goalList
        ownGoalSum = ownGoalSum + sum(1 for goal in fullGoalList if goal.goalType == "own goal")
        goalSum = goalSum + sum(1 for goal in fullGoalList)

    averageOwnGoalPerMatch = float(ownGoalSum) / float(len(matchList))
    print("Average own goals per match : " + str(averageOwnGoalPerMatch))

    averageOwnGoalPerGoal = float(ownGoalSum) / float(goalSum)
    print("Own goals per goal : " + str(averageOwnGoalPerGoal))

    print("Average shot count : " + str(match_utils.findAverageShotNumber(matchList)))
    print("Average goal count : " + str(match_utils.findAverageGoalNumber(matchList)))
    print("Average rigged goal count : " + str(match_utils.findAverageRiggedGoalNumber(matchList)))