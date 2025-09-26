#!/bin/sh

# Function to run a psql command
psql_cmd() {
    PGPASSWORD=postgres psql -h localhost -p 5433 -U postgres "$@"
}

# Drop and recreate the database
psql_cmd -d postgres -c "DROP DATABASE IF EXISTS aadhavhantire;"
psql_cmd -d postgres -c "CREATE DATABASE aadhavhantire;"

# Load schema and initial data
psql_cmd -d aadhavhantire -f create_db_new.sql