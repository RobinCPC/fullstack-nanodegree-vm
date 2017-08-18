-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Check if database is created
Drop DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

-- Create to TABLE to save basic information of the tournament.
CREATE TABLE players ( name TEXT,
                       id SERIAL primary key );

CREATE TABLE matches ( winner INTEGER references players (id),
                       loser INTEGER references players (id),
                       match_id SERIAL primary key );

-- Create a matcnt VIEW to merge winner and loser into the same column
CREATE VIEW matcnt as
    SELECT winner as id from matches UNION ALL
    SELECT loser from matches;


-- create two VIEW to sort by wins
-- Create a VIEW temp to count how many time each player wins.
CREATE VIEW tmp as
    SELECT players.id,
           players.name,
           count(matches.winner) as win
    from players
    left join matches on players.id = matches.winner
    group by players.id order by win DESC;

-- Create a VIEW rank to sort player by the times of win.
CREATE VIEW ranks as
    SELECT ROW_NUMBER() OVER (order by win) as rank,  * from tmp;

