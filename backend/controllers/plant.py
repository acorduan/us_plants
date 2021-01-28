import csv
import json

data2016FilePath = './data/egrid2016_data.csv'
data2018FilePath = './data/egrid2018_data_v2.csv'

class PlantModel:
    def __init__(self, totalGeneration, name, lat, lng, countyName, stateId, negative):
        self.totalGeneration = totalGeneration
        self.name = name
        self.lat = lat
        self.lng = lng
        self.countyName = countyName
        self.stateId = stateId
        self.negative = negative
        self.pctStateGeneration = None

class PlantController:
    def __init__(self):
        try:
            self.plants = []
            statesTotalGenerationByIndex = {}
            # Open wanted csv file
            with open(data2018FilePath) as file:
                filereader = csv.DictReader(file, delimiter=';')
                for row in filereader:
                    # Create PlantModel from csv file
                    value = 0
                    lat = 0
                    lng = 0
                    if row['PLNGENAN'] != '':
                        value = int(row['PLNGENAN'].replace(' ', ''))
                    if row['LAT'] != '':
                        lat = float(row['LAT'].replace(',', '.'))
                    if row['LON'] != '':
                        lng = float(row['LON'].replace(',', '.'))
                    plant = PlantModel(
                        abs(value),
                        row['PNAME'],
                        lat,
                        lng,
                        row['CNTYNAME'],
                        row['PSTATABB'],
                        value<0
                    )
                    # Calculate total generation of a state to be able to have the pct by plant
                    try:
                        statesTotalGenerationByIndex[plant.stateId]['totalGeneration']
                    except KeyError:
                        statesTotalGenerationByIndex[plant.stateId] = { 'totalGeneration': plant.totalGeneration }
                    else:
                        statesTotalGenerationByIndex[plant.stateId]['totalGeneration'] = statesTotalGenerationByIndex[plant.stateId]['totalGeneration'] + plant.totalGeneration
                    self.plants.append(plant)

            # Calculate pct generation of plant for it's state
            for plant in self.plants:
                pctStateGeneration = ( plant.totalGeneration / statesTotalGenerationByIndex[plant.stateId]['totalGeneration'] ) * 100
                plant.pctStateGeneration = format(pctStateGeneration, '.2f')

            # Sort plants by total generation descending
            self.plants = sorted(self.plants, key=lambda plant: plant.totalGeneration, reverse=True)
        except:
            print('An unexpected error occured during def __init__ PlantController')

    def getPlants(self):
        return self.plants
