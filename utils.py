import os, re
import xml.etree.ElementTree as ET

"""
Write XML records to a directory as files in the format specified by `file_suffix`
(the XML may be malformed, in which case corrections will need to be made by
reading the data from a TXT and then re-writing it as XML).
"""
def write_xml(records_ids_list, records_list, dir, file_prefix, file_suffix):
    i, maxI = 0, len(records_ids_list)
    while i < maxI:
        id = str(int(records_ids_list[i]))
        record = records_list[i]
        
        """
        Remove extraneous text so only data between tags (< >) remains
        """
        xml_data = re.findall(r"<.+>", record)

        """
        If xml_data isn't an empty list, define the file name, 
        padding the ID with leading zeros, and write the data
        to an XML file
        """
        if len(xml_data) > 0:
            # file_suffix = ".xml"
            if len(id) == 1:
                file_id = "00" + id
            elif len(id) == 2:
                file_id = "0" + id
            else:
                file_id = id
            filename = file_prefix + file_id + file_suffix
            filepath = dir+filename

            with open(filepath, "w") as file:
                for line in xml_data:
                    file.write(line)
                    file.write("\n")
            file.close()
            print("Wrote", filename+"!")

        i += 1

"""
Write JSON records to a directory as files in the format specified by `file_suffix`
(the JSON may be malformed, in which case corrections will need to be made by
reading the data from a TXT and then re-writing it as JSON).
"""
def write_json(records_ids_list, records_list, dir, file_prefix, file_suffix):
    i, maxI = 0, len(records_ids_list)
    while i < maxI:
        id = str(int(records_ids_list[i]))
        record = records_list[i]
        
        """
        Remove extraneous text so only data between curly braces ({ }) remains
        """
        json_data = re.findall(r"\{[\W\w]*\}", record)

        """
        If json_data isn't an empty list, define the file name, 
        padding the ID with leading zeros, and write the data
        to a JSON file
        """
        if len(json_data) > 0:
            # file_suffix = ".json"
            if len(id) == 1:
                file_id = "00" + id
            elif len(id) == 2:
                file_id = "0" + id
            else:
                file_id = id
            filename = file_prefix + file_id + file_suffix
            filepath = dir+filename

            with open(filepath, "w") as file:
                for line in json_data:
                    file.write(line)
                    file.write("\n")
            file.close()
            print("Wrote", filename+"!")

        i += 1


'''
Correct malformed Dublin Core XML by reading TXT versions of the files as strings
and re-writing the corrected versions as XML files.  To exclude an XLM prolog (declaring 
the document type and specifying UTF-8 encoding), set prolog to False.
'''
prolog = '<?xml version="1.0" encoding="UTF-8"?>'
dc_prefix_open_tag = '<metadata xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dc="http://purl.org/dc/elements/1.1/">'
dc_prefix_close_tag = '</metadata>'

def correctDCXML(txt_errored_files, error_list, prolog=prolog, dc_prefix_open_tag=dc_prefix_open_tag, dc_prefix_close_tag=dc_prefix_close_tag):
    i, maxI = 0, len(error_list)
    still_incorrect = []
    while i < maxI:
        txt_file, message = txt_errored_files[i], error_list[i]
        
        if "Namespace prefix dc" in message:
            with open(txt_file, "r") as f:
                f_string = f.read()

                # Look for different error patterns

                open_tag = re.findall("<dublin.*core.*>", f_string)
                if (len(open_tag) == 1):
                    f_string = f_string.replace(open_tag[0],dc_prefix_open_tag)
                close_tag = re.findall("</dublin.*core>", f_string)
                if (len(close_tag) == 1):
                    f_string = f_string.replace(close_tag[0], dc_prefix_close_tag)
                
                has_prefix_open_tag = re.findall(dc_prefix_open_tag, f_string)
                if not has_prefix_open_tag:
                    f_string = dc_prefix_open_tag + "\n" + f_string
                has_prefix_close_tag = re.findall(dc_prefix_close_tag, f_string)
                if not has_prefix_close_tag:
                    f_string = f_string + "\n" + dc_prefix_close_tag

                if prolog != False:
                    has_prolog = re.findall("^\<\?xml version=.+ encoding=.+", f_string)
                    if len(has_prolog) == 0:
                        f_string = prolog + "\n" + f_string

        # To validate that the new data is well-formed, try parsing it as XML
        try:
            root = ET.fromstring(f_string)
            xml_file = txt_file.replace(".txt", ".xml")
            with open(xml_file, "w") as f:
                f.write(f_string)
        except:
            still_incorrect += [txt_file]

        i += 1
        return still_incorrect