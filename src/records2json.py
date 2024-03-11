'''
Created on Dec 4, 2023

@author: John Bradley
'''
import MySQLdb
import json
# https://github.com/PyMySQL/mysqlclient/blob/main/doc/user_guide.rst#mysqldb-mysql

db_credentials = "c:/usr/local/etc/mysql/connection.json"

def getConnection(itm):
    infile = open(db_credentials, "r",encoding='utf-8')
    cred = json.loads(infile.read())
    infile.close()
    cdata = cred[itm]
    return MySQLdb.connect(cdata["host"], cdata["user"], cdata["password"], cdata["db"])

workdir = "D:/data/workspace/emlot-export/data/ks-"
filenameBase = "records"
outputFilename = workdir+filenameBase+".js"

# db=_mysql.connect(host="localhost",user="bradley", password="mat4thew",database="emlot")
modifiers = {"cir":"circa", "by":"by", "bef":"before", "aft":"after", "lat":"late", "ear":"early", "mid":"middle"}

# notes, undated, eitheror, from_modifier, from_weekday, from_day, from_modifier2,
#from_month, from_season, from_year, to_modifier, to_weekday, to_day, to_modifier2,
#to_month, to_season, to_year, claimsource

date_fields = ["notes", "undated", "eitheror", "from_modifier", "from_weekday", "from_day", "from_modifier2",
               "from_month", "from_season", "from_year", "to_modifier", "to_weekday", "to_day", "to_modifier2",
               "to_month", "to_season", "to_year", "claimsource"]

days_of_week = ["","Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def makeDateFields(prefix):
    sep = ", "+prefix
    rslt = prefix+sep.join(date_fields)
    # print(rslt)
    return rslt

def processDateDetail(modifier, weekday, day, modifier2, month, season, year):
    rslt = ""
    if modifier:
        rslt = rslt+modifiers[modifier]+" "
    if modifier2:
        rslt = rslt+modifiers[modifier2]+" "
    if weekday:
        rslt = rslt+days_of_week[weekday]+" "
    if day:
        rslt = rslt+str(day)+" "
    if month:
        rslt = rslt+months[month]+" "
    if year:
        rslt = rslt+str(year)
    return rslt.strip()

def processDateData(record, start):
    (notes, undated, eitheror, from_modifier, from_weekday, from_day, from_modifier2, from_month, from_season, from_year, to_modifier, to_weekday, to_day, to_modifier2,
    to_month, to_season, to_year, claimsource) = record[start:start+len(date_fields)]
    if undated:
        return "undated"
     
    from_date = processDateDetail(from_modifier, from_weekday, from_day, from_modifier2, from_month, from_season, from_year)
    to_date = processDateDetail(to_modifier, to_weekday, to_day, to_modifier2, to_month, to_season, to_year)
    if eitheror and from_date and to_date:
        return from_date+" OR "+to_date
    rslt = ""
    if from_date: # it appears to date by itself is displayed as "from" instead... JB
        rslt= rslt+"From: "+from_date+" "
        if to_date:
            rslt = rslt+"To: "+to_date
            
    elif to_date:
        rslt = rslt+"From: "+to_date
    else:
        return "..."
    return rslt.strip()

# dbConnection = MySQLdb.connect("localhost","bradley","mat4thew","emlot")
dbConnection = getConnection("emlot")
cursor = dbConnection.cursor()

def buildDocAuthors(cursor):
    rslt = {}
    cursor.execute("SELECT document_id, auth_standard_id FROM ltbapp_docauthors ORDER BY document_id, auth_order")
    for r in cursor:
        doc = r[0]
        person = r[1]
        if(not doc in rslt):
            rslt[doc] = []
        rslt[doc].append(person)
    return rslt

docAuthors = buildDocAuthors(cursor)


#def buildSecondarySourceAuthors(cursor):
#    rslt = {}
#    cursor.execute("SELECT document_id, secauth_standard_id FROM ltbapp_docsecauthors ORDER BY document_id, secauth_order")
#    for r in cursor:
#        doc = r[0]
#        person = r[1]
#        if(not doc in rslt):
#            rslt[doc] = []
#        rslt[doc].append(person)
#    return rslt

#ssourceAuthors = buildSecondarySourceAuthors(cursor)


cursor.execute("SELECT rec.id, rec.src_pagesCited, doc1.id, doc1.title, ev.id, ev.short_title, doc2.id, doc2.title "+
    "FROM ltbapp_record as rec, ltbapp_document as doc1, ltbapp_document as doc2, ltbapp_event as ev "+
    "WHERE doc1.id = rec.source_id AND ev.id = rec.event_id AND rec.transcription_id = doc2.id "+
    "ORDER BY doc1.title, rec.id")
records = []
cnt = 0
for r in cursor:
    cnt += 1
    [recid, pageCited, secId, secTitle, evId, evTitle, priId, priTitle] = r
    items = [recid, pageCited, secId, secTitle, evId, evTitle, priId, priTitle]
    authors = []
    if secId in docAuthors:
        authors = docAuthors[secId]
    items.append(authors)
    authors = []
    if priId in docAuthors: 
        authors = docAuthors[priId]
    items.append(authors)
    records.append(items)
    #print(r[0],"Recorded:"+processDateData(r, 1),"Happened:"+processDateData(r,1 + len(date_fields)),"val=",r[1+2*len(date_fields):])
    # print(r[0], events[r[0]])
dbConnection.close()

print("Count:",cnt)
outfile = open(outputFilename, "w",encoding='utf-8')
outfile.write("function getTranscriptionRecordData(){ return")
outfile.write(json.dumps(records, indent=4))
outfile.write("; }")
outfile.close()


