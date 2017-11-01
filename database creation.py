import sqlite3 as lite
import sys

# Change database location
sqlite_file = 'C:/Users/User/OneDrive/Universiteit/Module 9/Week 9 - final project/Flask/project.db'

# TODO add start and end date
people = (
    ("Hans", "Jansen", "Laadakkdja;ldja;kn 10", "7210 AH", "Timboektoe", 1010110101001),
    ("Eva", "Jansen", "Laan 10", "7210 AH", "Timboektoe", 1010110101001),
    ("Sofie", "Jansen", "Laan 10", "7210 AH", "Timboektoe", 1010110101001),
    ("Jan", "Jansen", "Laan 10", "7210 AH", "Timboektoe", 1010110101001),
)

con = lite.connect(sqlite_file)

with con:
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS userlist")

    cur.execute(
        "CREATE TABLE userlist(firstname TEXT, lastname TEXT,address TEXT, postalcode TEXT,city TEXT, rfid INTEGER)")

    cur.executemany("INSERT INTO userlist VALUES(?, ?, ?, ?, ?, ?)", people)
