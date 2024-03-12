# EMLoT Static Site Creation Tools
This repo contains the files that have been created to enable a static publication of EMLoT.  Most of the code here supports the creation of the searching/browsing mechanisms which can be found in the static site at /db/browse: the "Keyword Search" and "Browse" (a facetted browsing mechanism) tabs.

The work involved coding in two areas:
* First, data had to be extracted from the EMLoT MySQL database and turned into JSON (packaged within JavaScript files). These Python scripts can be found in the "src" folder.
* Then, Javascript coding had to be incorporated into HTML pages in the EMLoT presentation that could exploit this formulation and provide a mechanism that could run both the keyword search and facetted browse facilities. These can be found in the "web" folder: most specifically the HTML in web/db/browser and web/db/keyword-search, and the Javascript code in web/db/js.

## Connection to the MySQL database
Almost all the Python scripts provided here have to job of pulling data from the EMLoT MySQL data.  Thus, they need a MySQL connection. A very simple standardized mechanism has been thus put into each script that needs it.  The routine "getConnection(itm)" reads connection data from a JSON file and returns a MySQL database connection. The location of this file is specified by the global variable "db_credentials" which will need to be edited so that it points to the right location.  This will need to be changed in *all* scripts that use a MySQL connection.

The JSON file looks like this (replace material in <> with information relevent to your situation):
```
    {  
        "emlot": {  
            "host": "<location>",  
            "user": "<MySQL user name>",  
            "password": "<MySQL password>",  
            "db": "<MySQL database name>"  
        }  
    }
```

## Data extraction tools
To allow the Keyword Search and facetted Browsing mechanisms to work, the data that controls them has to be taken from the EMLoT database and turned into material that can sit alongside the HTML files in the static site.  The Python scripts that do this are in the "src" folder, and there are two types of scripts for this purpose:
* The scripts named xxx2json.py (where xxx is replaced with the name of the type of data) creates JSON files that contain information that is needed to generate the lists of items that appears in the Browse and KeyWord Search pages on the right hand side.  These files also contain textual information which provides the basis for the keyword search.  Unfortunately, what is needed to create each type of file varies bewteen the file types, so there is one script specific to the generation of each type of data needed.
* The script named facet-maker.py extracts the data necessary to support the facetted browsing mechanism. A single script can generate all the data needed for all types of facetted search result types.
* The script EmLOTNames.py generates JSON data that allows an id number to be mapped to a display name for Persons, Troupes and Venues.
* The script cleanup.py reads through the HTML pages in the generated EMLoT site and removes material that, although supported in the online version of EMLoT (such as the workspace) is not available in the static site.
* The script qtidy.py is used to clean up SQL queries into the form in which they appear here.

The various JSON files created by these scripts are all wrapped in a little bit of JavaScript so that they can be specified in the browser as JS files.  This is done to avoid security restrictions imposed (unnecessarily here) for URLs beginning file:.

##

John Bradley (john.bradley@kcl.ac.uk)
