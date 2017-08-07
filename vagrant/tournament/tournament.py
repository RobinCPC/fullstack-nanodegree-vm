#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
# TODO: remove unnecessary TABLE (wins, lose)

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM lose")
    c.execute("DELETE FROM wins")
    c.execute( "DELETE FROM matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute( "DELETE FROM players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(*) from players as cnt")
    cnt = c.fetchall()
    #print cnt[0]
    db.close()
    return int(cnt[0][0])


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    #query = "INSERT INTO players VALUE (%s)", (name,)
    c.execute("INSERT INTO players VALUES (%s)", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    # create a view to cumulate total matches
    c.execute("CREATE VIEW matcnt as SELECT player1 as id from matches UNION ALL SELECT player2 from matches")
    query = "SELECT players.id, players.name, count(wins.winner) as win, count(matcnt.id) as mat from players left join wins on players.id = wins.winner left join matcnt on players.id = matcnt.id group by players.id order by win"
    c.execute(query)
    stand = c.fetchall()
    #print stand
    c.execute("DROP VIEW matcnt")
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
    c.execute("INSERT INTO wins VALUES (%s)", (winner,) )
    c.execute("INSERT INTO lose VALUES (%s)", (loser,) )
    c.execute("INSERT INTO matches VALUES (%s, %s)", (winner, loser,))
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
    # create a view to sort by wins
    c.execute("CREATE VIEW tmp as SELECT players.id, players.name, count(wins.winner) as win from players left join wins on players.id = wins.winner group by players.id order by win DESC")
    c.execute("CREATE VIEW ranks as SELECT ROW_NUMBER() OVER (order by win) as rank,  * from tmp")
    c.execute("SELECT * from ranks")
    tmp = c.fetchall()
    #print "RANK: ", tmp
    c.execute("SELECT r1.id, r1.name, r2.id, r2.name FROM ranks r1 JOIN ranks r2 on (r1.rank % 2 = 1) and (r2.rank % 2 = 0) and r1.rank = (r2.rank - 1)")
    pairs = c.fetchall()
    #print "PAIRS: ", pairs
    c.execute("DROP VIEW ranks")
    c.execute("DROP VIEW tmp")
    return pairs



