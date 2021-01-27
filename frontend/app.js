// Const
const usCenterLatLng = [37.275588, -104.6570002];
const defaultZoomCountry = 4;
const defaultZoomState = 6;
const markerColor = '#3388ff';
const backendApi = 'http://localhost:5000';

// Values
let map;
let myRenderer;
let markers = [];
let plants = [];
let states = [];
let selectedStateId = '-None-';
let selectedIndex = 1000;

// Elements
let stateFilterElement;
let indexFilterElement;
let totalGenerationElement;
let nameElement;
let stateElement;
let pctStateGenerationElement;
let plantLengthElement;

document.addEventListener("DOMContentLoaded", function (event) {
    stateFilterElement = document.getElementById('stateFilter');
    indexFilterElement = document.getElementById('indexFilter');

    totalGenerationElement = document.getElementById('generation');
    nameElement = document.getElementById('name');
    stateElement = document.getElementById('state');
    pctStateGenerationElement = document.getElementById('pctStateGeneration');
    plantLengthElement = document.getElementById('plantLength');

    initMap();
    getStates();
    getPlants(selectedIndex, selectedStateId);
});

function initMap() {
    map = L.map('mapid', {
        preferCanvas: true
    }).setView(usCenterLatLng, defaultZoomCountry);
    myRenderer = L.canvas({padding: 0.5});
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoiYWNvcmR1YW4iLCJhIjoiY2trYmI3aGs4MDNjazJvcXJpd2hhd3d1dyJ9.k4FO_DbLEWm_rKmOjswsWw'
    }).addTo(map);
}

function clearMap() {
    markers.forEach(marker => {
        marker.removeEventListener();
        map.removeLayer(marker);
    });
    markers = [];
}

function httpGet(url) {
    return new Promise(function (resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.onload = function () {
            if (this.status === 200) {
                resolve(JSON.parse(xhr.response));
            } else {
                reject({
                    status: this.status,
                    statusText: xhr.statusText
                });
            }
        };
        xhr.send();
    });
}

function getPlants(index, stateId) {
    const queries = [];
    if ( index !== undefined && index !==  null && index !== '') {
        queries.push({name: 'index', value: index});
    }
    if (stateId !== undefined && stateId !== null && stateId !== '-None-') {
        queries.push({name: 'stateId', value: stateId});
    }
    let url = new URL(backendApi + '/plants');
    queries.forEach(query => url.searchParams.set(query.name, query.value));
    const request = httpGet(url);
    request.then(_plants => {
            plants = _plants;
            plantLengthElement.innerText = plants.length;
            plants.forEach(plant => {
                const circleMarker = L.circleMarker([plant.lat, plant.lng], {
                    renderer: myRenderer,
                    color: markerColor,
                    radius: getMarkerRadius(plant.totalGeneration)
                })
                    .addTo(map)
                    .on('click', onMarkerClick.bind(this, plant));
                markers.push(circleMarker);
            });
        }
    );
}

function getStates() {
    const request = httpGet(backendApi + '/states');
    request.then(_states => {
        states = _states;
        states.forEach((state) => {
            const option = document.createElement('option');
            option.value = state.id;
            option.text = state.id + ': ' + state.name;
            stateFilterElement.add(option);
        });
    });
}

function onUpdateClick() {
    clearMap();
    selectedIndex = indexFilterElement.value;
    selectedStateId = stateFilterElement.value;
    if (selectedStateId !== undefined && selectedStateId !== null && selectedStateId !== '-None-') {
        const state = states.find(_state => _state.id === selectedStateId);
        map.setView([state.lat, state.lng], defaultZoomState);
    }
    getPlants(selectedIndex, selectedStateId);
}

function onMarkerClick(plant) {
    totalGenerationElement.innerText = plant.totalGeneration + ' MWh';
    nameElement.innerText = plant.name;
    stateElement.innerText = plant.stateId;
    pctStateGenerationElement.innerText = plant.pctStateGeneration + ' %';
}

function getMarkerRadius(plantValue) {
    let toReturn;
    if (plantValue <= 1700000) {
        toReturn = 5;
    } else if (plantValue <= 2740000) {
        toReturn = 10;
    } else if (plantValue <= 4830000) {
        toReturn = 15;
    } else if (plantValue <= 5870000) {
        toReturn = 20;
    } else {
        toReturn = 25;
    }
    return toReturn;
}
