#!/bin/bash

# Variables
#PGHOST=""
#PGPORT=""
#PGUSER=""
DATABASE="analytics"
TABLE="data_source.subscription_created"
CSV_FILE="subscription_created.csv"

# Drop table if exists and create table
psql -h $PGHOST -U $PGUSER -d $DATABASE -c "DROP TABLE IF EXISTS $TABLE;"

psql -h $PGHOST -U $PGUSER -d $DATABASE -c "CREATE TABLE IF NOT EXISTS $TABLE (
    org_id BIGINT,
    event_timestamp TIMESTAMP WITH TIME ZONE,
    activity VARCHAR(255),
    plan VARCHAR(255),
    price DECIMAL,
    deployment VARCHAR(255)
);
"


# Copy CSV data to the table
psql -h $PGHOST -U $PGUSER -d $DATABASE -c "\COPY $TABLE FROM '$CSV_FILE' DELIMITER ',' CSV HEADER;"
