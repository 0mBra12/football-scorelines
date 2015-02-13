# Utilities for matches

import copy
import os
import sys

from api.match_definitions import Match
from api.match_definitions import BaseMatch

class PersonalMatch(BaseMatch):
    def __init__(self, match, teamName):
        super().__init__(copy.deepcopy(match.getDate()))

        self.personalSides = dict()
        if teamName == match.getHomeSide().getName():
            self.personalSides["us"] = copy.deepcopy(match.getHomeSide())
            self.personalSides["them"] = copy.deepcopy(match.getAwaySide())
            self.atHome = True
        elif teamName == match.getAwaySide().getName():
            self.personalSides["us"] = copy.deepcopy(match.getAwaySide())
            self.personalSides["them"] = copy.deepcopy(match.getHomeSide())
            self.atHome = False
        else:
            raise KeyError()

    def getPersonalSide(self):
        return self.personalSides["us"]

    def getOpponentSide(self):
        return self.personalSides["them"]

    def isAtHome(self):
        return self.atHome

class MatchUtils:
    @staticmethod
    def findMatchListInFolder(folderPath):
        matchList = list()
        for root, directories, filenameList in os.walk(folderPath):
            for file in filenameList:
                filePath = os.path.join(root, file)
                matchList.append(Match(filePath))

        return matchList

    @staticmethod
    def retrieveMatchesFromArguments():
        args = list(sys.argv)
        args.pop(0)
        argsCount = len(args)

        if argsCount != 1:
            raise Exception("Should provide a folder path to the script")

        folderPath = args[0]
        return MatchUtils.findMatchListInFolder(folderPath)

    @staticmethod
    def printMatchSummary(matchPath):
        print(Match(matchPath).toString())

    @staticmethod
    def _findTeamNames(matchList):
        nameSet = set()
        for match in matchList:
            nameSet.add(match.getHomeTeamName())
            nameSet.add(match.getAwayTeamName())

        return nameSet

    @staticmethod
    def _findPersonalMatchList(matchList, teamName):
        personalMatchList = list()
        for match in matchList:
            if match.getHomeSide().getName() == teamName or match.getAwaySide().getName() == teamName:
                personalMatchList.append(PersonalMatch(match, teamName))
        personalMatchList.sort(key = lambda match: match.getDate())
        return personalMatchList

    @staticmethod
    def findTeamNameToPersonalMatches(matchList):
        teamNameSet = MatchUtils._findTeamNames(matchList)

        teamToGames = dict()
        for teamName in teamNameSet:
            teamToGames[teamName] = MatchUtils._findPersonalMatchList(matchList, teamName)

        return teamToGames
