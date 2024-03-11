import MySQLdb
import json
import re
# https://github.com/PyMySQL/mysqlclient/blob/main/doc/user_guide.rst#mysqldb-mysql

db_credentials = "c:/usr/local/etc/mysql/connection.json"
pretty = False
making="venue"

facets = ["event", "people", "prisources", "records", "secsources", "troupe", "venue"]

def getConnection(itm):
    infile = open(db_credentials, "r",encoding='utf-8')
    cred = json.loads(infile.read())
    infile.close()
    cdata = cred[itm]
    return MySQLdb.connect(cdata["host"], cdata["user"], cdata["password"], cdata["db"])

inputdir = "D:/data/workspace/emlot-export/input/"
outputdir = "D:/data/workspace/emlot-export/data/"

dbConnection = getConnection("emlot")
cursor = dbConnection.cursor()


def processList(cursor, query):
    cursor.execute(query)
    rslt = {}
    for vals in cursor:
        name=vals[0]
        id = vals[1]
        if id:
            if name not in rslt:
                rslt[name] = []
            rslt[name].append(int(id))
    lst = []
    for name in rslt:
        lst.append([name, rslt[name]])
    return lst


def makeFacet(fName):
    infileName = inputdir+"facets-"+fName+".json"
    outfileName = outputdir+"facets-"+fName+".js"
    infile = open(infileName, "r",encoding='utf-8')
    data = json.loads(infile.read());
    infile.close()

    ftype = data[0]
    print("Working with: "+ftype)

    for toplevel in data[1]:
        print("Top Level: "+toplevel[0])
        for category in toplevel[2]:
            print("   Category: "+category[0])
            cdata = category[1]
            q = ""
            sep = ""
            if "q" in cdata:
                for part in cdata["q"]:
                    q = q+sep+part
                    sep = "\n"
                rslt = processList(cursor, q)
                if not pretty:
                    cdata.pop("q")
                cdata["i"]=rslt

    if pretty:
        outdata = json.dumps(data, indent=4)
        outdata = re.sub(r"(\d),\s+", r"\1, ", outdata)
    else:
        outdata = json.dumps(data)

    outfile = open(outfileName, "w",encoding='utf-8')
    outfile.write("function getFacetData(){ return ")
    outfile.write(outdata)
    outfile.write("; }")
    outfile.close()
    
if making=="all":
    for fac in facets:
        makeFacet(fac)
else:
    makeFacet(making)