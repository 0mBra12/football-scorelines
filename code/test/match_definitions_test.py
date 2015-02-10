# API unit testing

import unittest

from api import match_definitions


class MatchDefinitionTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.match = match_definitions.Match("../dataset/test/2014-2-2-Arsenal-Crystal_Palace.json")
        cls.homeSide = cls.match.getHomeSide()
        cls.firstGoal = cls.homeSide.getGoalList()[0]

    def testBasicInformation(self):
        matchDate = self.match.getDate()
        self.assertEqual(matchDate.year, 2014)
        self.assertEqual(matchDate.month, 2)
        self.assertEqual(matchDate.day, 2)

        self.match.toString()
        self.match.toShortString()

    def testSideInformation(self):
        self.assertEqual(self.match.getAwaySide().getName(), "Crystal Palace")

        self.assertEqual(self.homeSide.getName(), "Arsenal")
        self.assertEqual(self.homeSide.getFullTimeGoals(), 2)
        self.assertEqual(self.homeSide.getShotsOnTarget(), 6)
        self.assertEqual(self.homeSide.getShotsWide(), 5)

    def testFirstGoal(self):
        self.assertEqual(self.firstGoal.getScorer(), "A. Oxlade-Chamberlain")
        self.assertEqual(self.firstGoal.getGoalType(), GoalType.REGULAR)
        firstGoalMinute = self.firstGoal.getMinute()
        self.assertEqual(firstGoalMinute.getNormal(), 47)
        self.assertEqual(firstGoalMinute.getAdded(), 0)

if __name__ == '__main__':
    unittest.main()
