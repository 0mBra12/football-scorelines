# Utilities for experiments

def findAverageShotNumber(matchList):
    shotSum = 0
    for match in matchList:
        shotSum += match.getShotCount()

    return shotSum / len(matchList) if len(matchList) > 0 else 0

def findAverageGoalNumber(matchList):
    goalSum = 0
    for match in matchList:
        goalSum += match.getGoalCount()

    return goalSum / len(matchList) if len(matchList) > 0 else 0

def findAverageRiggedGoalNumber(matchList):
    goalSum = 0
    for match in matchList:
        goalSum += match.getRiggedGoalCount()

    return goalSum / len(matchList) if len(matchList) > 0 else 0

def getEarliestRedCard(match):

    redCardList = list()
    for player in match.lineup:
        redCardList.extend(filter(lambda card: card.color == 'red', player.cards))

    for sub in match.substitutes:
        redCardList.extend(filter(lambda card: card.color == 'red', sub.cards))

    redCardList.sort(key=lambda card: card.minute.normal)
    if len(redCardList) > 0:
        return redCardList[0]
    else:
        return None

def getGoalCount(match):
    return len(match.sides['home'].goalList) + len(match.sides['away'].goalList)

def getRiggedGoalCount(match):
    return len(match.sides['home'].goalList) + 1.25 * len(match.sides['away'].goalList)

def getShotCount(match):
    return match.sides['home'].shotswide + match.sides['home'].shotsontarget +\
           match.sides['away'].shotswide + match.sides['away'].shotsontarget


def findTeamToPointCount(matchList):
    teamToMatches = findTeamNameToPersonalMatches(matchList)

    teamToPoints = dict()
    for teamName, persoMatchList in teamToMatches.items():
        teamToPoints[teamName] = findPoints(persoMatchList)

    # teamRanking = sorted(teamToPoints.items(), key=lambda x: x[1])
    # teamRanking.reverse()
    # print(teamRanking)

    return teamToPoints

def findPoints(personalMatchList):
    pointSum = 0
    for match in personalMatchList:
        personalGoalCount = match.sides['team'].fulltimegoals
        opponentGoalCount = match.sides['opponent'].fulltimegoals
        if personalGoalCount > opponentGoalCount:
            pointSum += 3
        elif personalGoalCount == opponentGoalCount:
            pointSum += 1

    return pointSum

def findGoalsForAgainst(personalMatchList):
    goalsFor = 0
    goalsAgainst = 0

    for match in personalMatchList:
        goalsFor += match.sides['team'].fulltimegoals
        goalsAgainst += match.sides['opponent'].fulltimegoals

    return goalsFor, goalsAgainst

class Performance:

    def __init__(self, points, goalsFor, goalsAgainst):
        self.points = points
        self.goalsFor = goalsFor
        self.goalsAgainst = goalsAgainst

    def __gt__(self, other):
        if self.points > other.points:
            return True

        elif self.points < other.points:
            return False

        else:
            selfGoalDifference = self.goalsFor - self.goalsAgainst
            otherGoalDifference = other.goalsFor - other.goalsAgainst

            if selfGoalDifference > otherGoalDifference:
                return True
            elif selfGoalDifference < otherGoalDifference:
                return False
            else:
                return self.goalsFor > other.goalsFor

    def __eq__(self, other):
        return self.points == other.points \
               and self.goalsFor == other.goalsFor \
               and self.goalsAgainst == other.goalsAgainst


def findPerformance(personalMatchList):
    points = findPoints(personalMatchList)
    goalsFor, goalsAgainst = findGoalsForAgainst(personalMatchList)

    return Performance(points, goalsFor, goalsAgainst)