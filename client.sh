#!/bin/sh

docker-compose build --no-cache client
docker-compose run -T client "http://app_run:5000"
