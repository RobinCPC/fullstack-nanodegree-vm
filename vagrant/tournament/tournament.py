#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=tournament")
        return db
    except psycopg2.OperationalError as e:
        print e.message


def execute_query(query):
    """Takes a query statement as input and executes it"""
    try:
        db = connect()
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        db.close()
    except AttributeError as e:
        print e.message


def deleteMatches():
    """Remove all the match records from the database."""
    query = "DELETE FROM matches"
    execute_query(query)


def deletePlayers():
    """Remove all the player records from the database."""
    query = "DELETE FROM players"
    execute_query(query)


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(*) from players as cnt")
    cnt = c.fetchone()
    db.close()
    return int(cnt[0])


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    query = "INSERT INTO players (name) VALUES (%s)"
    c.execute(query, (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    query = """
            SELECT players.id,
                   players.name,
                   (SELECT count(matches.winner) from matches
                    where matches.winner = players.id) as nbr_of_win,
                   (SELECT count(matcnt.id) from matcnt
                    where matcnt.id = players.id) as nbr_of_match
            FROM players group by players.id order by nbr_of_win
            """
    c.execute(query)
    stand = c.fetchall()
    db.close()
    return stand


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s)"
    c.execute(query, (winner, loser,))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()
    query = """
            SELECT r1.id,
                   r1.name,
                   r2.id,
                   r2.name
            FROM ranks r1 JOIN ranks r2 on
            (r1.rank % 2 = 1) and (r2.rank % 2 = 0) and r1.rank = (r2.rank - 1)
            """
    c.execute(query)
    pairs = c.fetchall()
    db.close()
    return pairs

