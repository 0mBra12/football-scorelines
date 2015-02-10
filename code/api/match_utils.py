# Utilities for matches

import copy
import os
import sys

from api import match_definitions


def retrieveMatchesFromArguments():
    args = list(sys.argv)
    args.pop(0)
    argsCount = len(args)

    if argsCount != 1:
        raise Exception("Should provide a folder path to the script")

    folderPath = args[0]
    return findMatchListInFolder(folderPath)

def findMatchListInFolder(folderPath):
    matchList = list()
    for root, directories, filenameList in os.walk(folderPath):
        for file in filenameList:
            filePath = os.path.join(root, file)
            matchList.append(match_definitions.Match(filePath))

    return matchList

def printMatchSummary(matchPath):
    print(match_definitions.Match(matchPath).toString())

def findTeamNames(matchList):
    nameSet = set()
    for match in matchList:
        nameSet.add(match.getHomeTeamName())
        nameSet.add(match.getAwayTeamName())

    return nameSet

def findTeamNameToPersonalMatches(matchList):
    teamNameSet = findTeamNames(matchList)

    teamToGames = dict()
    for teamName in teamNameSet:
        teamToGames[teamName] = findPersonalMatchList(teamName, matchList)

    return teamToGames

def findPersonalMatchList(teamName, matchList):
    personalMatchList = list()
    for match in matchList:

        homeTeamName = match.getHomeTeamName()
        awayTeamName = match.getAwayTeamName()

        if homeTeamName == teamName or awayTeamName == teamName:
            matchCopy = copy.deepcopy(match)
            if teamName == homeTeamName:
                team = 'home'
                opponent = 'away'
            else:
                team = 'away'
                opponent = 'home'

            matchCopy.sides['team'] = matchCopy.sides.pop(team)
            matchCopy.sides['opponent'] = matchCopy.sides.pop(opponent)

            personalMatchList.append(matchCopy)

    return personalMatchList
