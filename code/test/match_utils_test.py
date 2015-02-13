__author__ = 'pierre'

import unittest

from api.match_utils import MatchUtils

class MatchUtilsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matchList = MatchUtils.findMatchListInFolder("../../dataset/test")
        cls.arsenalPalace = [match for match in cls.matchList if (match.getHomeSide().getName() == "Arsenal"
                               and match.getAwaySide().getName() == "Crystal Palace")][0]
        cls.norwichArsenal = [match for match in cls.matchList if (match.getHomeSide().getName() == "Norwich City"
                               and match.getAwaySide().getName() == "Arsenal")][0]
        cls.westHamSpurs = [match for match in cls.matchList if (match.getHomeSide().getName() == "West Ham United"
                               and match.getAwaySide().getName() == "Tottenham Hotspur")][0]

    @staticmethod
    def verifyArsenalFixtures(testCase, arsenalMatchList):
        testCase.assertEquals(len(arsenalMatchList), 2)
        testCase.assertEquals(arsenalMatchList[0].getDate(), testCase.arsenalPalace.getDate())
        testCase.assertEquals(arsenalMatchList[1].getDate(), testCase.norwichArsenal.getDate())

    @staticmethod
    def verifySpursFixtures(testCase, spursMatchList):
        testCase.assertEquals(len(spursMatchList), 1)
        testCase.assertEquals(spursMatchList[0].getDate(), testCase.westHamSpurs.getDate())

    def testListCreation(self):
        self.assertEquals(len(self.matchList), 3)

    def testFindPersonalMatchList(self):
        # This test assumes the three premier league matches can be uniquely identified by date
        arsenalMatchList = MatchUtils._findPersonalFixtures(self.matchList, "Arsenal")
        MatchUtilsTestCase.verifyArsenalFixtures(self, arsenalMatchList)

        spursMatchList = MatchUtils._findPersonalFixtures(self.matchList, "Tottenham Hotspur")
        MatchUtilsTestCase.verifySpursFixtures(self, spursMatchList)

    def testFindTeamFixtures(self):
        teamToFixtures = MatchUtils.findAllPersonalFixtures(self.matchList)

        arsenalMatchList = teamToFixtures["Arsenal"]
        MatchUtilsTestCase.verifyArsenalFixtures(self, arsenalMatchList)
        self.assertEquals(arsenalMatchList[0].isAtHome(), True)

        spursMatchList = teamToFixtures["Tottenham Hotspur"]
        MatchUtilsTestCase.verifySpursFixtures(self, spursMatchList)
        self.assertEquals(spursMatchList[0].isAtHome(), False)

if __name__ == '__main__':
    unittest.main()
