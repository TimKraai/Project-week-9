## import the serial library
import serial
from time import sleep
import sqlite3 as lite
import sys
import datetime

#----------------------- Connection with the Arduino -------------------
serin = 0
ser = serial.Serial('com7', 9600)
UID = ''

## loop until the arduino tells us it is ready
while serin != b'1':
    print("Waiting for initialisation of Arduino")
    serin = ser.read()
print("initialised")
ser.write(b'0')
counter = 0
UID = []
while counter < 4:
    UID.append(str(ser.read()))
    sleep(0.1)
    counter += 1
UIDstr = ""
g = 0
while g < len(UID) :
    UIDstr += UID[g][4]
    UIDstr += UID[g][5]
    g += 1
UIDbin = bin(int(UIDstr, 16))[2:].zfill(32)
print(UIDbin)

"""
ser.write(b'0')
if acces = granted:
    ser.write(b'1')
else:
    ser.write(b'0')
"""
#ser.close()

#----------------------- Creating the database -------------------]

import sqlite3 as lite
import sys

# Change database location
sqlite_file = 'C:/Users/User/OneDrive/Universiteit/Module 9/Week 9 - final project/Flask/project.db'

people = (
    ("Hans", 1010110101001, 1, "2017-10-07", "2019-10-07"),
    ("Hans", 1010110101011, 2, "2017-10-07", "2019-10-07"),
    ("Eva", 1010110101101, 2, "2017-10-07", "2019-10-07"),
)

con = lite.connect(sqlite_file)

with con:
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Houses")
    cur.execute("DROP TABLE IF EXISTS Doors")
    cur.execute("DROP TABLE IF EXISTS Residents")
    cur.execute("DROP TABLE IF EXISTS Authorization")

    cur.execute("CREATE TABLE Houses (House_id INTEGER, Street TEXT, Number TEXT, Postal_code TEXT, City TEXT, PRIMARY KEY(House_id))")
    cur.execute("CREATE TABLE Doors(Door_id INTEGER, Door_name TEXT, House_id INTEGER, PRIMARY KEY(`Door_id`))")
    cur.execute("CREATE TABLE Residents(Resident_id INTEGER, Name TEXT,RFID INTEGER,House_id INTEGER, PRIMARY KEY(Resident_id))")
    cur.execute("CREATE TABLE Authorization (Name TEXT, RFID INTEGER, Authorized for INTEGER, Start_date TEXT, End_date TEXT, PRIMARY KEY(RFID, Authorized))")

    cur.executemany("INSERT INTO Authorization VALUES(?, ?, ?, ?, ?)", people)


#----------------------- Checking the authorization -------------------]

#RFID received from the scan
myrfid = 1010110101001
#The door id received from the scan
doorid = 1

#Access set to false initialy
Access = False
#get date
date = datetime.datetime.now().strftime("%Y-%m-%d")

#path to the database file
sqlite_file = 'C:/Users/User/OneDrive/Universiteit/Module 9/Week 9 - final project/Code/project.db'

#connect to the database
con = lite.connect(sqlite_file)

#when connected do the following:
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM Authorization WHERE RFID=? AND Authorized=?", (myrfid, doorid))

    #prints the output of the SQL statement above
    output = cur.fetchone()
    print(output)

    if not output:
        Access = False
    else:
        #Get start and end date from the output and checks the authorization period
        start_date = output[3]
        end_date = output[4]
        if (date >= start_date) and (date <= end_date):
            Access = True

    print(Access)
