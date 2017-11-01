from flask import Flask, render_template, request
import sqlite3, os
from flask import g

app = Flask(__name__)

app.database = "project.db"
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'project.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

def connect_db():
    """Connects to the specific database."""
    return sqlite3.connect(app.config['DATABASE'])

# add stuff

@app.route('/')
def hello_world():
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM userlist')
    posts = [dict(firstname=row[0], lastname=row[1], address=row[2], postalcode=row[3], city=row[4], rfid=row[5]) for row in cur.fetchall()]
    g.db.close()
    return render_template("index.html", posts=posts)

@app.route('/result', methods=['POST'])
def result():
    print("triggert")
    # result = request.form
    firstname = request.form.get('inputFirstname')
    lastname = request.form.get('inputLastname')
    address = request.form.get('inputAddress')
    postalcode = request.form.get('inputPC')
    city = request.form.get('inputCity')
    #TODO change rfid
    rfid = 1010010101010000
    print(city)
    g.db = connect_db()
    g.db.execute("INSERT INTO userlist VALUES(?, ?, ?, ?, ?,?)", (firstname, lastname, address, postalcode, city, rfid))
    g.db.commit()
    g.db.close()
    print("checked")
    return hello_world()


@app.route('/houses')
def house():
    # Add the house that is clicked
    return render_template("House_overview.html")

if __name__ == '__main__':
    app.run()



