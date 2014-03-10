__author__ = 'axel'
import os
from ApprovalPredictor import ApprovalPredictor

class TweetHandler:
    teams = {}
    def __init__(self, teams):
        for team in teams:
            self.getTeamTextValues(team)

    def handleTweet(self, text):
        for team in self.teams:
            if team.lower() in text.lower():
                pos = self.getPositives(text)
                neg = self.getNegatives(text)
                print pos.__str__() + ":" + neg.__str__()
                self.updateText(team, pos, neg)



    def updateText(self, team, pos, neg):
        self.getTeamTextValues(team)
        pastPos = self.teams.get(team)[0]
        pastNeg = self.teams.get(team)[1]
        newPos = pastPos + pos
        newNeg = pastNeg + neg
        self.teams[team] = [newPos,newNeg]
        fileName = team+'Values.txt'
        f = open(fileName,'w+')
        f.write(newPos.__str__()+"\n" + newNeg.__str__()) # python will convert \n to os.linesep
        f.close() # you can omit in most cases as the destructor will call if

        print self.teams


    def getPositives(self, text):
        words = text.split()
        numPositives = 0
        for word in words:
            with open("positive.txt") as f:
                for line in f:
                    if line.lower().strip() == word.lower().strip():
                        numPositives = numPositives + 1
        return numPositives
    def getNegatives(self, text):
        words = text.split()
        numNegatives = 0
        for word in words:
            with open("negative.txt") as f:
                for line in f:
                    #print line.lower().strip()
                    if line.lower().strip() == word.lower().strip():
                        numNegatives = numNegatives + 1
        return numNegatives

    def getTeamTextValues(self, team):
        fileName = team+'Values.txt'
        values = []
        if os.path.isfile(fileName):
            with open(fileName) as f:
                for line in f:
                    values.append(int(line))
                f.close()
            self.teams[team] = values
        else:
            self.teams[team] = [0,0]






