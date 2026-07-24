# ArchivesSpace tools
Note that these tools *are* specific to the needs of a specific repository so anyone wanting to use them should probably run against a single file and check the output for your needs before proceeding.

Future work may include consolidating common functionality into a module rather than having in separate scripts multiple times. Keep an eye out for that but no promises. 

## Requirements
You will need to install the following modules for this to work properly. Order of installation is not important. These modules may have dependencies as well but if you use pip it should be fine.
* csv
* daterangeparser
* datetime
* errno
* lxml
* pysimplegui v4.xx
* re
* shutil

## Explanations for each of the scripts are as follows:

### ArchivesSpace_normalization.py
This is meant to normalize specific fields prior to importing a finding aid into ArchivesSpace. It does not have any embedded stylesheet. 

It will remove trailing commas, periods, and spaces from:
* ead:unittitle
* ead:unitdate

It will also de-nest specific fields which may have been nested previously.
* ead:relatedmaterial
* ead:controlaccess

Note that it will also remove the original container ead:controlaccess and relatedmaterial. Also, the controlaccess and relatedmaterial sections are output as immediate siblings the arrangement so it may not place that section exactly where it came from. This **WILL NOT** affect how data is rendered.

**Note:** ArchivesSpace normalization and system import was completed some years ago in earlier editions of ArchivesSpace and may not be compatible with current generation processes.

### normalizeDates_tocsv.py
For before ArchivesSpace ead import. This is meant to help with standardizing how dates are phrased in a finding aid. Over time it is common for different naming conventions to be used and different data entry standards to be applied. This tool works by taking the normal attribute of unitdate as the marker for a beginning and ending date. It works as a crawler and will output one spreadsheet per ead file it encounters.

It will output a spreadsheet with the following:
* filename: the name of the file that was processed
* xpath: the address in the file the data was pulled from. Used to push changed data back into the file
* date_original: The text as it exists now
* date_normal: the date normal attribute so you can see where the date is derived from
* date_computer_suggestion: the date derived from normal attribute. This can be configured but defaults to the spelled out month, numeric day including leading zeros and full year. Beginning and end date are separated by " to ". If there are 0000 in the normal attribute it will output Undated.
* date_desired: this will be where you choose which date text to keep. a future script will pair this field back to the actual ead file

Note: This is set to only handle year or year-month-day normal attributes. If the first day of a year is indicated as the start and last day as the end if will output year only. *This is only as good as your data, if there is an error in the normal attribute it will be transcribed.* 

Note: If you start this on a set of files, DO NOT change anything in the file until you are done. The xpath is sensitive to changes in structure and you might disrupt that detail.

### normalizeExtent_fromcsv.py
For before ArchivesSpace import. Takes the spreadsheet generated and people processed from normalizeExtent_tocsv.py and pairs the extent content back into the ead file. This is as a physdesc/extent. If someone was clever and tried to create a new tag within the extent you will get an &amp;lt; and &amp;gt; text you will need to address

### normalizeExtent_fromcsv_special.py
Same as above but with additional modifications for a coworker who didn't want to bother to actually change the spreadsheet like they needed to.

### normalizeExtent_to_csv.py
For before ArchivesSpace ead import. Crawls a directory and reads each ead file and spits out a spreadsheet per file with the address and text of the physdesc/extent field. Preprocesses the file by making sure extents are nested in a physdesc as much as possible. Be wary that if your data is structured weird you might lose it so check the output ead file for everything before throwing out the original.

It will output a spreadsheet with the following without headers:
* filename (for pairing to the correct file)
* xpath, for where to insert the modified data. If you decide to do this process **DO NOT** do anything else with an ead file until you are done as the xpath is very sensitive to structure changes.
* extent text. This is the field to modify

Note that the point here is to know what you have and standardize it before importing into ArchivesSpace and generating a bunch of unnecessary extent controlled value list thing. For example `2 folders` could be standardized to `2 folder` to avoid a duplicative item for the same underlying concept. Any also to catch where people decided to spell out a number so some archaic reason. ArchivesSpace will **only handle numbers** for a extent value.

### normalizeExtent_tocsv_oneCSV.py
For before ArchivesSpace ead import. Same as above but spits out to a single spreadsheet so everything can be done by one person. The fromcsv script pairs based on filename so it should work fine. I *highly* recommend using this over the individual spreadsheets for standardized approach reasons. For either, you can delete a line from the spreadsheet if it is fine. Just don't change the ead file until you are done.

# Executable tools
Executable tools *must* by compiled into a graphical executable, they do not run as well as a script. Graphical interface constructed using pysimplegui. See their documentation for how to compile the executable.
## executables/taro_processor.py
Requires compilation into an executable using pysimplegui version 4.xx. A complete re-write under the hood (since remove from github) of a prior graphical interface to normalize ArchivesSpace export for upload onto TARO (https://txarchives.org).
Rewrite was required to accommodate Lyrasis hosting which included a TARO-EAD export function. The TARO-EAD export plugin does many tasks but not everything to match TSLAC standards, this tool makes up the difference.

It will also create a html page to visually quickly QC the output for problems. An extra checkbox was added to activate a different html export that resolves an issue with table formatting which isn't technically "approved." Original file is kept, normalized file and html output saved to same folder as normalized file.

Error handling includes pop-ups that try to explain what step the problem arose in and where the error might be. Depending on the error, it may be possible to continue processing but you will need to make notes on the error before proceeding.
Individual actions taken on a file are very detailed and unrealistic to list out here.

## executables/inventory_tool.py
Swiss army knife style tool to handle many inventory functions either not done easily in ArchivesSpace or not handled by ArchivesSpace.
Only requires Location Holdings Report from reporting section of ArchivesSpace.

**NOTE:** if the formatting of this report changes over time the code will also need to change to account for that.

Has the following core functions:
* Circulation
  * Leveraging barcodes for a destination location and container to change locations in ArchivesSpace and insert a internal note on current location with an audit trail for all movements of the container over time.
* Inventory management
  * Can generate a print-out of either a whole room or range of Range/Section/Shelf coordinates
  * Generates a pop-up list, can also generate a PDF version and CSV version of the list
  * *NOTE* that nomenclature is specific to TSLAC and may need customization for other to use
  * Generate a gross volume of free stack space within a room
  * Using a value of how many linear inches are needed, generate a list of where gaps in space exist that can fit that volume of materials
* Container inventorying by container identifier or accession/resource identifier
  * Container identifier uses a text string startswith method and generates a stacks coordinates output
  * Accession/Resource identifier uses an exact match method and generates a stacks coordinates output
* Shelf-level inventory management
  * Adding barcodes to containers
  * Adding barcodes to locations
  * Updating location profiles to get a better read of available stacks space

# ArchiveSnake tools
These are scripts that rely on archivesnake to do API tasks. You will need to have that installed and configured to log into your system. 
## asnake_fixExtent.py
Uses a dictionary method to normalize errant extent types. The correct extent type is the dictionary key, the errant type is a text item in a list associated with the key. Crawls all repositories based on repo number.       This needs to be localized.
## asnake_fixSubjects.py
Meant to correct a problem where some LCSH subject terms were imported as `Library of Congress Subject Headings` rather than `lcsh`. Crawls entire system.
## asnake_microfilm.py
Meant to crawl repo #2  for instances where there are multiple top containers for an item, one physical item and one microfilm. Finds the microfilm container or creates a new top-container for the microfilm if that doesn't exist, makes the item pairing, removes the data for the microfilm from the original container.
Note that it has to wait for 30 seconds for a newly created container to register in the system so it can take a while. Has a feature to pick up where it left off built in so multiple full passes aren't necessary if you've added stuff and need to rerun.
## asnake_retype_top_container.py
A testing tool to change a top container type from one to another. Configured for changing "Reel" to microfilm but can be applicable to anything.
## container_test.py
The output of a container creation test, provides information on how container data is structured.
## generate_locations_csv.py
Crawls system for all generated locations and creates spreadsheet with the data points. Meant for future pairing of containers created as part of Aspace import to their correct stacks coordinates.
## topContainer_create.py
A testing tool to make sure it is possible to create top containers via the API
## topContainer_bulkGenerate.py
An API tool to take       a csv with container names and bulk generate those containers. Spreadsheet also hase informattttion parameters to link into a specific collection/accession, assign a container profile, and assign a location via the location UUID. Has a pause of 30 seconds after bulk create before trying any pairing to try to get the containers registered in the system.

***Note***: There is a known irresolvable issue where the containers do not always take in the system, or do take but there is a delay in getting recognized by the index. You may need to run, curate to what didn't get created, rerun, etc. ***and then*** check for dedupe needs.
