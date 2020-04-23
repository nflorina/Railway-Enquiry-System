FROM mysql:5.7

ENV MYSQL_DATABASE airplaneservice

WORKDIR /database

COPY /database/init.sql /database
ADD init.sql /docker-entrypoint-initdb.d

