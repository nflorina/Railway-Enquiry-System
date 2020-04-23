FROM mysql:5.7

WORKDIR /database
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=airplaneservice

COPY /database/init.sql /docker-entrypoint-initdb.d/

