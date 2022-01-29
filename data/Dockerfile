FROM postgres:14.1-alpine

RUN mkdir -p /data
COPY data.csv /data/

COPY init_experiments_db.sql /docker-entrypoint-initdb.d/init_experiments_db.sql

RUN chown postgres /data
RUN chmod +w /data

EXPOSE 5432