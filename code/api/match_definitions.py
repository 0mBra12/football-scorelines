# Actual match API

from enum import Enum
import json
from datetime import date

class Minute:
    def __init__(self, minuteObject):
        self._normal = minuteObject['normal']
        self._added = minuteObject['added']

    def getNormal(self):
        return self._normal

    def getAdded(self):
        return self._added

    def toString(self):
        return str(self._normal) + "'+" + str(self._added) if self._added > 0\
            else str(self._normal) + "'"

class GoalType(Enum):
    REGULAR = 1
    PENALTY = 2
    OWN_GOAL = 3

class Goal:
    def __init__(self, goalObject):
        self._scorer = goalObject['scorer']
        self._goalType = {
            "regular": GoalType.REGULAR,
            "penalty": GoalType.PENALTY,
            "own goal": GoalType.OWN_GOAL
        }[goalObject['goalType']]
        self._minute = Minute(goalObject['minute'])

    def getScorer(self):
        return self._scorer

    def getType(self):
        return self._goalType

    def getMinute(self):
        return self._minute

    def toString(self):
        goalTypeString = {
            GoalType.REGULAR: "Regular",
            GoalType.PENALTY: "Penalty",
            GoalType.OWN_GOAL: "Own goal"
        }[self._goalType]

        return self._minute.toString() + " " + self._scorer + " (" + goalTypeString + ")"

class CardColor(Enum):
    YELLOW = 1
    RED = 2

class Card:
    def __init__(self, cardObject):
        self._color = {
            "yellow": CardColor.YELLOW,
            'red': CardColor.RED,
        }[cardObject['color']]
        self._minute = Minute(cardObject['minute'])

    def getColor(self):
        return self._color

    def getMinute(self):
        return self._minute

    def toString(self):
        return self._minute.toString() + ", " + self._color

class Player:
    def __init__(self, playerObject):
        self._name = playerObject['name']
        self._number = int(playerObject['number'])

        self._cards = list()
        for cardObject in playerObject['cards']:
            self._cards.append(Card(cardObject))

    def getName(self):
        return self._name

    def getShirtNumber(self):
        return self._number

    def getCards(self):
        return self._cards

    def toString(self):
        playerDescription = str(self._number) + ". " + self._name
        nbCards = len(self._cards)
        if nbCards == 1:
            card = self._cards[0]
            if card.getColor() == 'red':
                playerDescription += ", sent off (" + card.getMinute().toString() + ")"
            else:
                playerDescription += ", booked (" + card.getMinute().toString() + ")"

        elif nbCards == 2:
            firstCard = self._cards[0]
            secondCard = self._cards[1]

            playerDescription += ", booked (" + firstCard.getMinute().toString() +\
                                 ") then sent off (" + secondCard.getMinute().toString() + ")";

        elif nbCards == 3:
            firstCard = self._cards[0]
            secondCard = self._cards[1]
            playerDescription += ", booked (" + firstCard.getMinute().toString() +\
                                 "), booked again and sent off (" + secondCard.getMinute().toString() + ")";

        return playerDescription


class Substitution:
    def __init__(self, replacementObject):
        self._replacedName = replacementObject['name']
        self._minute = Minute(replacementObject['minute'])

    def getSubstitutedName(self):
        return self._replacedName

    def getMinute(self):
        return self._minute

class Substitute(Player):
    def __init__(self, substituteObject):
        super().__init__(substituteObject)
        self._substitution = Substitution(substituteObject['replacement'])\
            if substituteObject['replacement'] is not None else None

    def getSubstitution(self):
        return self._substitution

    def toString(self):
        playerDescription = super(Substitute, self).toString()
        if self._substitution is not None:
            playerDescription += ". Replaced " + self._substitution._replacedName +\
                             " (" + self._substitution.getMinute().toString() + ")"

        return playerDescription

class Side:
    def __init__(self, sideObject):
        self._name = sideObject['name']
        self._fullTimeGoals = int(sideObject['fulltimegoals'])

        self._shotsOnTarget = int(sideObject['shotsontarget']) if sideObject['shotsontarget'] is not None else None
        self._shotsWide = int(sideObject['shotswide']) if sideObject['shotswide'] is not None else None

        self._goalList = list()
        for goalObject in sideObject['goals']:
            self._goalList.append(Goal(goalObject))

        self._lineup = list()
        for playerObject in sideObject['lineup']:
            self._lineup.append(Player(playerObject))

        self._substitutes = list()
        for substituteObject in sideObject['substitutes']:
            self._substitutes.append(Substitute(substituteObject))

    def getName(self):
        return self._name

    def getFullTimeGoals(self):
        return self._fullTimeGoals

    def getShotsOnTarget(self):
        return self._shotsOnTarget

    def getShotsWide(self):
        return self._shotsWide

    def getGoalList(self):
        return self._goalList

    def getLineup(self):
        return self._lineup

    def getBench(self):
        return self._substitutes

    def toTeamString(self):
        teamString = "Lineup\n"
        for player in self.getLineup():
            teamString += player.toString() + "\n"

        teamString += "Bench\n"
        for player in self.getBench():
            teamString += player.toString() + "\n"

        return teamString

    def toGoalsString(self):
        goalString = ""
        if len(self._goalList) > 0:
            for goal in self._goalList:
                goalString += goal.toString() + "\n"
        else:
            goalString += "No goals\n"

        return goalString

class BaseMatch:
    def __init__(self, eventDate):
        self._eventDate = eventDate

    def getDate(self):
        return self._eventDate

    def getDateString(self):
        return "{:%d %b %Y}".format(self._eventDate)

class Match(BaseMatch):
    def __init__(self, matchPath):
        with open(matchPath, 'r', encoding='utf-8') as matchFile:
            matchObject = json.load(matchFile)

            matchDate = matchObject['date']
            super().__init__(date(matchDate['year'], matchDate['month'], matchDate['day']))

            self._sides = dict()
            self._sides['home'] = Side(matchObject['home'])
            self._sides['away'] = Side(matchObject['away'])

    def getHomeSide(self) -> Side:
        return self._sides['home']

    def getAwaySide(self) -> Side:
        return self._sides['away']

    def toShortString(self):
        return self.getDateString() + ": " +\
            self.getHomeSide().getName() + " " + str(self.getHomeSide().getFullTimeGoals()) +\
            " - " + str(self.getAwaySide().getFullTimeGoals()) + " " + self.getAwaySide().getName()

    def toString(self):
        homeShots = self.getHomeSide().getShotsWide() + self.getHomeSide().getShotsOnTarget()
        awayShots = self.getAwaySide().getShotsWide() + self.getAwaySide().getShotsOnTarget()

        return self.toShortString() + "\n" + \
            "Shots : " + str(homeShots) + " - " + str(awayShots) + "\n" + \
            "Shots on target : " + str(self.getHomeSide().getShotsOnTarget()) + " - " +\
            str(self.getAwaySide().getShotsOnTarget()) + "\n" + "\n" \
            "Home goals\n" + self.getHomeSide().toGoalsString() + "\n" \
            "Away goals\n" + self.getAwaySide().toGoalsString() + "\n" \
            "Home team\n" + self.getHomeSide().toTeamString() + "\n" \
            "Away team\n" + self.getAwaySide().toTeamString()