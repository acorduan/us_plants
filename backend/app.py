import json

from controllers.plant import PlantController
from controllers.state import StateController

from flask import Flask, Response, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

plantCtrl =  PlantController()
stateCtrl = StateController()

@app.route("/plants")
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def getPlantsRequest():
    try:
        error = None
        toReturn = []
        index = -1
        stateId = request.args.get('stateId')
        if stateId != None:
            matches = [state for state in stateCtrl.getStates() if state.id.lower() == stateId.lower()]
            if matches:
                for plant in plantCtrl.getPlants():
                    if plant.stateId.lower() == stateId.lower():
                        toReturn.append(plant)
            else:
                error = {'message': 'State not found', 'code': 404}
        else:
            toReturn = plantCtrl.getPlants()
        
        if request.args.get('index') != None:
            try:
                index = int(request.args.get('index'))
                if index < 0:
                    error = {'message': 'Index must be a positif integer', 'code': 400}
                else:
                    toReturn = toReturn[:index]
            except:
                error = {'message': 'Index must be a positif integer', 'code': 400}

        if error == None:
            toReturn = json.dumps(toReturn, default=lambda o: o.__dict__)
            return Response(toReturn, mimetype="application/json", status=200)
        else:
            return Response(error['message'], mimetype="application/json", status=error['code'])
    except:
        return Response('Unexpected error occured', mimetype="application/json", status=500)


@app.route("/states")
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def getStatesRequest():
    try:
        toReturn = json.dumps(stateCtrl.getStates(), default=lambda o: o.__dict__)
        return Response(toReturn, mimetype="application/json", status=200)
    except:
        return Response('Unexpected error occured', mimetype="application/json", status=500)

if __name__ == "__main__":
    app.run(debug=True, port=5000)