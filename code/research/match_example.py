# Match API Usage example

from api.match_utils import MatchUtils

matchList = MatchUtils.findMatchListInFolder("../dataset/actual/England/PL-2012-2013")

goalSum = 0
for match in matchList:
    goalSum += match.getHomeSide().getFullTimeGoals() + match.getAwaySide().getFullTimeGoals()

print("Goal sum : " + str(goalSum))

MatchUtils.printMatchSummary("../dataset/test/2014-2-2-Arsenal-Crystal_Palace.json")
