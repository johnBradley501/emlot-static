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

workdir = "D:/data/workspace/emlot-static/data/ks-"
filenameBase = "events"
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

dbConnection = getConnection("emlot")
cursor = dbConnection.cursor()

def buildEventPersons(cursor):
    rslt = {}
    cursor.execute("SELECT event_id, person_id FROM ltbapp_ass_event_people ORDER BY event_id")
    for r in cursor:
        event = r[0]
        person = r[1]
        if(not event in rslt):
            rslt[event] = []
        rslt[event].append(person)
    return rslt

eventPersons = buildEventPersons(cursor)

def buildEventTroupes(cursor):
    rslt = {}
    cursor.execute("SELECT event_id, troupe_id FROM ltbapp_ass_event_troupes ORDER BY event_id")
    for r in cursor:
        event = r[0]
        troupe = r[1]
        if(not event in rslt):
            rslt[event] = []
        rslt[event].append(troupe)
    return rslt;

eventTroupes = buildEventTroupes(cursor)


def buildEventVenues(cursor):
    rslt = {}
    cursor.execute("SELECT event_id, venue_id FROM ltbapp_ass_event_venues ORDER BY event_id")
    for r in cursor:
        event = r[0]
        venue = r[1]
        if(not event in rslt):
            rslt[event] = []
        rslt[event].append(venue)
    return rslt;

eventVenues = buildEventVenues(cursor)

cursor.execute("SELECT id, "+makeDateFields("drecord_")+", "+makeDateFields("devent_")+", short_title, helper_keywordsearch FROM ltbapp_event "+
    "ORDER BY CASE WHEN devent_from_year is null THEN devent_to_year ELSE devent_from_year END, short_title")
events = []
cnt = 0
for r in cursor:
    cnt += 1
    items = [r[0], processDateData(r, 1), processDateData(r,1 + len(date_fields))]# .extend(r[1+2*len(date_fields):])
    items.extend(r[1+2*len(date_fields):])
    ePersons = []
    if r[0] in eventPersons:
        ePersons = eventPersons[r[0]]
    eTroupes = []
    if r[0] in eventTroupes:
        eTroupes = eventTroupes[r[0]]
    eVenues = []
    if r[0] in eventVenues:
        eVenues = eventVenues[r[0]]
    items.append(ePersons)
    items.append(eTroupes)
    items.append(eVenues)
    events.append(items)
    #print(r[0],"Recorded:"+processDateData(r, 1),"Happened:"+processDateData(r,1 + len(date_fields)),"val=",r[1+2*len(date_fields):])
    # print(r[0], events[r[0]])
dbConnection.close()

print("Count:",cnt)
outfile = open(outputFilename, "w",encoding='utf-8')
outfile.write("function getEventData(){ return")
outfile.write(json.dumps(events)) # , indent=4))
outfile.write("; }")
outfile.close()


