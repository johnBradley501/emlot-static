import MySQLdb
import json
import re
# https://github.com/PyMySQL/mysqlclient/blob/main/doc/user_guide.rst#mysqldb-mysql

db_credentials = "c:/usr/local/etc/mysql/connection.json"

def getConnection(itm):
    infile = open(db_credentials, "r",encoding='utf-8')
    cred = json.loads(infile.read())
    infile.close()
    cdata = cred[itm]
    return MySQLdb.connect(cdata["host"], cdata["user"], cdata["password"], cdata["db"])

workdir = "D:/data/workspace/emlot-export/data/"
outfileName = workdir+"ptvdata.js"

def fetchPersonNames(cursor):
    rslt={}
    cursor.execute("SELECT id, name, surname, altname FROM ltbapp_person")
    for r in cursor:
        (id, name, surname, altname) = r
        id = int(id)
        if not name:
            name = "---"
        displayName = surname+", "+name
        if re.findall(r",",name):
            parts = re.split(r", *", name)
            displayName = surname+", "+parts[0]
        rslt[id] = displayName
    return rslt;

def fetchTroupeNames(cursor):
    rslt={}
    cursor.execute("SELECT id, name FROM ltbapp_troupe")
    for r in cursor:
        (id, name) = r
        id = int(id)
        rslt[id] = name
    return rslt;


def fetchVenueNames(cursor):
    rslt={}
    cursor.execute("SELECT id, name FROM ltbapp_venue")
    for r in cursor:
        (id, name) = r
        id = int(id)
        rslt[id] = name
    return rslt;

def buildNameFiles(cursor):
    outfile = open(outfileName, "w",encoding='utf-8')
    
    data = fetchPersonNames(cursor)
    outfile.write("function getPersonNames(){return ")
    outfile.write(json.dumps(data))
    outfile.write("\n; }\n\n")
     
    data = fetchTroupeNames(cursor)
    outfile.write("function getTroupeNames(){return ")
    outfile.write(json.dumps(data))
    outfile.write("\n; }\n\n")

    data = fetchVenueNames(cursor)
    outfile.write("function getVenueNames(){return ")
    outfile.write(json.dumps(data))
    outfile.write("\n; }\n\n")
    
    outfile.close()
    
dbConnection = getConnection("emlot")
cursor = dbConnection.cursor()
buildNameFiles(cursor)
dbConnection.close()

