__author__ = 'axel'
import math
import sys
import os

class ApprovalPredictor:
    teams = {}
    def __init__(self, teamsAndValues, func=None):
        self.teams = teamsAndValues
        if func :
             self.executePrediction = func

    def executePrediction(self):
        fileName = 'prediction'
        teamsApproval = {}
        for team in self.teams:
            fileName = fileName + team
            values = self.teams[team]
            totalPosNeg = values[0] + values[1]
            if totalPosNeg is not 0:
                approvalRating = float(values[0])/float(totalPosNeg)
                approvalRating = round(approvalRating, 2)
            else:
                approvalRating = 0
            teamsApproval[team] = approvalRating
        fileName = fileName + '.txt'
        f = open(fileName,'w+')
        for team in teamsApproval:
            f.write(team.__str__() + " " + teamsApproval[team].__str__() + "\n")
        f.close()

def predictorWithComparison() :
        print "Strategy 1"


def executeReplacement2() :
         print "Strategy 2"



if __name__ == '__main__':
    teams = {}
    for team in sys.argv[1:]:
        fileName = team+'Values.txt'
        values = []
        if os.path.isfile(fileName):
            with open(fileName) as f:
                for line in f:
                    values.append(int(line))
                f.close()
            teams[team] = values
        else:
            teams[team] = [0,0]
    approvalCalc = ApprovalPredictor(teams)
    approvalCalc.executePrediction()