# Introduction to facetted browser HTML files

The HTML files in this repo at `web/db/keyword-search` provide the set of files that need to be incorporated into the collection of files that make up the static pages (at `/db/browse`.  They provide the Javascript-driven active keyword searching component to the site.  Note that there are 6 of them -- one for each type of EMLoT data item for which keyword searching is provided.  One is called `index.html`, and thus acts as the first page a user sees when they enter the keyword searching area of the site.  It provides keyword seaching for events.  The other pages are named to identify the type of item that they support for keyword searching: `people.html` searches people, `prisources.html` searches primary sources, etc.

In the rest of this page we will focus on the `index.html` page, which supports searching of events.  All the other pages differ only in changes needed to allow them to support their own type of data.

## Included Javascript files
Like most of the files in the EMLoT static pages, the visual design of the page is managed by references to stylesheets and some javascript files.  We will ignore these "styling" references in this discription.  The script tags that support the Javascript-based keyword searching are referenced in this way:
```
<script type="text/javascript" src="../data/ks-events.js"></script>
<script type="text/javascript" src="../data/ptvdata.js"></script>
<script type="text/javascript" src="../data/facets-event.js"></script>
<script type="text/javascript" src="../js/listdispl.js"></script>
<script type="text/javascript" src="../js/browse.js"></script>
```
* `ks-events.js` is packaged as a javascript file and contains the JSON data needed for the display of selected items.  It is created by the python script `events2json.py` that is in this repo in the `src` folder.  Both the Javascript file that enables the user interaction (`browse.js`) and the Javascript file that displays results (`listdispl.js`) expect to find the material provided in this file. For other HTML pages that manage keyword search on other objects, the other "ks" files must be specified here: `ks-people.js` for people, for example.
* `ptvdata.js` provides JSON data that supports the mapping of ids for Persons, Troupes and Venues into their names.  A name for these things are needed when an ID for one of them needs to be turned into a link.
* `facets-event.js` contains a JSON representation (lightly wrapped in a bit of Javascript) of the data about the facets.  This file is specifically about events, and there are other files (eg `facets-people.js`, etc) that provide the facet data that are included to support the other facet searching pages that are provided (e.g. `people.html`)
* `listdispl.js` contains the javascript used to manage the tabular display of items in the right-hand side of the keyword search pages.
* `browse.js` contains the javascript needed to support user interaction, to manage the facet filtering, and to process the results to feed them to `listdispl.js` functions

## Setting up the interaction in Javascript
Following the \<script tags that load the data and js files is a block of embedded javascript that sets up the environment so the whole thing can work:
```
	facetSetup("Event", getEventData(), 6);
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
```
* First, is the call to the `facetSetup` function (defined in `browse.js`. The parameters are, first, the name of the type of item being searched here (used for various display purposes), followed by a call to `getEventData()`.  This function is defined in `ks-events.js`, and holds the JSON data about the items this page works with (here, events).  The 3rd parameter is the number of columns in the display of items that `listdispl.js` will be creating. This could have been calculated, but I was too lazy to do that.
* Following setup is a call to `setItemRelativeURL()` (defined in `listdispl.js`) that specifiess what the relative URL should start with to generate a link to information about items (here event items).
* Finally, `defineRowFunction()` (defined in `listdispl.js`) is called with a function that `listdispl.js` will use to generate a tabular row for each item (here event item) that it displays. Note the use of `displayList()` (provided by `listdispl.js` which can turn a list of IDs (first parameter) into a list of HTML "A" links.

## Key identified spots in the HTML body
`listdispl.js` and `browse.js` expect certain spots in the body of the HTML to be identified with IDs.  These are the places where the scripts will insert dynamic material that the user will see:

The HTML code that will hold the list of selected elements has IDs in it that are used by `listdispl.js`:
* id `rslts`: marks the spot where `listdispl.js` is to insert the list of items it is asked to display
* ids `topbuttons" and `bottombuttons`: marks the places where the pagination buttons that `listdispl.js` generates are to be inserted.
* ids `topPositionLabel` and `bottomPositionLabel`: marks the places where the information about which block of items are being displayed are to be placed.
* id `headingText`: marks the spot where `ksearch.js` is to put the heading for the list of results.

Much of the HTML for the "accordian-style" facet display mechanism on the left side of the display is hard-coded into the HTML pages. At each level in the hierarchical display, the sequence is numbered (zero based).  Thus, the first top level item ("Event and Person") is numbered 0, the second ("Troupe and Venue") is numbered 1, etc. Within these top level display items and the facet names themselves.  Also numbered.  Thus, "Event Type", which is the first facet in the "Event and Person" category is numbered 0.0. "Event Date" is numbered 0.1, etc. These numbers also provide the link to the actual data about the facets in the facet JSON/JS material (for events, in the file `facets-event.js`).

IDs, including these sequence numbers, are assigned to various HTML components that implement the facet display structure to allow the Javascript in `browse.js` to interact with them.

At the top level two HTML elements are given IDs:
* First, an element contained within the top level label is given an ID "i" followed by the top level number (e.g., witin "Event and Person" the ID is "i0". This area contains the contained facet list, and the Javascript in `browse.js` will change its style `display` setting to display or hide it.
* In addition, a span that initially displays the text "Click to open" is given ID "oc" followed by the top level number (e.g. within "Event and Person" the ID is "oc0"). The Javascript in `browse.js` changes this text to say "Click to close" if the facet list is currently being displayed.

At the second level of the facet display accordian are the elements that display the names of the facets associated with each top-level facet grouping.  IDs are assigned there too to allow enable interaction by `browse.js`:

* First, within the Facet name HTML is a span with ID "h" followed by the facet number (e.g. "h0.0", "h0.1", etc).  This span is filled with HTML that provides help text.  This text is provided by `browse.js` Javascript, and comes from the facet JSON data.
* The HTML element that allows the user to open and close the facet list if given ID "oc" followed by the facet number (e.g. "oc0.0", "oc0.1")  This allows the Javascript in `browser.js` to change the text depending whether the contents of this facet is being displayed or not.
* Finally, the HTML element that is used to contain the display of categories for the facet is given ID "i" followed by the facet number (e.g. "i0.0", "i0.1", etc).  This allows the Javascript in `browser.js` to generate the list of categories for the facet (drawn, originally, from the categories for the facet given in the facet JSON data (in `facets-event.js` for events,etc).  It also allows the Javascript to hide or display ths list depending upon whether the user has asked to see it or not.

The contents of the third level of the facet display accordian (the actual categories for each facet) will vary with the user's interaction: starting with the initial list of categories found in `facets-event.js` for events, etc, but changing as the user chooses facets that filter the list for all facets.  Thus, the Javascript code in `browser.js` is responsible for generating the HTML that displays the particular list of categories that apply at any point in time.
