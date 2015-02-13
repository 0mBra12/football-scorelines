# Utilities for matches

import copy
import os
import sys

from api.match_definitions import Match
from api.match_definitions import BaseMatch

class PersonalMatch(BaseMatch):
    def __init__(self, match, teamName):
        super().__init__(copy.deepcopy(match.getDate()))

        self._personalSides = dict()
        if teamName == match.getHomeSide().getName():
            self._personalSides["us"] = copy.deepcopy(match.getHomeSide())
            self._personalSides["them"] = copy.deepcopy(match.getAwaySide())
            self._atHome = True
        elif teamName == match.getAwaySide().getName():
            self._personalSides["us"] = copy.deepcopy(match.getAwaySide())
            self._personalSides["them"] = copy.deepcopy(match.getHomeSide())
            self._atHome = False
        else:
            raise KeyError()

    def getPersonalSide(self):
        return self._personalSides["us"]

    def getOpponentSide(self):
        return self._personalSides["them"]

    def isAtHome(self):
        return self._atHome

class MatchUtils:
    @staticmethod
    def _findMatchListInFolder(folderPath):
        matchList = list()
        for root, directories, filenameList in os.walk(folderPath):
            for file in filenameList:
                filePath = os.path.join(root, file)
                extension = os.path.splitext(filePath)[1]
                if extension == ".json":
                    matchList.append(Match(filePath))
                else:
                    print("Ignored : " + filePath)
        return matchList

    @staticmethod
    def findMatchListInFolders(folderPathList):
        matchList = list()
        for folderPath in folderPathList:
            matchList.extend(MatchUtils._findMatchListInFolder(folderPath))

        return matchList

    @staticmethod
    def retrieveMatchesFromArguments():
        args = list(sys.argv)
        args.pop(0)
        argsCount = len(args)

        if argsCount != 1:
            raise Exception("Should provide a folder path to the script")

        folderPath = args[0]
        return MatchUtils._findMatchListInFolder(folderPath)

    @staticmethod
    def printMatchSummary(matchPath):
        print(Match(matchPath).toString())

    @staticmethod
    def _findTeamNames(matchList):
        nameSet = set()
        for match in matchList:
            nameSet.add(match.getHomeSide().getName())
            nameSet.add(match.getAwaySide().getName())

        return nameSet

    @staticmethod
    def _findPersonalFixtures(matchList, teamName):
        personalMatchList = list()
        for match in matchList:
            if match.getHomeSide().getName() == teamName or match.getAwaySide().getName() == teamName:
                personalMatchList.append(PersonalMatch(match, teamName))
        personalMatchList.sort(key = lambda match: match.getDate())
        return personalMatchList

    @staticmethod
    def findAllPersonalFixtures(matchList):
        teamNameSet = MatchUtils._findTeamNames(matchList)

        teamToFixtures = dict()
        for teamName in teamNameSet:
            teamToFixtures[teamName] = MatchUtils._findPersonalFixtures(matchList, teamName)

        return teamToFixtures
