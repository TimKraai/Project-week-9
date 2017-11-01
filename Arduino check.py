## import the serial library
import serial
from time import sleep
import sqlite3 as lite
import sys
import datetime
import sqlite3 as lite
import sys

# Before you start change the database location to the correct path
# Select the correct Com output for the Arduino



## Creating the database
# database location
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

    cur.execute("CREATE TABLE userlist(firstname TEXT, lastname TEXT,address TEXT, postalcode TEXT,city TEXT, rfid INTEGER)")

    cur.executemany("INSERT INTO userlist VALUES(?, ?, ?, ?, ?, ?)", people)

## connecting to Arduino
serin = 0
ser = serial.Serial('com7', 9600)
## loop until the arduino tells us it is ready
while serin != b'1':
    print("Waiting for initialisation of Arduino")
    serin = ser.read()
print("initialised")
ser.write(b'0')
## Receive UID when scanned
counter = 0
UID = []
while counter < 4:
    UID.append(str(ser.read()))
    sleep(0.1)
    counter += 1
UIDstr = ""
g = 0
while g < len(UID) :
    if len(UID[g]) != 8 :
        UIDstr += format(ord(UID[g][len(UID[g])-2]), "x")
    else:
        UIDstr += UID[g][len(UID[g])-3]
        UIDstr += UID[g][len(UID[g])-2]
    g += 1
UIDbin = bin(int(UIDstr, 16))[2:].zfill(32)
print("UID recognised:")
print(UIDbin)


#----------------------- Checking the authorization -------------------]

#RFID received from the scan
myrfid = UIDbin
#The door id received from the scan
doorid = 1

#Access set to false initialy
Access = False
#get date
date = datetime.datetime.now().strftime("%Y-%m-%d")

#connect to the database
con = lite.connect(sqlite_file)

#when connected do the following:
with con:
    cur = con.cursor()
    # maybe add authorization check for different doors (AND Authorized=?)
    cur.execute("SELECT * FROM userlist WHERE rfid=? ", myrfid)

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
