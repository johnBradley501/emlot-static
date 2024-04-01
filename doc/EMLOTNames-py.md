# Information about EmLOTNames.py

The data provided to the Javascript code that populates the right-hand area of the Browse and Keyword Search pages (the list of items), contains pointers to associated people, venues and troupes in the form of their ids, but this needs to be turned into links attached to the name of the person/venue/toupe.  The purpose of this code is to generate mapping mechanisms expressed as a JSON object that, given an id, returns the name for that entity.  From the name and the id, the Javascript code is then able to generate a working link.

EmLOTNames.py does this by running SQL queries against the people, venue and troupe entities that fetch all the names with their associated ids, and stores them in three JSON objects.  These are then each wrapped in a little bit of Javascript and saved in the output file `pvtdata.js`.

## Python-MySQL connection module.
This script uses `mysqlclient` as its module (which supports "`import MySQLdb`") to enable MySQL querying.  Like most things Python, it can be installed using pip.  The version I have when this page was created was 2.2.0, but probably almost any version will work.

## The generated pvtdata.js file
Here is an overview of what the file this script creates looks like:
```
function getPersonNames(){return {"1": "Young, William", "3": "Wright, James", "4": "Pavy, Salomon", "5": "Alleyn, Edward", "7": "Fitzstephen, William", "9": "Stow, John", (...) "3234": "Bartholmew, John", "3235": "May, William", "3236": "Goldinge, Ambrose"}
; }

function getTroupeNames(){return {"1": "Admiral's Men", "2": "Queen's Men", "3": "Worcester's Men (1589-1603)", "4": "Prince Henry's Men", "5": "King's Men (1603-1625)", (...) "160": "Gentlemen of the Inns of Court", "161": "the Clergy and Scholars of St Paul's", "163": "Children of Paul's (II)"}
; }

function getVenueNames(){return {"1": "Rose", "2": "Theatre", "3": "Newington Butts", "4": "Fortune (I)", "5": "Curtain", "6": "Whitefriars", "7": "Globe (I)", "9": "Court", (...)  "118": "Cross Keys", "125": "Paris Garden", "127": "playhouse"}
; }
```

... with, of course, the middle of each list left out (indicated by "\(...\)" in this illustration.

The generated .js file can thus be included with a "<script" tag, and in the Javascript code the mapping mechanism from id to name can be fetched by invoking `getPersonNames()`, `getTroupeNames()` and `getVenueNames()`

## Before running an EmLOTNames.py script
Before you can run this script you will probably need to make two changes to it:
* First,  you need to give information that will allow it to connect to the EMLoT database.  As described on [the front page of this repo](./README.md), you need to create a file containing MySQL credentials that will provide database access and store it somewhere.  Then, set the path and file name to it in variable "`db_credentials`" which can be found near the top of this script.
* Then, you need to specify where the script is to store the JS/JSON file `pvtdata.js` that it will create.  Edit variable "`workdir`" which can be found near the top of this script.
