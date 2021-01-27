# US Power plants

Application to answer to AIQ challenge

## Description

Web application to display on a map us power plants with several filters and several information

## Getting Started

### Dependencies

* install docker: `https://docs.docker.com/get-docker/`
* install docker-compose: `https://docs.docker.com/compose/install/` 

### Installing

* Launch the following command
```
docker-compose up -d
```

### Development server

After executing the previous command verify your both container `plants_client_1` and `plants_api_1` are up thanks to:
```
docker ps
```
Application will be available at `http://localhost:8000` (frontend). Backend is available at `http://localhost:5000`
