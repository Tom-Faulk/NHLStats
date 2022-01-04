import requests
from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from random import *
from flask_cors import CORS

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

class NHLAPI:

    def __init__(self):
        # load team IDs
        self.teamIDs = dict()
        teamsRequest = requests.get('https://statsapi.web.nhl.com/api/v1/teams')
        teamsJSON = teamsRequest.json()['teams']
        for team in teamsJSON:
            teamName = team['name']
            teamID = team['id']
            self.teamIDs[teamName] = teamID

    def getTeamID(self, teamName):
        return self.teamIDs[teamName]

    def getRoster(self, teamID):
        url = 'https://statsapi.web.nhl.com/api/v1/teams/' + str(teamID) +'/roster'
        return requests.get(url).json()['roster']

    def getPlayerID(self, team, playerIn):
        roster = self.getRoster(self.getTeamID(team))
        for player in roster:
            if player['person']['fullName'] == playerIn:
                return str(player['person']['id'])

    def formatStats(self, stats):
        dictOut = {}
        for stat in stats.keys():
            dictOut[stat] = stats[stat]
        return dictOut


    def getPlayerStats(self, playerName=None, teamName=None, playerID=None):
        if playerID is not None: 
            url = f'https://statsapi.web.nhl.com/api/v1/people/{str(playerID)}/stats?stats=statsSingleSeason&season=20192020'
        else:
            url = 'https://statsapi.web.nhl.com/api/v1/people/' + \
                self.getPlayerID(teamName, playerName) +'/stats?stats=statsSingleSeason&season=20192020'
        ##print(requests.get(url).json())
        return requests.get(url).json()['stats'][0]['splits'][0]['stat']

    def fillDBPlayers(self):
        playerNameStat = {}
        i = 0
        realbreak = False
        client = MongoClient('localhost', 27017)
        db = client['nhlPlayers']
        collection_players = db['players']
        ##collection_players.remove({})
        for teamName, teamID in self.teamIDs.items():
            roster = self.getRoster(teamID)
            for player in roster:
                try:
                    playerStats = self.getPlayerStats(playerID=player["person"]["id"])
                    print(playerStats)
                    found_goals = False
                    for statName in playerStats:
                        if statName == 'goals':
                            found_goals = True
                    if not found_goals:
                        ##code for goalies
                        continue
                    
                    ##playerNameStat[player['person']['fullName'].replace(".", "~")] = playerStats
                    playerStats['name'] = player['person']['fullName']
                    collection_players.insert_one(playerStats)
                    i+=1
                    ##print(playerStats)
                    ###print(playerNameStat)
                    
                except Exception as e:
                    ###print("We have hit a IndexError!")
                    print(e)
                    print(player)
                    print(playerStats)

                if i == 6:
                    realbreak = True
                    break
            if realbreak:
                break

    def fillDBGoalies(self):
        playerNameStat = {}
        i = 0
        realbreak = False
        client = MongoClient('localhost', 27017)
        db = client['nhlPlayers']
        collection_goalies = db['goalies']
        ##collection_players.remove({})
        for teamName, teamID in self.teamIDs.items():
            roster = self.getRoster(teamID)
            for player in roster:
                try:
                    playerStats = self.getPlayerStats(playerID=player["person"]["id"])
                    print(playerStats)
                    found_goals = False
                    for statName in playerStats:
                        if statName == 'goals':
                            found_goals = True
                    if not found_goals:
                        ##code for goalies
                        print("we found a goalie")
                        goalieStats = playerStats
                        goalieStats['name'] = player['person']['fullName']
                        collection_goalies.insert_one(goalieStats)
                        print("this is the goalie:", goalieStats)
                        
                        continue
                    
                    i+=1
                    ##print(playerStats)
                    ###print(playerNameStat)
                    
                except Exception as e:
                    ###print("We have hit a IndexError!")
                    print(e)
                    print(player)
                    print(playerStats)

                if i == 100:
                    realbreak = True
                    break
            if realbreak:
                break

@app.route('/api/playerQuery')
def playerQuery():
    api = NHLAPI()

    api.fillDBPlayers()

    ##headings = []
    playerQuery = []
    playerData = []
    goalieQuery = []
    goalieData = []

    client = MongoClient('localhost', 27017)
    db = client['nhlPlayers']
    collection_players = db['players']
    collection_goalies = db['goalies']
    playerQuery = collection_players.find()
    goalieQuery = collection_goalies.find()
    ##for player in playerQuery.items:

    #Reformat player statistics
    print("This is what playerQuery: ", playerQuery)

    print("This is the goalieQuery: ", goalieQuery)

    ##Build only table headers
    for stats in playerQuery[0].items():
        print("hellooo this is the final print thingy")
        print(stats)
        ##headings += [stats[0]]
        
    for playerStats in playerQuery:
        print("this is stats at line 189: ", playerStats)
        del playerStats['_id']
        playerData += [playerStats]

    for goalieStats in goalieQuery:
        print("this is stats at line 189: ", goalieQuery)
        del goalieStats['_id']
        goalieData += [goalieStats]

    print("final print of goalieData")
    print(goalieData)

    playerResponse = playerData
    return jsonify(playerResponse)

@app.route('/api/goalieQuery')
def goalieQuery():
    api = NHLAPI()

    api.fillDBGoalies()

    ##headings = []
    goalieQuery = []
    goalieData = []

    client = MongoClient('localhost', 27017)
    db = client['nhlPlayers']
    collection_goalies = db['goalies']
    goalieQuery = collection_goalies.find()

    #Reformat player statistics

    print("This is the goalieQuery: ", goalieQuery)

    for goalieStats in goalieQuery:
        print("this is stats at line 189: ", goalieQuery)
        del goalieStats['_id']
        goalieData += [goalieStats]

    print("final print of goalieData")
    print(goalieData)

    goalieResponse = goalieData
    return jsonify(goalieResponse)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")