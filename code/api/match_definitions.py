# Actual match API

import json
import datetime

class Minute:
    def __init__(self, minuteObject):
        self.normal = minuteObject['normal']
        self.added = minuteObject['added']

    def getNormal(self):
        return self.normal

    def getAdded(self):
        return self.added

    def toString(self):
        return str(self.normal) + "'+" + str(self.added) if self.added > 0\
            else str(self.normal) + "'"

class Goal:
    def __init__(self, goalObject):
        self.scorer = goalObject['scorer']
        self.goalType = goalObject['goalType']
        self.minute = Minute(goalObject['minute'])

    def getScorer(self):
        return self.scorer

    def getGoalType(self):
        return self.goalType

    def getGoalMinute(self):
        return self.goalType

    def toString(self):
        goalTypeString = {
            'regular': "Regular",
            'penalty': "Penalty",
            'own goal': "Own goal"
        }[self.goalType]

        return self.minute.toString() + " " + self.scorer + " (" + goalTypeString + ")"

class Card:
    def __init__(self, cardObject):
        self.color = cardObject['color']
        self.minute = Minute(cardObject['minute'])

    def getColor(self):
        return self.color

    def getMinute(self):
        return self.minute

    def toString(self):
        return self.minute.toString() + ", " + self.color

class Player:
    def __init__(self, playerObject):
        self.name = playerObject['name']
        self.number = int(playerObject['number'])

        self.cards = list()
        for cardObject in playerObject['cards']:
            self.cards.append(Card(cardObject))

    def getName(self):
        return self.name

    def getNumber(self):
        return self.number

    def getCards(self):
        return self.cards

    def toString(self):
        playerDescription = str(self.number) + ". " + self.name
        nbCards = len(self.cards)
        if nbCards == 1:
            card = self.cards[0]
            if card.color == 'red':
                playerDescription += ", sent off (" + card.minute.toString() + ")"
            else:
                playerDescription += ", booked (" + card.minute.toString() + ")"

        elif nbCards == 2:
            firstCard = self.cards[0]
            secondCard = self.card[1]

            playerDescription += ", booked (" + firstCard.minute.toString() +\
                                 ") then sent off (" + secondCard.minute.toString() + ")";

        elif nbCards == 3:
            firstCard = self.cards[0]
            secondCard = self.cards[1]
            playerDescription += ", booked (" + firstCard.minute.toString() +\
                                 "), booked again and sent off (" + secondCard.minute.toString() + ")";

        return playerDescription


class Substitution:
    def __init__(self, replacementObject):
        self.replacedName = replacementObject['name']
        self.minute = Minute(replacementObject['minute'])

class Substitute(Player):
    def __init__(self, substituteObject):
        super(Substitute, self).__init__(substituteObject)
        self.substitution = Substitution(substituteObject['replacement'])\
            if substituteObject['replacement'] is not None else None

    def getSubstitution(self):
        return self.substitution

    def toString(self):
        playerDescription = super(Substitute, self).toString()
        playerDescription += ". Replaced " + self.substitution.replacedName +\
                             " (" + self.substitution.minute.toString() + ")" if self.substitution is not None else ""
        return playerDescription

class Side:
    def __init__(self, sideObject):
        self.name = sideObject['name']
        self.fullTimeGoals = int(sideObject['fulltimegoals'])

        self.shotsOnTarget = int(sideObject['shotsontarget']) if sideObject['shotsontarget'] is not None else None
        self.shotsWide = int(sideObject['shotswide']) if sideObject['shotswide'] is not None else None

        self.goalList = list()
        for goalObject in sideObject['goals']:
            self.goalList.append(Goal(goalObject))

        self.lineup = list()
        for playerObject in sideObject['lineup']:
            self.lineup.append(Player(playerObject))

        self.substitutes = list()
        for substituteObject in sideObject['substitutes']:
            self.substitutes.append(Substitute(substituteObject))

    def getName(self):
        return self.name

    def getFullTimeGoals(self):
        return self.fullTimeGoals

    def getShotsOnTarget(self):
        return self.shotsOnTarget

    def getShotsWide(self):
        return self.shotsWide

    def getGoalList(self):
        return self.goalList

    def getLineup(self):
        return self.lineup

    def getBench(self):
        return self.substitutes

    def toTeamString(self):
        teamString = "Lineup\n"
        for player in self.getLineup():
            teamString += player.toString() + "\n"

        teamString += "Bench\n"
        for player in self.getBench():
            teamString += player.toString() + "\n"

        return teamString

    def getGoals(self):
        goalString = ""
        if len(self.goalList) > 0:
            for goal in self.goalList:
                goalString += goal.toString() + "\n"
        else:
            goalString += "No goals\n"

        return goalString

class Match:
    def __init__(self, matchPath):
        with open(matchPath, 'r', encoding='utf-8') as matchFile:
            matchObject = json.load(matchFile)

            matchDate = matchObject['date']
            self.date = datetime.date(matchDate['year'], matchDate['month'], matchDate['day'])
            self.sides = dict()
            self.sides['home'] = Side(matchObject['home'])
            self.sides['away'] = Side(matchObject['away'])


    def getHomeSide(self) -> Side:
        return self.sides['home']

    def getAwaySide(self) -> Side:
        return self.sides['away']

    def toShortString(self):
        return self.date.toString() + ": " +\
            self.getHomeSide().getName() + " " + str(self.getHomeSide().getFullTimeGoals()) +\
            " - " + str(self.getAwaySide().getFullTimeGoals()) + " " + self.getAwaySide().getName()

    def toString(self):
        homeShots = self.getHomeSide().getShotsWide() + self.getHomeSide().getShotsOnTarget()
        awayShots = self.getAwaySide().getShotsWide() + self.getAwaySide().getShotsOnTarget()

        return self.toShortString() + "\n" + \
            "Date : " + self.date.toString() + "\n" + \
            "Shots : " + str(homeShots) + " - " + str(awayShots) + "\n" + \
            "Shots on target : " + str(self.getHomeSide().getShotsOnTarget()) + " - " +\
            str(self.getAwaySide().getShotsOnTarget()) + "\n" + "\n" \
            "Home goals\n" + self.getHomeSide().getGoals() + "\n" \
            "Away goals\n" + self.getAwaySide().getGoals() + "\n" \
            "Home team\n" + self.getHomeSide().toTeamString() + "\n" \
            "Away team\n" + self.getAwaySide().toTeamString()