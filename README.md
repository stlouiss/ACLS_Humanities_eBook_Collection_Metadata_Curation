# Preliminary Metadata Curation: ACLS Humanities eBook Collection on Fulcrum

READ_ME editing is in process. Please bear with us as we continue to revise this document!

## Python Script for Initial Metadata Curation

* Input spreadsheet: “2020-09-23_11-55-25_breakout_title.csv”
  * Be sure to place the input spreadsheet in the same directory on your machine as the Python code. Doing so is necessary in order for the script to run correctly.

* Final output spreadsheet: “python_FINAL_output_metadata.csv”
  * (Ignore other output spreadsheets; these are processing materials)

### What does the Python script do?

* Main goal of the Python script: 
 * The main function of this Python script is to return a CSV file that contains a list of curated HEB titles and corresponding URIs. 
  * The final CSV documents which titles require their volume/edition to be manually reviewed and in what priority order.
    * See docstrings and code in srs_metadata_cleaning.py
    
### Functions

##### read_csv(filename)
Reads the input CSV file into the Python script.
  
##### read_csv_with_pandas(filename)
Opens the input CSV file into a DataFrame objec, drops all columns except those stpecified as output headers, and converts the DataFrame into a list of row lists that will be used in later functions detailed below.
  
##### generate_uri_list(list_of_row_lists)
Generates a list of URIs from the metadata records of the input CSV for which no encoding errors were detected. It isolates the uri items in list_of_row_lists by slicing at position [0] in list_of_row_lists, yielding the object uri. Then, object uri is appended to the object uri_list. The function returns uri_list.
  
##### curating_metadata(list_of_row_lists)
Performs basic metadata curation on the list of row lists, including the following actions:
* Identifying a full title
* Generating title prefixes
* Splitting FM full titles into main titles and subtitles
* Incorporating URIs, MARC main titles, MARC subtitles, edition information, and copyright OCR information into each metadata record
* Returns curated metadata records (a list of lists) that will be used later in the script

This function starts by taking the items at position [1] in list_of_row_lists (object “fm:title”) and breaks them down into their title components. First, it identifies title prefixes with an if/else strip function that identifies “A”, “An”, and “The” as title prefixes and strips the prefixes of their extra whitespace. Then, it identifies main titles and subtitiles in another if/else setup that splits items that contain “:” in their string. The function then designates that the items at positions [0] and [1] in the split string equate to the main title and subtitle respectively. Finally, the list object metadata_records is populated with row objects from list_of_row_lists through position slicing. Finally, the metadata_records list is appended to the curated_metadata_records list. The function returns curated_metadata_records.

##### sifting_metadata_for_volume_info(list_of_row_lists)
Examines full title values in metadata records to look for keywords that might signify the presence of volume information. Designated keywords: “volume” and “vol.”

Returns list with values indicating which titles need to be checked for volume information manually, and which do not.

The function creates 2 new list objects, full_title_list and check_full_titles_for_volume_info. First, the function cleans the items in row[1] of list_of_row_lists and cleans them through an if statement, creating objects for clean_full_title, cleaner_full_title, and cleanest_full_title. The cleanest_full_title object is appended to the full_title_list object. Next, an if/else/elif statement assigns “YES” or “N” indicators to the objects in full_title_list. The if/else/elif statement checks to see if the objects in the list contain the keywords “volume” or “vol.”, and creates a new object check_for_volume_info to which the value “YES” or “N” is assigned depending on if they contain the keyword values or not. The check_for_volume_info objects are appended to the check_full_titles_for_volume_info list. 

The function returns the check_full_titles_for_volume_info list. The user will be able to see if the titles need to be manually reviewed through the Yes or N labels the function has assigned them.

##### sifting_metadata_for_edition_info(list_of_row_lists)
Examines copyright OCR text in metadata records to look for keywords that might signify the presence of edition information. Designated keywords: “edition” (CHECK FIRST) and “ ed.” (note spacing) (CHECK SECOND due to greater potential for noise pickup on the second keyword than on the first).

Returns list with values indicating which copyright OCR texts need to be checked for edition information manually and in what order of priority if so (first/second), as well as which do not need manual review.

The function creates two new list objects, copyright_ocr_list and check_copyright_ocr_for_edition_info. First, the function cleans the items in row[5] of list_of_row_lists and cleans them through an if statement, creating objects for clean_copyright_ocr, cleaner_copyright_ocr, and cleanest_copyright_ocr. The cleanest_copyright_ocr object is appended to the copyright_ocr_list object. Next, an if/ else /elif statement assigns “YES -- CHECK FIRST”, “YES -- CHECK SECOND” or “N” indicators to the objects in copyright_ocr_list. 

The if/else/elif statement checks to see if the objects in the list contain the keywords “edition” or “ed.”, and creates a new object check_for_edition_info to which the value “YES -- CHECK FIRST”, “YES -- CHECK SECOND”, or “N” is assigned depending on if they contain the keyword values or not. The check_for_edition_info objects are appended to the check_full_titles_for_volume_info list. 

The function returns the check_copyright_ocr_for_edition_info list. The user will be able to see if the titles need to be manually reviewed through the Yes or N labels the function has assigned them, as well as the order in which they should be addressed through the manual review process.


##### sifting_metadata_for_title_differences(list_of_row_lists)
Compares fm and MARC title values in metadata records to determine where differences might require manual review. Flags potential discrepancies via string length comparison after cleaning the titles to make string length a viable method of comparison for this purpose.

Returns a list with values indicating which fm and MARC title values need to be checked for discrepancies manually, and which do not.

##### combine_values(uri_list, check_full_titles_for_volume_info, check_copyright_OCR_for_edition_info, check_fm_and_marc_titles_for_differences)
Creates a list of check values corresponding to object URIs. These values reflect the necessity of manual review for volume information, edition information, and title differences, as established by previous functions.

##### write_curated_metadata(curated_metadata_records, filename_1)
Creates a CSV file of curated metadata records developed by a previous function, using URIs as the unique identifier.

##### write_sifting_responses(combined_values, filename_2)
Creates a CSV file for the manual-review check values on title, volume, and edition information, using URIs as the unique identifier.

##### merge_csv_files(filename_1, filename_2)
Merges the CSV files generated by the previous two functions by way of the URI value in each record.

##### IN SUMMARY: 
The script selects relevant fields from an input CSV, performs curation based on the project team’s manual review needs, and then moves the cleaned metadata records to an output CSV, where they are ready for manual review regarding volume information, edition information, and differences in existing title records.

fm:title in input spreadsheet becomes full_title in output spreadsheet, which also includes main_title and subtitle fields derived from full_title

Script analyzes metadata to flag for three different manual tasks:
* Check_full_titles_for_volume_info?
  * Designated keywords flagged by script: “volume” and “vol.”
  
* Check_copyright_ocr_for_edition_info?
  * Designated keywords flagged by script: “edition” and “ ed.” (note spacing)
  
* Check_fm_and_marc_titles_for_differences?
  * Performs string length comparison to flag potential discrepancies in need of manual review.
  
##### For project team members: 

The fields added to this output spreadsheet MANUALLY reflect our need for note-taking as we complete the manual review tasks listed above.

You will notice that the python_FINAL_output_metadata CSV spreadsheet in our Google Drive folder, on which Kelsey and Scott are completing manual review, contains additional fields compared to the output sample available on GitHub at the link above. Those fields have been added manually to assist with completing the manual review process.
The manual review process consists of tasks that require human inspection/judgment.

##### Thank you!

--- Scott St. Louis (primary developer and documentation co-author)
--- Rachel Gosch (documentation co-author and editor)
--- Joe Muller (project supervisor)

