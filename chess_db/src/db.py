import pandas as pd
import sqlite3 as sq
import os
import logging

log = logging.getLogger(__name__)

#Step 0: Create Schema
def create_schema(conn:sq.Connection)->None:
    """
    We need to create and normalize 3 tables out of the csv data:
    Players, Openings, Games

    Define all three tables with explicit types, PRIMARY KEYS,
    FORIEGN KEYs, NOT NULL constraints, and CHECK constraints.

    Why explicit CREATE TABLE instead of letting to_sql infer?
    - to_sql creates column with no constraints whatsover
    -FK relationships would exists in comments only, not enforced
    -CHECK constraints (winner IN(...), turns>=1) would be absent
    -NOT NULL would not be set on ny column
    -Column types would be SQLite affinity guesses, not intentional choices

    Insertion order matters:
     players and openinings must exists before games,
     becuse games has FK references to both.
    """
    #Drop in reverse FK dependency order so re-runs are clean
    conn.execute("DROP TABLE IF EXISTS games")
    conn.execute("DROP TABLE IF EXISTS openings")
    conn.execute("DROP TABLE IF EXISTS players")


    # Players: are raw per unique player
    conn.execute("""
        CREATE TABLE players(
                 username   TEXT    PRIMARY KEY NOT NULL,
                 last_rating    INTEGER NOT NULL,
                 total_games    INTEGER NOT NULL DEFAULT 0
        )
    """)

    # Openings: one row per unique opening code.
    conn.execute("""
        CREATE TABLE openings (
            opening_code    TEXT PRIMARY KEY NOT NULL,
            opening_shotname    TEXT NOT NULL,
            opening_fullname    TEXT NOT NULL
        )
    """)
    # Games: The core table
    # White_id and Balck_id are foreign keys to players.username
    # Opening_code is a foreign key to openings.opening_code
    # I gonna keep the ratings even though in normalizatio we can derive them from players.
    # This is a delibrte de-normalization for analytical convenience.
    conn.execute("""
        CREATE TABLE games(
            game_id         INTEGER PRIMARY KEY NOT NULL,
            white_id        TEXT    NOT NULL
                                REFERENCES players(username),
            black_id        TEXT    NOT NULL
                                REFERENCES players(username),
            winner          TEXT    NOT NULL
                                CHECK(winner IN('White', 'Black', 'Draw')),
            victory_status  TEXT    NOT NULL,
            turns           INTEGER NOT NULL
                                CHECK(turns >= 1),
            time_increment  TEXT    NOT NULL,
            rated           INTEGER NOT NULL
                                CHECK(rated in (0, 1)),
            opening_code    TEXT    NOT NULL
                                REFERENCES openings(opening_code),
            white_rating    INTEGER NOT NULL,
            black_rating    INTEGER NOT NULL
        )
    """)








