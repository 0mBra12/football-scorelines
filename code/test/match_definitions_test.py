# API unit testing

import unittest

from api.match_definitions import Match
from api.match_definitions import CardColor
from api.match_definitions import GoalType

class MatchDefinitionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.match = Match("../../dataset/test/2014-2-2-Arsenal-Crystal_Palace.json")
        cls.homeSide = cls.match.getHomeSide()

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

        self.homeSide.toGoalsString()
        self.homeSide.toTeamString()

    def testFirstGoal(self):
        firstChamberlainGoal = self.homeSide.getGoalList()[0]

        self.assertEqual(firstChamberlainGoal.getScorer(), "A. Oxlade-Chamberlain")
        self.assertEqual(firstChamberlainGoal.getType(), GoalType.REGULAR)
        firstGoalMinute = firstChamberlainGoal.getMinute()
        self.assertEqual(firstGoalMinute.getNormal(), 47)
        self.assertEqual(firstGoalMinute.getAdded(), 0)

    def testPlayer(self):
        szczesny = self.homeSide.getLineup()[0]
        self.assertEqual(szczesny.getName(), "W. Szczęsny")
        self.assertEqual(szczesny.getShirtNumber(), 1)
        self.assertEqual(szczesny.getCards(), [])
        szczesny.toString()

    def testCardedPlayer(self):
        mertesacker = self.homeSide.getLineup()[1]
        self.assertEqual(mertesacker.getName(), "P. Mertesacker")

        card = mertesacker.getCards()[0]
        self.assertEqual(card.getColor(), CardColor.YELLOW)
        self.assertEqual(card.getMinute().getNormal(), 86)

    def testUsedSubstitute(self):
        rosicky = self.homeSide.getBench()[0]
        self.assertEqual(rosicky.getName(), "T. Rosický")
        self.assertEqual(rosicky.getShirtNumber(), 7)

        podolskiSubstitution = rosicky.getSubstitution()
        self.assertEqual(podolskiSubstitution.getSubstitutedName(), "L. Podolski")
        self.assertEqual(podolskiSubstitution.getMinute().getNormal(), 72)

        rosicky.toString()

    def testUnusedSubstitute(self):
        jenkinson = self.homeSide.getBench()[4]

        self.assertEqual(jenkinson.getName(), "C. Jenkinson")
        self.assertEqual(jenkinson.getShirtNumber(), 25)
        self.assertIs(jenkinson.getSubstitution(), None)

        jenkinson.toString()

if __name__ == '__main__':
    unittest.main()
