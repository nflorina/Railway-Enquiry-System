#!/bin/sh

docker-compose build --no-cache app 
docker rm app_run > /dev/null
docker-compose run --service-ports --name=app_run app
