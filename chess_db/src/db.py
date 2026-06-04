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

    conn.execute("DROP TABLE IF EXISTS games")
    conn.execute("DROP TABLE IF EXISTS openings")
    conn.execute("DROP TABLE IF EXISTS players")








