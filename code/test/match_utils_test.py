__author__ = 'pierre'

import unittest

from api.match_utils import MatchUtils

class MatchUtilsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matchList = MatchUtils.findMatchListInFolder("../../dataset/test")

    def testListCreation(self):
        self.assertEquals(len(self.matchList), 3)

        arsenalPalace = [match for match in self.matchList if (match.getHomeSide().getName() == "Arsenal"
                               and match.getAwaySide().getName() == "Crystal Palace")][0]
        norwichArsenal = [match for match in self.matchList if (match.getHomeSide().getName() == "Norwich City"
                               and match.getAwaySide().getName() == "Arsenal")][0]
        westHamSpurs = [match for match in self.matchList if (match.getHomeSide().getName() == "West Ham United"
                               and match.getAwaySide().getName() == "Tottenham Hotspur")][0]

    def testPersonalMatch(self):
        pass

if __name__ == '__main__':
    unittest.main()
