#!/usr/bin/python3

import sys
import match_definitions

args = list(sys.argv)
args.pop(0)
nbArgs = len(args)

def usage():
    print("USAGE : ./analytics.py matchPath1 matchPath2 ...")
    print("If there is only one match, this match will be printed")
    print("If there are multiple matches, the experimental mode is run")

if nbArgs >= 2:
    matchList = list()

    for matchPath in args:
        matchList.append(match_definitions.Match(matchPath))

    print("Received multiple matches (" + str(len(matchList)) + ") as arguments. Running experimental mode.")

    #experiments.processExperiments(matchList)
    #clustering.processMatches(matchList)

elif nbArgs == 1:
    matchPath = args[0]
    print("Received one match as argument, printing it.")
    print(match_definitions.Match(matchPath).toString())
else:
    print("No arguments given")
    usage()


