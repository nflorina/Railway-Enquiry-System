FROM mysql:5.7

ENV MYSQL_DATABASE airplaneservice

WORKDIR /database
COPY /database/init.sql /database
COPY /database/init.sql /docker-entrypoint-initdb.d/

