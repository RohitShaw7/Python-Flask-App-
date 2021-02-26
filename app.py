from flask import Flask, render_template, request, flash
import mysql.connector
from mysql.connector import errorcode, cursor

# Obtain connection string information from the portal

config = {
    'host': 'myserver10.mysql.database.azure.com',
    'user': 'rootadmin@myserver10',
    'password': 'Rt7129#00000',
    'database': 'studentdb'
}

try:
    conn = mysql.connector.connect(**config)
    print("Connection established")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with the user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = conn.cursor()


def read_data(rollid):
    if rollid == "":
        cursor.execute("SELECT * FROM studentdb.dataset;")
    else:
        # Read data
        cursor.execute("SELECT * FROM studentdb.dataset where rollID = (%s);" % (str(rollid)))
    rows = cursor.fetchall()
    return rows


def insert_data(fname, lname, email, rollid):
    cursor.execute("INSERT INTO studentdb.dataset (firstName,lastName,emailID,rollID) VALUES ('%s','%s','%s','%s');" % (
        str(fname), str(lname), str(email), str(rollid)))
    flash("Data inserted")
    conn.commit()


def delete_data(rollid):
    # Delete a data row in the table
    cursor.execute("DELETE FROM studentdb.dataset WHERE rollID = ('%s');" % (str(rollid)))
    flash("Data deleted")
    conn.commit()


def update_data(rollid, fname):
    # Update a data row in the table
    cursor.execute("UPDATE studentdb.dataset SET firstName = ('%s') WHERE rollID = ('%s');" % (str(fname), str(rollid)))
    flash("Data updated")
    conn.commit()


app = Flask(__name__)
app.secret_key = 'Rt7129#00000'


@app.route('/')
def home():
    return '''<a href="/insert">INSERT</a></br> <a href="/read">READ</a><br><a href="/update">UPDATE</a><br><a
    href="/delete">DELETE</a><br> '''


@app.route('/insert', methods=['POST', 'GET'])
def insert():
    return render_template('insert.html')


@app.route('/insertdata', methods=['POST', 'GET'])
def insertdata():
    rollid = request.args['rollid']
    f = request.args['fname']
    ll = request.args['lname']
    e = request.args['email']
    insert_data(f, ll, e, rollid)
    return render_template('data.html', rows=read_data(''))


@app.route('/read', methods=['POST', 'GET'])
def read():
    return render_template('read.html')


@app.route('/update', methods=['POST', 'GET'])
def update():
    return render_template('update.html')


@app.route('/updatedata', methods=['POST', 'GET'])
def updatedata():
    rollid = request.args['rollid']
    f = request.args['fname']
    update_data(rollid, f)
    return render_template('data.html', rows=read_data(''))


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    return render_template('delete.html')


@app.route('/deletedata', methods=['POST', 'GET'])
def deletedata():
    rollid = request.args['rollid']
    delete_data(rollid)
    return render_template('data.html', rows=read_data(''))


@app.route('/data')
def data():
    rollid = request.args['rollid']
    if rollid == '':
        return 'Data Missing'
    else:
        return render_template('data.html', rows=read_data(rollid))


if __name__ == '__main__':
    app.run(debug=True)

cursor.close()
conn.close()
