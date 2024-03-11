This repo contains the files that have been created to enable a static publication of EMLoT

The work involved coding in two areas:
* First, data had to be extracted from the EMLoT MySQL database and turned into JSON (packaged within JavaScript files). These Python scripts can be found in the "src" folder.
* Then, Javascript coding had to be incorporated into HTML pages in the EMLoT presentation that could exploit this formulation and provide a mechanism that could run both the keyword search and facetted browse facilities. These can be found in the "web" folder: most specifically the HTML in web/db/browser and web/db/keyword-search, and the Javascript code in web/db/js.

John Bradley (john.bradley@kcl.ac.uk)
