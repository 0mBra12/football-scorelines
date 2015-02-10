#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt


def processRedQuarters(matchList):
    minuteRange = range(1, 90 + 1)

    minuteHome = 1
    quarterToHomeWinShare = dict()
    while minuteHome <= 90:
        wins = 0
        games = 0
        for i in range(minuteHome, minuteHome + 15):
            red = countHomeRedAtMinute(matchList, i)
            wins += red['wins']
            games += red['games']
        quarterToHomeWinShare[minuteHome // 15] = float(wins / games) if games != 0 else 0
        minuteHome += 15


    minuteAway = 1
    quarterToAwayWinShare = dict()
    while minuteAway <= 90:
        wins = 0
        games = 0
        for i in range(minuteAway, minuteAway + 15):
            red = countAwayRedAtMinute(matchList, i)
            wins += red['wins']
            games += red['games']
        quarterToAwayWinShare[minuteAway // 15] = float(wins / games) if games != 0 else 0
        minuteAway += 15



    # quarterToHomeWinShare = {k: v / 0.48 for k, v in quarterToHomeWinShare.items()}
    # quarterToAwayWinShare = {k: v / 0.26 for k, v in quarterToAwayWinShare.items()}
    # plt.title('Win share ratio (with over without red card) regarding game quarter of sending off')
    # plt.xlabel('Game quarters')
    # plt.ylabel('Win share ratio')
    # maxShare = 1

    plt.title('Win share regarding game quarter of sending off')
    plt.xlabel('Game quarters')
    plt.ylabel('Win share')
    maxShare = 0.38

    quarters = [ 0, 15, 30, 45, 60, 75 ]
    opacity = 0.4
    bar_width = 15
    plt.bar(quarters, list(quarterToHomeWinShare.values()), alpha=opacity, label='Home', width=bar_width/2, color = 'b')
    plt.bar([ x + (bar_width / 2) for x in quarters ], list(quarterToAwayWinShare.values()), alpha=opacity, label='Away', width=bar_width/2, color = 'r')
    
    plt.plot([15, 15], [0, maxShare], color='b', linestyle='-', linewidth=4)
    plt.plot([30, 30], [0, maxShare], color='b', linestyle='-', linewidth=4)
    plt.plot([45, 45], [0, maxShare], color='b', linestyle='-', linewidth=4)
    plt.plot([60, 60], [0, maxShare], color='b', linestyle='-', linewidth=4)
    plt.plot([75, 75], [0, maxShare], color='b', linestyle='-', linewidth=4)

    plt.grid(True)
    plt.xticks(np.arange(0, 90, 15))
    plt.legend(loc = 'upper left')
    plt.show()



def countHomeRedAtMinute(matchList, minute):
    redWinCount = 0
    redMatchCount = 0

    for match in matchList:
        earliestCard = match.home.getEarliestRedCard()
        if not (earliestCard is None) and earliestCard.minute.normal == minute:
            redMatchCount += 1

            if match.home.fulltimegoals > match.away.fulltimegoals:
                redWinCount += 1

    red = dict()
    red['wins'] = redWinCount
    red['games'] = redMatchCount 

    return red

def countAwayRedAtMinute(matchList, minute):
    redWinCount = 0
    redMatchCount = 0

    for match in matchList:
        earliestCard = match.away.getEarliestRedCard()
        if not (earliestCard is None) and earliestCard.minute.normal == minute:
            redMatchCount += 1

            if match.away.fulltimegoals > match.home.fulltimegoals:
                redWinCount += 1

    red = dict()
    red['wins'] = redWinCount
    red['games'] = redMatchCount 

    return red


def processRedAccumulation(matchList):

    minuteRange = range(1, 90 + 1)

    minuteToWinProb = dict()

    redMatchesCount = countAllRedMatches(matchList)
    for minute in minuteRange:
        redWinBeforeCount = 0
        for i in range(1, minute + 1):
            redWinBeforeCount += countRedWins(matchList, i)

        minuteToWinProb[minute] = float(redWinBeforeCount / redMatchesCount) if redMatchesCount != 0 else 0

    print(minuteToWinProb)


    England
    minuteToWinProb = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.005780346820809248, 6: 0.005780346820809248, 7: 0.005780346820809248, 8: 0.005780346820809248, 9: 0.011560693641618497, 10: 0.011560693641618497, 11: 0.011560693641618497, 12: 0.011560693641618497, 13: 0.011560693641618497, 14: 0.011560693641618497, 15: 0.011560693641618497, 16: 0.017341040462427744, 17: 0.023121387283236993, 18: 0.023121387283236993, 19: 0.023121387283236993, 20: 0.023121387283236993, 21: 0.023121387283236993, 22: 0.023121387283236993, 23: 0.028901734104046242, 24: 0.028901734104046242, 25: 0.028901734104046242, 26: 0.028901734104046242, 27: 0.028901734104046242, 28: 0.03468208092485549, 29: 0.03468208092485549, 30: 0.03468208092485549, 31: 0.03468208092485549, 32: 0.03468208092485549, 33: 0.03468208092485549, 34: 0.04046242774566474, 35: 0.04046242774566474, 36: 0.04046242774566474, 37: 0.05202312138728324, 38: 0.05202312138728324, 39: 0.05202312138728324, 40: 0.05202312138728324, 41: 0.05202312138728324, 42: 0.05202312138728324, 43: 0.05202312138728324, 44: 0.057803468208092484, 45: 0.06358381502890173, 46: 0.06358381502890173, 47: 0.06358381502890173, 48: 0.06358381502890173, 49: 0.06936416184971098, 50: 0.06936416184971098, 51: 0.07514450867052024, 52: 0.07514450867052024, 53: 0.08092485549132948, 54: 0.08670520231213873, 55: 0.09248554913294797, 56: 0.09826589595375723, 57: 0.10404624277456648, 58: 0.10404624277456648, 59: 0.10982658959537572, 60: 0.10982658959537572, 61: 0.11560693641618497, 62: 0.11560693641618497, 63: 0.12138728323699421, 64: 0.12138728323699421, 65: 0.12716763005780346, 66: 0.12716763005780346, 67: 0.12716763005780346, 68: 0.12716763005780346, 69: 0.1329479768786127, 70: 0.1329479768786127, 71: 0.1329479768786127, 72: 0.1329479768786127, 73: 0.13872832369942195, 74: 0.14450867052023122, 75: 0.14450867052023122, 76: 0.15028901734104047, 77: 0.15606936416184972, 78: 0.15606936416184972, 79: 0.1676300578034682, 80: 0.17341040462427745, 81: 0.17341040462427745, 82: 0.17341040462427745, 83: 0.17341040462427745, 84: 0.17341040462427745, 85: 0.1791907514450867, 86: 0.1791907514450867, 87: 0.18497109826589594, 88: 0.19653179190751446, 89: 0.19653179190751446, 90: 0.2023121387283237}
    values = [x * 100 for x in list(minuteToWinProb.values())]
    deriv = np.gradient(list(minuteToWinProb.values()))



    # Big 5 leagues home
    minuteToWinProbHome = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.000968054211035818, 6: 0.001936108422071636, 7: 0.001936108422071636, 8: 0.001936108422071636, 9: 0.002904162633107454, 10: 0.00484027105517909, 11: 0.005808325266214908, 12: 0.007744433688286544, 13: 0.007744433688286544, 14: 0.007744433688286544, 15: 0.007744433688286544, 16: 0.008712487899322363, 17: 0.00968054211035818, 18: 0.010648596321393998, 19: 0.010648596321393998, 20: 0.011616650532429816, 21: 0.01452081316553727, 22: 0.015488867376573089, 23: 0.016456921587608905, 24: 0.016456921587608905, 25: 0.016456921587608905, 26: 0.017424975798644726, 27: 0.022265246853823813, 28: 0.028073572120038724, 29: 0.02904162633107454, 30: 0.030977734753146177, 31: 0.03388189738625363, 32: 0.03581800580832527, 33: 0.03872216844143272, 34: 0.04065827686350436, 35: 0.04259438528557599, 36: 0.044530493707647625, 37: 0.046466602129719266, 38: 0.0484027105517909, 39: 0.05033881897386254, 40: 0.051306873184898356, 41: 0.05324298160696999, 42: 0.05517909002904162, 43: 0.05614714424007745, 44: 0.0590513068731849, 45: 0.06485963213939981, 46: 0.06679574056147145, 47: 0.06873184898354308, 48: 0.06873184898354308, 49: 0.07163601161665054, 50: 0.07260406582768635, 51: 0.07647628267182963, 52: 0.07841239109390126, 53: 0.0803484995159729, 54: 0.08422071636011616, 55: 0.08809293320425944, 56: 0.0909970958373669, 57: 0.0968054211035818, 58: 0.09777347531461762, 59: 0.10067763794772508, 60: 0.10648596321393998, 61: 0.11132623426911907, 62: 0.11423039690222653, 63: 0.12294288480154889, 64: 0.12487899322362052, 65: 0.12971926427879962, 66: 0.13165537270087124, 67: 0.1345595353339787, 68: 0.1355275895450145, 69: 0.1393998063891578, 70: 0.14133591481122942, 71: 0.14327202323330107, 72: 0.14714424007744434, 73: 0.15004840271055178, 74: 0.15488867376573087, 75: 0.1606969990319458, 76: 0.16360116166505323, 77: 0.16747337850919652, 78: 0.1713455953533398, 79: 0.18005808325266215, 80: 0.18393030009680542, 81: 0.18780251694094868, 82: 0.19167473378509198, 83: 0.20135527589545016, 84: 0.20329138431752178, 85: 0.2149080348499516, 86: 0.22362052274927396, 87: 0.2362052274927396, 88: 0.24298160696999033, 89: 0.24975798644724104, 90: 0.2700871248789932}
    homeAverageValues = movingaverage(5, list(minuteToWinProbHome.values()))

    # Big 5 leagues away
    minuteToWinProbAway = {1: 0.0, 2: 0.0006811989100817438, 3: 0.0006811989100817438, 4: 0.0006811989100817438, 5: 0.0006811989100817438, 6: 0.0006811989100817438, 7: 0.0006811989100817438, 8: 0.0006811989100817438, 9: 0.0006811989100817438, 10: 0.0006811989100817438, 11: 0.0006811989100817438, 12: 0.0006811989100817438, 13: 0.0020435967302452314, 14: 0.0020435967302452314, 15: 0.0020435967302452314, 16: 0.0034059945504087193, 17: 0.0034059945504087193, 18: 0.0034059945504087193, 19: 0.0034059945504087193, 20: 0.004087193460490463, 21: 0.004768392370572207, 22: 0.004768392370572207, 23: 0.005449591280653951, 24: 0.006130790190735695, 25: 0.008174386920980926, 26: 0.008855585831062671, 27: 0.009536784741144414, 28: 0.009536784741144414, 29: 0.010899182561307902, 30: 0.010899182561307902, 31: 0.01226158038147139, 32: 0.01430517711171662, 33: 0.015667574931880108, 34: 0.01634877384196185, 35: 0.01634877384196185, 36: 0.017711171662125342, 37: 0.017711171662125342, 38: 0.018392370572207085, 39: 0.01907356948228883, 40: 0.020435967302452316, 41: 0.023841961852861037, 42: 0.025204359673024524, 43: 0.02656675749318801, 44: 0.02997275204359673, 45: 0.0326975476839237, 46: 0.03474114441416894, 47: 0.03474114441416894, 48: 0.03678474114441417, 49: 0.03814713896457766, 50: 0.03814713896457766, 51: 0.039509536784741145, 52: 0.04155313351498638, 53: 0.043596730245231606, 54: 0.04632152588555858, 55: 0.04904632152588556, 56: 0.0497275204359673, 57: 0.051771117166212535, 58: 0.05313351498637602, 59: 0.05381471389645776, 60: 0.05653950953678474, 61: 0.05926430517711172, 62: 0.06267029972752043, 63: 0.06267029972752043, 64: 0.0653950953678474, 65: 0.06743869209809264, 66: 0.07016348773841961, 67: 0.07220708446866485, 68: 0.07493188010899182, 69: 0.0776566757493188, 70: 0.082425068119891, 71: 0.08583106267029973, 72: 0.0885558583106267, 73: 0.09059945504087194, 74: 0.09332425068119891, 75: 0.09673024523160763, 76: 0.09673024523160763, 77: 0.09877384196185286, 78: 0.10149863760217984, 79: 0.10422343324250681, 80: 0.10490463215258855, 81: 0.10831062670299728, 82: 0.11103542234332425, 83: 0.11444141689373297, 84: 0.11716621253405994, 85: 0.12057220708446867, 86: 0.12397820163487738, 87: 0.12806539509536785, 88: 0.13147138964577657, 89: 0.13419618528610355, 90: 0.1444141689373297}
    awayAverageValues = movingaverage(5, list(minuteToWinProbAway.values()))

    plt.title('Repartition of win share regarding time of sending off')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Win share')

    plt.plot(minuteRange, homeAverageValues, 'b', label='Home')
    plt.plot(minuteRange, awayAverageValues, 'r', label='Away')
    plt.plot([45, 45], [0, 0.25], color='g', linestyle='--', linewidth=2)
    plt.plot([15, 15], [0, 0.25], color='g', linestyle='--', linewidth=2)
    plt.plot([75, 75], [0, 0.25], color='g', linestyle='--', linewidth=2)

    plt.grid(True)
    plt.yticks(np.arange(0, 0.26, 0.025))
    plt.legend(loc = 'upper left')
    plt.show()


def movingaverage(nbPoints, data):

    smoothed = dict()
    for i in range(0, len(data)):
        mySum = 0
        for count in range(0, nbPoints):
            mySum += data[i - count] if i - count >= 0 else 0
        smoothed[i] = mySum / nbPoints

    return list(smoothed.values())



def countRedWins(matchList, minute):

    redWinCount = 0
    for match in matchList:
        earliestCard = match.home.getEarliestRedCard()
        if not (earliestCard is None) and earliestCard.minute.normal == minute \
                and match.home.fulltimegoals > match.away.fulltimegoals:
            redWinCount += 1

    return redWinCount

def countAllRedMatches(matchList):

    redMatchCount = 0

    for match in matchList:
        earliestCard = match.home.getEarliestRedCard()
        if not (earliestCard is None):
            redMatchCount += 1

    return redMatchCount
