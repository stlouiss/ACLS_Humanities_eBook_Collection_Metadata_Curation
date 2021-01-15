
# SCOTT ST. LOUIS, Michigan Publishing, Fall 2020
# Preliminary Metadata Curation: ACLS Humanities E-Book Collection on Fulcrum

import csv
import pandas as pd


def read_csv(filename):
    """
    This function has been taken directly from the slides of
    Lecture 17 from Professor Anthony Whyte's SI 506 class (Python I)
    at the University of Michigan School of Information, Fall 2019 semester.

    Retrieves data from a CSV file.

    Parameters
    ----------
    filename: str
        The name of the CSV file.

    Returns
    ----------
    list_of_row_lists: list
        Data from each row in the CSV file.

    """

    list_of_row_lists = []

    with open(filename, 'r', encoding='utf-8') as file_obj:
        reader = csv.reader(file_obj, delimiter=',')
        print("\n\n\n\n\n\n\n")
        print('----------------------')
        print("RETURNING METADATA RECORDS WITH NO ENCODING ERRORS")
        print('----------------------')
        print("\n\n\n\n")
        for row in reader:
            try:
                print(row)
                if True:
                    list_of_row_lists.append(row)
            except UnicodeEncodeError:
                pass

        return list_of_row_lists

def read_csv_with_pandas(filename):

    """
    Function written by Joe Muller, Digital Publishing Coordinator,
    during troubleshooting with Scott St. Louis. November 13, 2020.

    Opens the CSV file into a DataFrame object,
    drops all columns except the ones specified in output_headers,
    and converts the DataFrame to a list of row lists.

    Parameters
    ----------
    filename: str
        The name of the CSV file.

    Returns
    ----------
    list_of_row_lists: list of lists
        Records from metadata CSV file.

    """

    df = pd.read_csv(filename,dtype=str)
    list_of_row_lists = []

    output_headers = [
        "uri",
        "fm:title",
        "marc:245A",
        "marc:245B",
        "marc:250A",
        "ocr:copyrightPage"
    ]

    df = df.reindex(columns = output_headers)

    for i in df.index.values:

        initial_row_as_list = df.iloc[i].to_list()

        row_as_list = []
        for cell in initial_row_as_list:
            if pd.isnull(cell):
                cell = str(cell)
            row_as_list.append(cell)

        list_of_row_lists.append(row_as_list)

    return list_of_row_lists
    

def generate_uri_list(list_of_row_lists):
    """
    Generates a list of URIs from the metadata records
    for which no encoding errors were detected.

    Parameters
    ----------
    filename: str
        The name of the CSV file.

    Returns
    ----------
    uri_list: list
        A list of URIs for each title.
    """

    uri_list = []

    for row in list_of_row_lists:
        uri = row[0]
        uri_list.append(uri)

    return uri_list


def curating_metadata(list_of_row_lists):
    """
    Cleans metadata records from CSV that did not return
    UTF-8 encoding errors.

    Parameters
    ----------
    list_of_row_lists: list
        A list of the metadata records returned
        from the original CSV without encoding errors.


    Returns
    ----------
    curated_metadata_records: list of lists
        A list of curated metadata data records
        ready to write to a new CSV file.
    """

    curated_metadata_records = []

    for row in list_of_row_lists:
        full_title = row[1]
        full_title = full_title.strip()

        if full_title.startswith("A ") == True:
            title_prefix = "A"
        elif full_title.startswith("An ") == True:
            title_prefix = "An"
        elif full_title.startswith("The ") == True:
            title_prefix = "The"
        else:
            title_prefix = ""


        if ":" in full_title:
            split_full_title_list = full_title.split(":")
            if len(split_full_title_list) == 2:
                main_title = split_full_title_list[0]
                subtitle = split_full_title_list[1].strip()

            else:
                main_title = split_full_title_list[0]
                subtitle = ":".join(split_full_title_list[1:])


        else:
            main_title = full_title
            subtitle = ""


        uri = row[0]
        marc_main_title = row[2]
        marc_subtitle = row[3]
        edition = row[4]
        copyright_ocr = row[5]

        metadata_record = [uri, full_title, main_title, subtitle, marc_main_title, marc_subtitle, title_prefix, edition, copyright_ocr]

        curated_metadata_records.append(metadata_record)

    return curated_metadata_records


def sifting_metadata_for_volume_info(list_of_row_lists):
    """
    Sifts full title values in metadata records for which
    no encoding errors were detected to look for keywords
    relevant to potential volume information.


    Parameters
    ----------
    list_of_row_lists: list
        A list of the metadata records returned
        from the original CSV without encoding errors.

    Returns
    ----------
    check_full_titles_for_volume_info: list
        A list with values indicating whether the full title fields
        need to be checked for volume information manually.
    """

    full_title_list = []
    check_full_titles_for_volume_info = []

    for row in list_of_row_lists:
        full_title = row[1]
        clean_full_title = str(full_title).lower()
        cleaner_full_title = clean_full_title.replace("\n", "")
        cleanest_full_title = cleaner_full_title.replace(" ", "")
        full_title_list.append(cleanest_full_title)

    for title in full_title_list:
        if "volume" in title:
            check_for_volume_info = "YES"
            check_full_titles_for_volume_info.append(check_for_volume_info)
        elif "vol." in title:
            check_for_volume_info = "YES"
            check_full_titles_for_volume_info.append(check_for_volume_info)
        else:
            check_for_volume_info = "N"
            check_full_titles_for_volume_info.append(check_for_volume_info)


    return check_full_titles_for_volume_info


def sifting_metadata_for_edition_info(list_of_row_lists):
    """
    Sifts copyright OCR text in metadata records for which
    no encoding errors were detected to look for keywords
    relevant to potential edition information.

    Parameters
    ----------
    list_of_row_lists: list
        A list of the metadata records returned
        from the original CSV without encoding errors.

    Returns
    ----------
    check_copyright_ocr_for_edition_info: list
        A list with values indicating whether the full copyright OCR text
        needs to be checked for edition information manually, and in what
        order of priority if so.
    """

    copyright_ocr_list = []
    check_copyright_ocr_for_edition_info = []

    for row in list_of_row_lists:
        copyright_ocr = row[5]
        clean_copyright_ocr = str(copyright_ocr).lower()
        cleaner_copyright_ocr = clean_copyright_ocr.replace("\n", "")
        cleanest_copyright_ocr = cleaner_copyright_ocr.replace(" ", "")
        copyright_ocr_list.append(cleanest_copyright_ocr)

    for copyright_ocr_item in copyright_ocr_list:
        if "edition" in copyright_ocr_item:
            check_for_edition_info = "YES -- CHECK FIRST"
            check_copyright_ocr_for_edition_info.append(check_for_edition_info)
        elif " ed." in copyright_ocr_item:
            check_for_edition_info = "YES -- CHECK SECOND"
            check_copyright_ocr_for_edition_info.append(check_for_edition_info)
        else:
            check_for_edition_info = "N"
            check_copyright_ocr_for_edition_info.append(check_for_edition_info)

    return check_copyright_ocr_for_edition_info


def sifting_metadata_for_title_differences(list_of_row_lists):
    """
    Sifts fm and marc title values in metadata records for which
    no encoding errors were detected to look for potential
    indicators of discrepancies.

    The following Stack Overflow page was helpful in producing this function:
    "Merge Two Lists to Make List of Lists,"
    https://stackoverflow.com/questions/23327242/merge-two-lists-to-make-list-of-lists (accessed October 28, 2020)

    Parameters
    ----------
    list_of_row_lists: list
        A list of the metadata records returned
        from the original CSV without encoding errors.

    Returns
    ----------
    check_fm_and_marc_titles_for_differences: list
        A list with values indicating whether the fm and marc title values
        need to be checked for discrepancies manually.
    """


    fm_full_title_list = []
    marc_full_title_list = []
    check_fm_and_marc_titles_for_differences = []

    for row in list_of_row_lists:
        fm_full_title = str(row[1]).lower()
        clean_fm_full_title = fm_full_title.replace("/n", "")
        cleaner_fm_full_title = clean_fm_full_title.replace(" ", "")
        cleanest_fm_full_title = cleaner_fm_full_title.replace(":", "")
        ready_fm_full_title = cleanest_fm_full_title.replace(",", "")
        fm_full_title_list.append(ready_fm_full_title)

        marc_main_title = row[2]
        marc_subtitle = row[3]

        clean_marc_main_title = str(marc_main_title).lower()
        cleaner_marc_main_title = clean_marc_main_title.replace("\n", "")
        cleanest_marc_main_title = cleaner_marc_main_title.replace(" ", "")
        almost_ready_marc_main_title = cleanest_marc_main_title.replace(",", "")
        ready_marc_main_title = almost_ready_marc_main_title.replace(":", "")

        if marc_subtitle.endswith("/") == True:
            marc_subtitle = marc_subtitle[:-1]
            clean_marc_subtitle = str(marc_subtitle).lower()
            cleaner_marc_subtitle = clean_marc_subtitle.replace("\n", "")
            cleanest_marc_subtitle = cleaner_marc_subtitle.replace(" ", "")
            almost_ready_marc_subtitle = cleanest_marc_subtitle.replace(",", "")
            ready_marc_subtitle = almost_ready_marc_subtitle.replace(":", "")

        elif marc_subtitle.endswith("/") == False:
            clean_marc_subtitle = str(marc_subtitle).lower()
            cleaner_marc_subtitle = clean_marc_subtitle.replace("/n", "")
            cleanest_marc_subtitle = cleaner_marc_subtitle.replace(" ", "")
            almost_ready_marc_subtitle = cleanest_marc_subtitle.replace(",", "")
            ready_marc_subtitle = almost_ready_marc_subtitle.replace(":", "")

        marc_full_title = ready_marc_main_title + ready_marc_subtitle

        marc_full_title_list.append(marc_full_title)

        a = fm_full_title_list
        b = marc_full_title_list

        combined_title_values = [list(x) for x in zip(a, b)]

    for title_string_pairs in combined_title_values:       # Implementing conditions below to anticipate the "nan" that Python is adding to certain strings.

        if len(title_string_pairs[0]) == len(title_string_pairs[1]):

            if title_string_pairs[0] == title_string_pairs[1]:
                check_fm_and_marc_titles = "N"
                check_fm_and_marc_titles_for_differences.append(check_fm_and_marc_titles)
                continue
            elif title_string_pairs[0] != title_string_pairs[1]:
                check_fm_and_marc_titles = "YES"
                check_fm_and_marc_titles_for_differences.append(check_fm_and_marc_titles)
                continue

        elif len(title_string_pairs[0]) != len(title_string_pairs[1]):

            if title_string_pairs[1].endswith("nan"):

                if title_string_pairs[0] == title_string_pairs[1][:-3]:
                    check_fm_and_marc_titles = "N"
                    check_fm_and_marc_titles_for_differences.append(check_fm_and_marc_titles)
                    continue
                elif title_string_pairs[0] != title_string_pairs[1][:-3]:
                    check_fm_and_marc_titles = "YES"
                    check_fm_and_marc_titles_for_differences.append(check_fm_and_marc_titles)
                    continue

            else:
                check_fm_and_marc_titles = "YES"
                check_fm_and_marc_titles_for_differences.append(check_fm_and_marc_titles)
                continue

    return check_fm_and_marc_titles_for_differences


def combine_values(uri_list, check_full_titles_for_volume_info, check_copyright_ocr_for_edition_info, check_fm_and_marc_titles_for_differences):
    """
    Creates list of check values corresponding to title URIs.

    The following Stack Overflow page was helpful in producing this function:
    "Merge Two Lists to Make List of Lists,"
    https://stackoverflow.com/questions/23327242/merge-two-lists-to-make-list-of-lists (accessed October 28, 2020)

    Parameters
    ----------
    uri_list: list
        A list of URIs for each title
    check_full_titles_for_volume_info: list
        A list of check values for volume information corresponding to full title strings.
    check_copyright_ocr_for_edition_info: list
        A list of check values for edition information corresponding to copyright OCR strings.

    Returns
    ----------
    combined_values: list
        A list of URIs and volume/edition check values
        corresponding to each title.

    """

    a = uri_list
    b = check_full_titles_for_volume_info
    c = check_copyright_ocr_for_edition_info
    d = check_fm_and_marc_titles_for_differences

    combined_values = [list(x) for x in zip(a, b, c, d)]

    return combined_values


def write_curated_metadata(curated_metadata_records, filename_1):
    """
    Cleans metadata records from CSV that did not return
    UTF-8 encoding errors.

    Source for help constructing this function:
    Jon Fincher, "Reading and Writing CSV Files in Python,"
    Real Python, accessed October 13, 2020,
    https://realpython.com/python-csv/

    Parameters
    ----------
    curated_metadata_records: list of lists
        The list of curated metadata records to be written
        to the desired CSV file.

    filename_1: string
        The desired CSV file to which to write the
        curated metadata records.

    Returns
    ----------
    filename_1: CSV
        A spreadsheet file with the curated metadata records.

    """

    with open(filename_1, 'w', encoding = 'utf-8') as csv_file:

        fieldnames = ["uri", "full_title", "main_title", "subtitle",
        "marc_main_title", "marc_subtitle", "title_prefix", "edition", "copyright_ocr",]

        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)

        writer.writeheader()

        for record in curated_metadata_records:

            writer.writerow({"uri": record[0], "full_title": record[1], "main_title": record[2], "subtitle": record[3],
            "marc_main_title": record[4], "marc_subtitle": record[5], "title_prefix": record[6],
            "edition": record[7], "copyright_ocr": record[8]})

        return filename_1


def write_sifting_responses(combined_values, filename_2):
    """
    Writes the check values corresponding to URI onto a spreadsheet.

    Source for help constructing this function:
    Jon Fincher, "Reading and Writing CSV Files in Python,"
    Real Python, accessed October 13, 2020,
    https://realpython.com/python-csv/

    Parameters
    ----------
    combined_values: list
        A list of URIs and volume/edition check values corresponding to each title.
    filename_2: string
        The desired CSV file to which to write the check values

    Returns
    ----------
    filename_2: CSV
        A spreadsheet file with the check values organized by URI.
    """

    with open(filename_2, 'w', encoding = 'utf-8') as csv_file:

        fieldnames = ["uri", "check_full_titles_for_volume_info?", "check_copyright_ocr_for_edition_info?", "check_fm_and_marc_titles_for_differences?"]

        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)

        writer.writeheader()

        for combined_value in combined_values:
            writer.writerow({"uri": combined_value[0],
            "check_full_titles_for_volume_info?": combined_value[1],
            "check_copyright_ocr_for_edition_info?": combined_value[2],
            "check_fm_and_marc_titles_for_differences?": combined_value[3]})

    return filename_2


def merge_csv_files(filename_1, filename_2):
    """
    The following Stack Overflow page was helpful in writing this function:
    "Merging two CSV files using Python,"
    https://stackoverflow.com/questions/16265831/merging-two-csv-files-using-python
    (accessed October 28, 2020)

    Merges CSV files of curated metadata records and
    volume/edition check values on shared URI strings.

    Parameters
    ----------
    filename_1: string

    filename_2: string

    Returns
    ----------
    final_output_metadata: CSV
        A CSV file merging the two input CSV files
        on the URI field.
    """

    curated_metadata_records = pd.read_csv(filename_1)
    sifting_resposes = pd.read_csv(filename_2)
    merged = curated_metadata_records.merge(sifting_resposes, on="uri")
    final_output_metadata = merged.to_csv("python_FINAL_output_metadata.csv", index=False)

    return final_output_metadata




if __name__ == "__main__":


    list_of_row_lists = read_csv_with_pandas("2020-09-23_11-55-25_breakout_title.csv")


    print("\n\n\n\n\n")
    print('----------------------')
    print(f"RETURNED {len(list_of_row_lists)} METADATA RECORDS WITH NO ENCODING ERRORS" )
    print('----------------------')
    print("\n\n\n\n")


    curated_metadata_records = curating_metadata(list_of_row_lists)


    print("----------------------")
    print(f"CURATED METDATA RECORDS FOR {len(curated_metadata_records)} ROW ENTRIES WITHOUT ENCODING ERRORS")
    print("----------------------")
    print("\n\n\n\n")

    uri_list = generate_uri_list(list_of_row_lists)
    check_full_titles_for_volume_info = sifting_metadata_for_volume_info(list_of_row_lists)
    check_copyright_ocr_for_edition_info = sifting_metadata_for_edition_info(list_of_row_lists)
    check_fm_and_marc_titles_for_differences = sifting_metadata_for_title_differences(list_of_row_lists)

    combined_values = combine_values(uri_list, check_full_titles_for_volume_info, check_copyright_ocr_for_edition_info, check_fm_and_marc_titles_for_differences)

    processing_metadata_csv = write_curated_metadata(curated_metadata_records, "python_curated_metadata.csv")

    sifting_responses = write_sifting_responses(combined_values, "python_sifting_responses.csv")

    print("----------------------")
    print(f"RETURNED CSV FILE WITH {len(curated_metadata_records)} CURATED METADATA RECORDS")
    print("----------------------")
    print("\n\n\n\n")


    final_curated_metadata = merge_csv_files("python_curated_metadata.csv", "python_sifting_responses.csv")

