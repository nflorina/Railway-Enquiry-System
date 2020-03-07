#!/bin/sh

docker-compose build --no-cache admin
docker-compose run -T admin

