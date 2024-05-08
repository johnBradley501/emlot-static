# Overview of emlot-static

The work to build this browser-only search/browsing mechanism involved coding in two areas:
* First, data had to be extracted from the EMLoT MySQL database and turned into JSON (packaged within JavaScript files). The Python scripts that did this can be found in the "src" folder.
* Then, Javascript coding had to be incorporated into HTML pages in the EMLoT presentation that could exploit this formulation of data (created in the step just mentioned) and use it to support both the keyword search and facetted browse facilities. This Javascript can be found in this repo in the "web" folder: most specifically the HTML files in `web/db/browser` and `web/db/keyword-search`, and the Javascript code they make use of in `web/db/js`.

In the end, the JSON data extracted by the python scripts mentioned in the first step are put together with the Javascript material mentioned in the second, and inserted into the bundle of files that make up the EMLoT static website.  The Python script files that created the JSON data do this job only, and once they have been run will not need to be incorporated into the EMLoT static site itself.

## Connection to the MySQL database
Almost all the Python scripts provided here have to job of pulling data from the EMLoT MySQL data.  Thus, they need a MySQL connection. A very simple standardized mechanism has been thus put into each Python script that needs it.  The routine "getConnection(itm)" reads connection data from a JSON file and returns a MySQL database connection. The location of this file is specified by the global variable "db_credentials" which will need to be edited so that it points to the right location for your particualr use.  This variable will need to be changed in *all* scripts that use a MySQL connection.

The JSON file that provides the MySQL credentials looks like this (replace material in <> with information relevent to your situation):
```
    {  
        "emlot": {  
            "host": "<MySQL server location>",  
            "user": "<MySQL user name>",  
            "password": "<MySQL password>",  
            "db": "<MySQL database name>"  
        }  
    }
```

## Data extraction tools
To allow the Keyword Search and facetted Browsing mechanisms to work, the data that controls them has to be taken from the EMLoT database and turned into JSON material that can sit alongside the HTML files in the static site.  The Python scripts that do this are in the "src" folder, and there are several types of scripts for this purpose:
* The scripts named **xxx2json.py** (where xxx is replaced with the name of the entity type being proessed) creates JSON files that contain information that is needed to generate the lists of items that appears in the Browse and KeyWord Search pages on the right hand side.  These files also contain textual information which provides the basis to enable the keyword search.  Unfortunately, what is needed to create each type of file varies between the file types, so there is one script specific to the generation of each type of data needed. [More information](./xxx2json-py.md)
* The script named **facet-maker.py** extracts the data necessary to support the facetted browsing mechanism. A single script can generate all the data needed for all types of facetted search result types -- however, files in folder "input" are read by this script to tell it how to do its job for a particular type of data. [More information](./facet-maker-py.md)
* The script **EmLOTNames.py** generates JSON data that allows an id number to be mapped to a display name for Persons, Troupes and Venues. [More information](./EMLOTNames-py.md)
* The scripts **cleanup.py** and **troupe-cleanup.py** read through the HTML pages in the generated EMLoT site and, using regular expressions, removes material that, although supported in the online version of EMLoT is not available in the static site.  **cleanup.py** focuses primarily on removing top-of-page tab links to things such as "Track a Bear" or the workspace that are no longer available.  **troupe-cleanup.py** removes links from the troupe display pages created by sitesucker to REED's P&P site.
* The script **qtidy.py** was used to clean up SQL queries into the form in which they appear here.

The various JSON files created by these scripts are all wrapped in a little bit of JavaScript so that they can be specified for the browser as JS files.  This is done to avoid security restrictions imposed by browsers (unnecessary here) on `file:` like URLs.

## Javascript materials
The browser can carry out the dynamic processing associated with keyword searching and facetted browsing thanks to the Javascript code in folder `/db/js` which is included as part of the EMLoT static page distribution.  The Javascript files are:

* **listdispl.js** supports the display of items on the right side of the browse and keyword search pages.  It also provides pagination of that data. [More information](./listdispl-js.md)
* **ksearch.js** supports the left area of the keyword search pages where users can specify what word to search for. [More information](./ksearch-js.md)
* **browse.js** supports the left area of the Browse search pages to provide facetted searching for users. [More information](./browse-js.md)
* **fuse.js** is the engine used for keywoard searching: https://www.fusejs.io/

## HTML pages for browsing and keyword searching

The HTML pages in the static site folder at `/db/browser` and `/db/keyword-search` make use of the Javascript files in /db/js to make the searching and browsing active.

* [Keyword Search HTML pages](keyword-search-html.md) explains how the Javascript and the data are brought together for the keyword search.
* [Facetted Browser HTML pages](browser-html.md) explains how the Javascript and the data are brought together for the facetted browsing.
