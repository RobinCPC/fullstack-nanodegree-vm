# Udacity Full Stack Web Developer Nanodegree Program
## Project 2. Tournament (Relational Database)

### Goal
The Goal of this project is to write a Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.

### Contents in the project folder
* **tournament.sql** - this file is used to set up the database schema.
* **tournament.py** - this file is used to provide access to the database via a library of functions which can add, delete or query data in the database.
* **tournament_test.py** - this is a client program which will use functions in tournament.py module.

### How to run?
Make sure you have connected to virtual machine by vagrant, then type:
``` bash
# change directory to the project
cd /vagrant/tournament
# run postgreSQL and import the tournament.sql
psql
\i tournament.sql
\q
# left psql and run python to test all-SQL tournament pairing.
python tournament_test.py
```

Thank you for the review!

