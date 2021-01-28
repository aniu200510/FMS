#!/bin/bash

#
#  Funding management system installation instructions.
#

create_db(){
    sudo -u postgres psql -c 'CREATE DATABASE "fms";'
    sudo -u postgres psql -c "CREATE USER funder WITH PASSWORD 'funder1017';"
    sudo -u postgres psql -c 'ALTER USER funder CREATEDB;'
    sudo -u postgres psql -c 'ALTER ROLE funder SET client_encoding TO "utf8";'
    sudo -u postgres psql -c 'ALTER ROLE funder SET default_transaction_isolation TO "read committed";'
    sudo -u postgres psql -c 'ALTER ROLE funder SET timezone TO "Asia/Shanghai";'
    sudo -u postgres psql -c 'GRANT ALL PRIVILEGES ON DATABASE "fms" TO funder;'
}

create_db
