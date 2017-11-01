import sqlite3 as lite
import sys
import datetime

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

