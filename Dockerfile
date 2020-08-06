FROM mysql

ENV MYSQL_DATABASE="bank"
ENV MYSQL_ROOT_PASSWORD="admin"

COPY init_db/ /docker-entrypoint-initdb.d/

EXPOSE 3306