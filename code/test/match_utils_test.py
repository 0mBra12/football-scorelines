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

    def testListCreation(self):
        self.assertEquals(len(self.matchList), 3)

    def testFindPersonalMatchList(self):
        arsenalMatchList = MatchUtils._findPersonalMatchList(self.matchList, "Arsenal")
        self.assertEquals(len(arsenalMatchList), 2)
        self.assertEquals(arsenalMatchList[0].getDate(), self.arsenalPalace.getDate())
        self.assertEquals(arsenalMatchList[1].getDate(), self.norwichArsenal.getDate())

        spursMatchList = MatchUtils._findPersonalMatchList(self.matchList, "Tottenham Hotspur")
        self.assertEquals(len(spursMatchList), 1)
        self.assertEquals(spursMatchList[0].getDate(), self.westHamSpurs.getDate())

if __name__ == '__main__':
    unittest.main()
