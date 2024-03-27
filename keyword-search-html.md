# Introduction to keyword search HTML files

The HTML files in this repo at `web/db/keyword-search` provide the set of files that need to be incorporated into the collection of files that make up the static pages (at `\db\keyword-search`.  They provide the Javascript-driven active keyword searching component to the site.  Note that there are 6 of them -- one for each type of EMLoT data item for which keyword searching is provided.  One is called `index.html`, and thus acts as the first page a user sees when they enter the keyword searching area of the site.  It provides keyword seaching for events.  The other pages are named to identify the type of item that they support for keyword searching: `people.html` searches people, `prisources.html` searches primary sources, etc.

In the rest of this page we will focus on the `index.html` page, which supports searching of events.  All the other pages differ only in changes needed to allow them to support their own type of data.

# Included Javascript files
Like most of the files in the EMLoT static pages, the visual design of the page is managed by references to stylesheets and some javascript files.  We will ignore these "styling" references in this discription.  The script tags that support the Javascript-based keyword searching are referenced in this way:
```
<script type="text/javascript" src="../js/fuse.js"></script>
<script type="text/javascript" src="../data/ks-events.js"></script>
<script type="text/javascript" src="../data/ptvdata.js"></script>
<script type="text/javascript" src="../js/listdispl.js"></script>
<script type="text/javascript" src="../js/ksearch.js"></script>
```

* `fuse.js` contains the javascript that defines the Fuse engine that we use for text searching.
* `ks-events.js` is packaged as a javascript file and contains the JSON data needed for keyword searching and display of selected items.  It is created by the python script `events2json.py` that is in this repo in the `src` folder.  Both the searching Javascript page and the item display Javascript page expect to find the material provided in this file.
* `ptvdata.js` provides JSON data that supports the mapping of ids for Persons, Troupes and Venues into their names.  A name for these things are needed when an ID for one of them needs to be turned into a link.
* `listdispl.js` contains the javascript used to manage the tabular display of items in the right-hand side of the keyword search pages.
* `ksearch.js` contains the javascript needed to support user interaction, to run the queries against the fuse engine, and to process the results to feed them to `listdispl.js` functions
