#!/bin/bash

sqlite3 ../main/database.db < ddl.sql
echo
echo "Done"