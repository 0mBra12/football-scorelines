#!/usr/bin/python3

import match_utils
import experiment_utils


def getAverageQualificationPoints(yearToMatches, selectedWinners):

    qualifiedCount = 0
    pointsSum = 0
    for yearMatchList in yearToMatches.values():

        groupStageMatches = [ m for m in yearMatchList if m.group != None ]

        # Put teams in groups
        groupToTeams = dict()
        for match in groupStageMatches:
            group = match.group

            if group not in groupToTeams.keys():
                groupToTeams[group] = set()
            groupToTeams[group].add(match.sides['home'].name)
            groupToTeams[group].add(match.sides['away'].name)

        for groupName, teamSet in groupToTeams.items():

            teamToPerformance = dict()
            for team in teamSet:
                persoMatchList = experiment_utils.findPersonalMatchList(team, groupStageMatches)

                performance = experiment_utils.findPerformance(persoMatchList)
                teamToPerformance[team] = performance

            ranking = sorted(teamToPerformance.keys(), key=lambda t: teamToPerformance[t], reverse=True)

            # print("Group " + groupName)
            # for rank, teamName in enumerate(ranking):
            #     print(str(rank + 1) + ". " + teamName)

            if (selectedWinners == "1&2"):
                interestingWinners = ranking[:2]
            elif (selectedWinners == "1"):
                interestingWinners = ranking[:1]
            elif (selectedWinners == "2"):
                interestingWinners = ranking[1:2]
            else:
                assert False

            for winner in interestingWinners:
                pointsSum += teamToPerformance[winner].points
                qualifiedCount += 1

    avgPoints = pointsSum / qualifiedCount if qualifiedCount != 0 else 0
    return avgPoints

def getQualificationRate(yearToMatches, result, matchIndex):

    qualifyingWinnerCount = 0
    winnerCount = 0
    for yearMatchList in yearToMatches.values():

        groupStageMatches = [ m for m in yearMatchList if m.group != None ]

        # Put teams in groups
        groupToTeams = dict()
        for match in groupStageMatches:
            group = match.group

            if group not in groupToTeams.keys():
                groupToTeams[group] = set()
            groupToTeams[group].add(match.sides['home'].name)
            groupToTeams[group].add(match.sides['away'].name)

        qualifyingTeams = set()
        firstMatchWinners = set()
        for groupName, teamSet in groupToTeams.items():

            teamToPerformance = dict()
            for team in teamSet:
                persoMatchList = experiment_utils.findPersonalMatchList(team, groupStageMatches)

                performance = experiment_utils.findPerformance(persoMatchList)
                teamToPerformance[team] = performance

                sortedByDate = sorted(persoMatchList, key=lambda x: x.date)

                wantedMatch = sortedByDate[matchIndex - 1]

                teamGoals = wantedMatch.sides['team'].fulltimegoals
                opponentGoals = wantedMatch.sides['opponent'].fulltimegoals
                if (result == 'w' and teamGoals > opponentGoals) \
                    or (result == 'd' and teamGoals == opponentGoals) \
                    or (result == 'l' and teamGoals < opponentGoals):
                    firstMatchWinners.add(team)

            ranking = sorted(teamToPerformance.keys(), key=lambda t: teamToPerformance[t], reverse=True)

            # print("Group " + groupName)
            # for rank, teamName in enumerate(ranking):
            #     print(str(rank + 1) + ". " + teamName)

            groupWinners = ranking[:2]
            for winner in groupWinners:
                qualifyingTeams.add(winner)

        for team in firstMatchWinners:
            if team in qualifyingTeams:
                qualifyingWinnerCount += 1
        winnerCount += len(firstMatchWinners)

    qualificationRate = qualifyingWinnerCount / winnerCount
    return qualificationRate


def processQualificationRate(matchList):

    # Put matches in years
    yearToMatches = dict()
    for match in matchList:
        year = match.date.year
        if year not in yearToMatches.keys():
            yearToMatches[year] = list()
        yearToMatches[year].append(match)

    # Find qualification rates    
    print("Match index;Win;Draw;Loss")
    for matchIndex in [ 1, 2, 3 ]:
        print(str(matchIndex) + ";", end="")
        for result in [ 'w', 'd', 'l' ]:
            print("{0:0.2f}".format(getQualificationRate(yearToMatches, result, matchIndex)) + ";", end="")
        print("")

    # Find average qualification points needed to qualify
    print("Average qualification points")
    print("Winner: " + str(getAverageQualificationPoints(yearToMatches, "1")))
    print("Runner-up: " + str(getAverageQualificationPoints(yearToMatches, "2")))
    print("Winner and Runner-up: " + str(getAverageQualificationPoints(yearToMatches, "1&2")))



    #print("Match n° " + str(matchIndex) + " : " + "{0:0.3f}".format(successRate))

    # Results for first match :
    # Match 1 : 0.848
    # Match 2 : 0.826
    # Match 3 : 0.711

def processMatches(matchList):

    processQualificationRate(matchList)