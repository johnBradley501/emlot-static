# A brief introduction to ksearch.js
The `jsearch.js` Javascript files holds the code that manages the keyword searching function.  The actual search itself is carried out using the [fuse engine](https://www.fusejs.io/).

The functionality is very simple and requirees only two functions:
* `setup()` stores the major pieces of data that will actually be required for the search.  Among them is the setting up of the fuse engine.  In this regard, note in particular the parameter `itemNo` which specifies the position in each item in the set of search data one will find the text to be searched.  With this information Fuse can be set up using its `getFn` parameter which tells it where to get its search data from.
* `doquerying()` is invoked when the user pushes the button in beside the text searching box to ask for the search to be carried out.  This function gets the query text and invokes fuse with it.  Fuse will return a list of items containing the items it selected.  Each selected item is collected into another list in a form suitable for the code in `listdispl.js` to handle, and its function `showData()` is called to display this list of results in the right-hand area.
