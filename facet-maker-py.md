# Information about facet-maker.py

The Javascript facetted browsing mechanism requires information about the facets for each kind of primary Entity type that it supports: facets-event.js provides the necessary facet data for for events, facets-people.js for people, etc.  In this it is like the keyword search mechanism.  However, unlike the keyword search case, a single script `facet-maker.py` handles the generation of all of them: a parameter set near the front of the script establishes which one is to be produced (or asks for them all to be done in one run). Of this more later.

## Python-MySQL connection module.
This script uses `mysqlclient` as its module (which supports "`import MySQLdb`") to enable MySQL querying.  Like most things Python, it can be installed using pip.  The version I have when this page was created was 2.2.0, but probably almost any version will work.

## The input file
There is, in the folder "input", JSON files that tell facet-maker.py how to generate the data needed for the facets: "input/facets-event.json" provides information needed to create the output file "web/data/facets-event.js", for all facets related to events.  Similarly, "input/facets-people.json" tells facet-maker.py how to generate the facet data for all facets related to people (and stored in "web/data/facets-people.js"

Here is the beginning of the facets-event.json:
```
[
    "event",
    [
        ["Event & Person",
            "This category contains facets classifying EMLoT's events and people.",
            [
                ["Event Type",{
                    "t": "s",
                    "q": [
                        "SELECT DISTINCT et.name, eet.event_id, CASE WHEN ev.devent_from_year is null THEN ev.devent_to_year ELSE ev.devent_from_year END AS Year, ev.short_title",
                        "FROM ltbapp_eventtype  as et, ltbapp_event_event_type as eet, ltbapp_event as ev",
                        "WHERE et.id = eet.eventtype_id AND ev.id = eet.event_id",
                        "ORDER BY et.name, Year, ev.short_title"
                    ],
                    "h": "Contains a list that includes types of performance activity and primary sources and other subjects of relevance for London's theatrical world (for example, Arrest)."
                }],
                ["Event Date",{
                    "t": "n",
                    "q": [
                        "SELECT CASE WHEN ev.devent_from_year is null THEN ev.devent_to_year ELSE ev.devent_from_year END AS Year, ev.id, ev.short_title", 
                        "FROM ltbapp_event as ev",
                        "HAVING Year Is Not Null",
                        "ORDER BY Year, ev.short_title"
                        ],
                    "h": "Contains a list of years when events recorded in EMLoT happened."
                }],

(etc...)
```

* As one can see, the input file is structured as a hierarchy of Facet groups and individual Facets that matches the hierarchical display the user sees.
* For each individual facet, e.g. "`Event Type`", a JSON object provides information about that particular Facet.
* The "t" item specifies a facet type, and is either "s" or "n". Perhaps "d" (for "date") might have been better than "n"
* The "q" item provides an SQL query that fetches the data from the MySQL database for that particular facet.
* The "h" item provides a bit of help text that is to be displayed if the user hovers the mouse pointer over the help icon.

## What is produced
If facet-maker.py is asked to generate "event" facet data, it will create the file "facets-event.js", which looks like this:

```
function getFacetData(){ return [
    "event",
    [
        [
            "Event & Person",
            "This category contains facets classifying EMLoT's events and people.",
            [
                [
                    "Event Type",
                    {
                        "t": "s",
                        "h": "Contains a list that includes types of performance activity and primary sources and other subjects of relevance for London's theatrical world (for example, Arrest).",
                        "i": [
                            [
                                "advertisement", [ 3790 ]
                            ],
                            [
                                "animal baiting", [ 7570, 7780, 7705, 7709, 7710 ]
                            ],
                            [
                                "animal entertainment", [ 7486 ]
                            ],
                            [
                                "anti-theatrical comment", [ 4059, 7645, 698, 700, 745, 4297, 725, 5327, 415, 727, 4079, 4100, 7569, 6427, 4101, 7547, 3527, 5706, 771, 491, 1810, 7729, 490, 3390, 2891, 4008, 4113, 5252, 690, 678, 3946, 7676, 7875, 7950, 4209, 791, 7309, 792 ]
                            ],
... etc, ending with

]
; }
```

A few things to note about this:
* The generated JSON is wrapped in a bit of Javascript (the first two lines, and the last line) so that it can be incorporated into EMLoT's web pages where it is needed with an HTML "<script..." tag.
* Like the input JSON file, the structure is hierarchical, and contains much of the data that was present in the input file. However...
* The SQL query in "q" is now omitted: it is not needed in the static web processing.
* One new item ("i") has been added, which contains the results of the processing of the SQL queries against the database.
* Item "i" is again a JSON array: one entry for each facet value.
* Each item in "i"'s JSON array is made up the facet value name, followed by a list of IDs that are associated with it (drawn from the results of the SQL query): "advertisement" has only one associated event, with id 3790; "animal baiting" has 5 events, with ids 7570, 7780, 7705, 7709, 7710, etc.

## Before running facet-maker.py script
Before you can run this script you need to make a few changes to it:
* First,  you need to give information that will allow it to connect to the EMLoT database.  As described on [the front page of this repo](./README.md), you need to create a file containing MySQL credentials that will provide database access and store it somewhere.  Then, set the path and file name to it in variable "`db_credentials`" which can be found near the top of this script.
* Next, set the "pretty" variable.  If set "True" it causes the script to generate JSON output which is indented and easier to read.  If False, the data is packed in, so the output JSON/JS file is somewhat smaller.  The "non-pretty" format is perfectly usable in the static web context.
* Next, the "making" variable specifies which set of facets you wish to generate.  Put "all" here to get facet-maker to generate all the files.  Otherwise, change the making value to match one of the names shown in the Python list "facets" (just below) to get only a particular one generated: e.g. `making="troupe"` for making facets for troupes only.  (My apologies for the "number inconsistency" in the names: singular "event", "troupe" and "venue", but plural "people", "records" etc.)

* Then, you must specify a path to the folder where the input JSON files are to be found (in "inputdir"), and where the output JS/JSON file is to be created (in "outputdir").
