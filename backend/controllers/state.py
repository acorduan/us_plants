import json

dataFilePath = './data/states.json'

class StateModel:
    def __init__(self, id, name, lat, lng):
        self.id = id
        self.name = name
        self.lat = lat
        self.lng = lng

class StateController:

    def __init__(self):
        try:
            with open(dataFilePath) as file:
                self.states = []
                statesJson = json.load(file)
                for stateRow in statesJson:
                    self.states.append(StateModel(
                        stateRow['id'],
                        stateRow['name'],
                        stateRow['lat'],
                        stateRow['lng']
                    ))
        except:
            print('An unexpected error occured during def __init__ StateController')

    def getStates(self):
        return self.states