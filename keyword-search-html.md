# Introduction to keyword search HTML files

The HTML files in this repo at `web/db/keyword-search` provide the set of files that need to be incorporated into the collection of files that make up the static pages (at `/db/keyword-search`.  They provide the Javascript-driven active keyword searching component to the site.  Note that there are 6 of them -- one for each type of EMLoT data item for which keyword searching is provided.  One is called `index.html`, and thus acts as the first page a user sees when they enter the keyword searching area of the site.  It provides keyword seaching for events.  The other pages are named to identify the type of item that they support for keyword searching: `people.html` searches people, `prisources.html` searches primary sources, etc.

In the rest of this page we will focus on the `index.html` page, which supports searching of events.  All the other pages differ only in changes needed to allow them to support their own type of data.

## Included Javascript files
Like most of the files in the EMLoT static pages, the visual design of the page is managed by references to stylesheets and some javascript files.  We will ignore these "styling" references in this discription.  The script tags that support the Javascript-based keyword searching are referenced in this way:
```
<script type="text/javascript" src="../js/fuse.js"></script>
<script type="text/javascript" src="../data/ks-events.js"></script>
<script type="text/javascript" src="../data/ptvdata.js"></script>
<script type="text/javascript" src="../js/listdispl.js"></script>
<script type="text/javascript" src="../js/ksearch.js"></script>
```

* `fuse.js` contains the javascript that defines the Fuse engine that we use for text searching.
* `ks-events.js` is packaged as a javascript file and contains the JSON data needed for keyword searching and display of selected items.  It is created by the python script `events2json.py` that is in this repo in the `src` folder.  Both the Javascript file that enables the user interaction (`ksearch.js`) and the Javascript file that displays results (`listdispl.js`) expect to find the material provided in this file. For other HTML pages that manage keyword search on other objects, the other "ks" files must be specified here: `ks-people.js` for people, for example.
* `ptvdata.js` provides JSON data that supports the mapping of ids for Persons, Troupes and Venues into their names.  A name for these things are needed when an ID for one of them needs to be turned into a link.
* `listdispl.js` contains the javascript used to manage the tabular display of items in the right-hand side of the keyword search pages.
* `ksearch.js` contains the javascript needed to support user interaction, to run the queries against the fuse engine, and to process the results to feed them to `listdispl.js` functions

## Setting up the interaction in Javascript
Following the \<script tags that load the data and js files is a block of embedded javascript that sets up the environment so the whole thing can work:
```
<script type="text/javascript">
	setup("Event", getEventData(), 4, 6);
	setItemRelativeURL("../record/event/");
	
	defineRowFunction(function (item){
		let [id, recDate, evDate, title, text, persons, troupes, venues] = item;
		if(title.trim()=="undefined" || title.trim()=="")return;
		rslt = "<tr><td>"+displayItemTitle(id, title)
					+"</td><td>"+displayList(venues, venueNames, venueRelativeURL)
					+"</td><td>"+displayList(troupes, troupeNames, troupeRelativeURL)
					+"</td><td>"+displayList(persons, personNames, personRelativeURL)
					+"</td><td>"+evDate+"</td><td>"+recDate+"</td></tr>\n";
		return rslt;
	});
</script>
```
* First, is the call to the `setup` function (defined in `ksearch.js`. The parameters are, first, the name of the type of item being searched here (used for various display purposes), followed by a call to `getEventData()`.  This function is defined in `ks-events.js`, and holds the JSON data about the items this page works with (here, events).  The 3rd parameter identifies the item in each item list that contains the text that fuse is to work with (it is zero based, so 4 points to the 5th item). The final number is the number of columns in the display of items that `listdispl.js` will be creating. This could have been calculated, but I was too lazy to do that.
* Following setup is a call to `setItemRelativeURL()` (defined in `listdispl.js`) that specifiess what the relative URL should start with to generate a link to information about items (here event items).
* Finally, `defineRowFunction()` (defined in `listdispl.js`) is called with a function that `listdispl.js` will use to generate a tabular row for each item (here event item) that it displays. Note the use of `displayList()` (provided by `listdispl.js` which can turn a list of IDs (first parameter) into a list of HTML "A" links.

Note that near the bottom of this page is a small script element that invokes `init()` (defined in `listdispl.js`) to get the whole thing started up.

## Key identified spots in the HTML body
`listdispl.js` and `ksearch.js` expect certain spots in the body of the HTML to be identified with IDs.  These are the places where the script will insert dynamic material that the user will see:
* id `rslts`: marks the spot where `listdispl.js` is to insert the list of items it is asked to display
* ids `topbuttons" and `bottombuttons`: marks the places where the pagination buttons that `listdispl.js` generates are to be inserted.
* ids `topPositionLabel` and `bottomPositionLabel`: marks the places where the information about which block of items are being displayed are to be placed.
* id `headingText`: marks the spot where `ksearch.js` is to put the heading for the list of results.
* id `bs_input`: marks the form input element where the user specifies the text for searching.
