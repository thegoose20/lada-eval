import os, re, json
from pyld import jsonld
import xml.etree.ElementTree as ET
import pandas as pd

dc_namespace = 'xmlns:dc="http://purl.org/dc/elements/1.1/"'
dc_qual_namespace = 'xmlns:dcterms="http://purl.org/dc/terms/"'
rdf_namespace = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
dc_prefix_open_tag_qual = '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/">'
dc_prefix_open_tag_simple = '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dc="http://purl.org/dc/elements/1.1/">'
dc_prefix_close_tag = '</rdf:RDF>'



############################################################
################### CREATING CLEAN FILES ###################
############################################################



'''
Write XML records to a directory as files in the format specified by `file_suffix`
(the XML may be malformed, in which case corrections will need to be made by
reading the data from a TXT and then re-writing it as XML).
'''
def write_xml(records_ids_list, records_list, dir, file_prefix, file_suffix):
    i, maxI = 0, len(records_ids_list)
    while i < maxI:
        id = str(int(records_ids_list[i]))
        record = records_list[i]
        
        '''
        Remove extraneous text so only data between tags (< >) remains
        '''
        xml_data = re.findall(r"<.+>", record)

        '''
        If xml_data isn't an empty list, define the file name, 
        padding the ID with leading zeros, and write the data
        to an XML file
        '''
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


'''
Write JSON records to a directory as files in the format specified by `file_suffix`
(the JSON may be malformed, in which case corrections will need to be made by
reading the data from a TXT and then re-writing it as JSON).
'''
def write_json(records_ids_list, records_list, dir, file_prefix, file_suffix):
    i, maxI = 0, len(records_ids_list)
    while i < maxI:
        id = str(int(records_ids_list[i]))
        record = records_list[i]
        
        '''
        Remove extraneous text so only data between curly braces ({ }) remains
        '''
        json_data = re.findall(r"\{[\W\w]*\}", record)

        '''
        If json_data isn't an empty list, define the file name, 
        padding the ID with leading zeros, and write the data
        to a JSON file
        '''
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



############################################################
################### EVALUATING METADATA ####################
############################################################



def hasDCNamespaces(f, dc_namespace=dc_namespace, dc_qual_namespace=dc_qual_namespace):
    f = f.lower()
    if "dcterms" in f:
        if (dc_namespace in f) and (dc_qual_namespace in f):
            return True
        else:
            return False
    else:
        if dc_namespace in f:
            return True
        else:
            return False


def hasRDFNamespace(f, rdf_namespace=rdf_namespace):
    f = f.lower()
    if rdf_namespace in f:
        return True
    else:
        return False
    

def hasProlog(f):
    f = f.lower()
    if '<?xml version="1.0"' in f:
        return True
    else:
        return False

'''
By default check for UTF-8 encoding, but allow for other encodings with the encoding parameter.
'''
def hasPrologWithEncoding(f, encoding="UTF-8"):
    f = f.lower()
    if '<?xml version="1.0" encoding="UTF-8"?>' in f:
        return True
    else:
        return False
    

'''
Input a compiled regex pattern, indicating where to look for emptiness in specified 
files, and a list of file paths (as strings), indicating which files to check for 
empty data fields.
Output a list of only the files (as strings of a full file path) that contain at least 
one empty field, a list of lists of the empty fields of each file (one sublist per file 
for each file in the input list of file paths), and a list of the total number of empty 
fields per file (one total for each file in the input list of file paths).
'''
def findEmptyFields(empty_pattern, file_paths):
    files_with_empty, empty_fields_per_file, fields_per_file = [], [], []
    for file_path in file_paths:
        with open(file_path, "r") as f:
            f_string = f.read().lower()
            # Look for empty fields in the file
            is_empty = re.finditer(empty_pattern, f_string)
            # Save the empty fields, including the opening and closing tags and any text in between
            empty_fields = [field[0] for field in is_empty]
            fields_per_file += [empty_fields]
            # # Save the file path to the XML version of the file
            if len(empty_fields) > 0:
                file_path.replace(".txt", ".xml")
                files_with_empty += [file_path]
            # Save the number of empty fields in the file
            empty_fields_per_file += [len(empty_fields)]
            f.close()
    print(sum(empty_fields_per_file), "empty field(s) across", len(files_with_empty), "files found.")
    return files_with_empty, empty_fields_per_file, fields_per_file


def emptyErrorReportValues(df, col):
    if not col in df.columns:
        df = df.reset_index()
    old_empty_values = list(df[col])
    new_empty_values = []
    for v in old_empty_values:
        if v.isalpha():
            new_empty_values += ["'"+v+"'"]
        elif v == "":
            new_empty_values += ["no value provided (e.g., <tag_name></tag_name)"]
        elif v == "\n":
            new_empty_values += ["newline (e.g., <tag_name>\n</tag_name>)"]
        else:
            new_empty_values += ["'"+str(v)+"'"]
    df = df.drop(columns=[col])
    df.insert(0, col, new_empty_values)
    return df


def contextInclusion(file_paths, data_model, context_pattern, context_url_pattern, context_var="@context"):
    error_raised, error_type, context_correct, has_context_var, has_model_url = [], [], [], [], []
    for file_path in file_paths:
        with open(file_path, "r") as f:
            f_string = f.read().lower()

            try:
                jsonld.expand(f_string)
                error_raised += [False]
            except Exception as e:
                error_raised += [e]
                error_type += [type(e)]

            if re.search(context_pattern, f_string):
                context_correct += [True]
                has_context_var += [True]
                has_model_url += [True]
            else:
                context_correct += [False]
                if context_var in f_string:
                    has_context_var += [True]
                else:
                    has_context_var += [False]
                if re.search(context_url_pattern, f_string):
                    has_model_url += [True]
                else:
                    has_model_url += [False]

            f.close()
    df = pd.DataFrame.from_dict({
        "file_path":file_paths, "data_model":[data_model]*len(file_paths), "error_type":error_type, "error_message":error_raised,
        "includes_context_correctly":context_correct, "includes_@context":has_context_var, "includes_data_model_url":has_model_url
        })

    return df


############################################################
################### CORRECTING METADATA ####################
############################################################



'''
Correct malformed Dublin Core XML by reading TXT versions of the files as strings
and re-writing the corrected versions as XML files.  By default, include an XML prolog.
'''
def correctXML(
        txt_errored_files, error_list, 
        dc_prefix_open_tag_simple=dc_prefix_open_tag_simple, dc_prefix_open_tag_qual=dc_prefix_open_tag_qual, dc_prefix_close_tag=dc_prefix_close_tag,
        dc_namespace=dc_namespace, dc_qual_namespace=dc_qual_namespace, rdf_namespace=rdf_namespace
               ):
    i, maxI = 0, len(error_list)
    still_incorrect = []
    while i < maxI:
        txt_file, message = txt_errored_files[i], error_list[i]
        
        with open(txt_file, "r") as f:
            f_string = f.read()
            f_string = f_string.strip()  # Remove any leading and trailing whitespace

            # Remove duplicated quotes surrounding text (not empty strings)
            dup_quotes = re.findall(".+", f_string)
            for dup_quote in dup_quotes:
                dedup = dup_quote.replace('""', '"')
                f_string = f_string.replace(dup_quote, dedup)
            
                if "Namespace prefix dc" in message:
                    # If dcterms tags are used, the record is a qualified DC record and
                    # should include the DC terms namespace
                    if "<dcterms:" in f_string:
                        dc_prefix_open_tag = dc_prefix_open_tag_qual
                    # Otherwise, the record is a simple DC record and should only include
                    # the namespace for the 15 core fields
                    else:
                        dc_prefix_open_tag = dc_prefix_open_tag_simple

                    # Find the name of the first open and last closing tags and, if they are a pair,
                    # replace them with tags that include the RDF and DC namespaces
                    last_close_tag = re.findall("<\/[a-z]+>$", f_string)
                    if len(last_close_tag) > 0:
                        first_open_tag_pattern = "<" + last_close_tag[0][2:-1] + "[^<]*>"
                        first_open_tag = re.findall(first_open_tag_pattern, f_string)
                        if len(first_open_tag) > 0:
                            # If the tags are a pair and they are not for a metadata field, replace them with the
                            # DC prefix tags defining the relevant namespace(s)
                            if not ("dc" in first_open_tag[0]):
                                f_string = f_string.replace(first_open_tag[0], dc_prefix_open_tag)
                                f_string = f_string.replace(last_close_tag[0], dc_prefix_close_tag)
                            else:
                                # If there is no pair of outermost tags surrounding all the metadata felds, add them,
                                # being sure to place them after the XML prolog if it exists
                                has_prolog = re.findall('<\?xml version="1.0"[^<]*>', f_string)
                                if len(has_prolog) > 0:
                                    f_string = f_string.replace(has_prolog[0], (has_prolog[0] + "\n" + dc_prefix_open_tag))
                                else:
                                    f_string = dc_prefix_open_tag + "\n" + f_string
                                f_string = f_string + "\n" + dc_prefix_close_tag
                                

                        # If the last closing tag doesn't have a matching opening tag, add the matching opening
                        # tag if there isn't already one that includes the DC and RDF namespaces, and replace
                        # the last closing tag if it is different from the expected DC closing tag
                        else:
                            f_string = dc_prefix_open_tag + "\n" + f_string
                            if last_close_tag[0] != dc_prefix_close_tag:
                                f_string = f_string.replace(last_close_tag[0], dc_prefix_close_tag)


                if "Namespace prefix rdf for about on Description" in message:
                    # If the RDF description tag is malformed, replace it with a well-formed one
                    rdf_desc_open_tag = re.findall('<rdf:Description rdf:about=.+>', f_string)
                    if len(rdf_desc_open_tag) > 0:
                        f_string = f_string.replace(rdf_desc_open_tag[0], '<rdf:Description rdf:about="http://www.w3.org/TR/rdf-syntax-grammar">')
                    
            f.close()

            # To validate that the new data is well-formed, try parsing it as XML
            # and, if successful, write the corrected file to a new directory 
            try:
                f_string = f_string.strip()  # Remove any leading and trailing whitespace
                root = ET.fromstring(f_string)
                xml_file = txt_file.replace(".txt", ".xml")
                corrected_file = xml_file.replace("cleaned", "corrected")
                with open(corrected_file, "w") as f:
                    f.write(f_string)
                    f.close()
            except Exception as e:
                new_error = {"file": txt_file, "exception_type": type(e), "exception_message": str(e)}
                still_incorrect += [new_error]

        i += 1

    return still_incorrect


# dc_prefix_open_tag_qual = '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/">'
# dc_prefix_open_tag_simple = '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dc="http://purl.org/dc/elements/1.1/">'
# dc_prefix_close_tag = '</rdf:RDF>'

# def correctDCXML(txt_errored_files, error_list, include_prolog=True, prolog=prolog, dc_prefix_open_tag_simple=dc_prefix_open_tag_simple, dc_prefix_open_tag_qual=dc_prefix_open_tag_qual, dc_prefix_close_tag=dc_prefix_close_tag):
#     i, maxI = 0, len(error_list)
#     still_incorrect_list = []
#     while i < maxI:
#         txt_file, message = txt_errored_files[i], error_list[i]
#         with open(txt_file, "r") as f:
#             f_string = f.read()
#             f_string = f_string.strip()  # Remove any leading and trailing whitespace

#             # Remove duplicated quotes surrounding text (not empty strings)
#             dup_quotes = re.findall(".+", f_string)
#             for dup_quote in dup_quotes:
#                 dedup = dup_quote.replace('""', '"')
#                 f_string = f_string.replace(dup_quote, dedup)
            
#             # if "dc" in message:

#             # If dcterms tags are used, the record is a qualified DC record and
#             # should include the DC terms namespace
#             if "<dcterms:" in f_string:
#                 dc_prefix_open_tag = dc_prefix_open_tag_qual
#             # Otherwise, the record is a simple DC record and should only include
#             # the namespace for the 15 core fields
#             else:
#                 dc_prefix_open_tag = dc_prefix_open_tag_simple
            
#             has_prefix_open_tag = re.findall('<[a-zA-Z]+ xmlns:dc.+">', f_string)
#             # Be sure that if dcterms tags are used, the record uses the DC terms namespace
#             if len(has_prefix_open_tag) > 0:
#                 if ("<dcterms:" in f_string) and not ("<dcterms:" in has_prefix_open_tag[0]):
#                     f_string = f_string.replace(has_prefix_open_tag[0], dc_prefix_open_tag)

            
#             else:
#                 # Make sure the Dublin Core namespace is properly included
#                 open_tag = re.findall('<[Dd]ublin.*[Cc]ore [\S]+>|<[Dd]ublin.*[Cc]ore>(?=[\s<])', f_string)
#                 if (len(open_tag) == 1):
#                     f_string = f_string.replace(open_tag[0], dc_prefix_open_tag)
#                 else:
#                     # If no namespaces are included, add them to the file
#                     f_string = dc_prefix_open_tag + "\n" + f_string

#                 # Be sure the file ends with the correct closing tag
#                 if not dc_prefix_close_tag in f_string:
#                     close_tag = re.findall("</[Dd]ublin.*[Cc]ore>", f_string)
#                     if (len(close_tag) == 1):
#                         f_string = f_string.replace(close_tag[0], dc_prefix_close_tag)
#                     else:
#                         has_prefix_close_tag = re.findall("<\/[a-zA-z]+>$", f_string)
#                         if len(has_prefix_close_tag) > 0:
#                             if has_prefix_close_tag[0] != dc_prefix_close_tag:
#                                 f_string = f_string.replace(has_prefix_close_tag[0], dc_prefix_close_tag)
#                         else:
#                             f_string = f_string + dc_prefix_close_tag

#             if "Namespace prefix rdf for about on Description is not defined" in message:
#                 rdf_desc_open_tag = re.findall('<rdf:Description rdf:about=.+>', f_string)
#                 f_string = f_string.replace(rdf_desc_open_tag[0], '<rdf:Description rdf:about="http://www.w3.org/TR/rdf-syntax-grammar">')

                
#             f.close()

#             # To validate that the new data is well-formed, try parsing it as XML
#             # and if successful, write the data as an XML file to a new directory,
#             # and if unsuccessful, write the data as a TXT file to that same directory.
#             try:
#                 f_string = f_string.strip()  # Remove any leading and trailing whitespace
#                 root = ET.fromstring(f_string)
#                 xml_file = txt_file.replace(".txt", ".xml")
#                 corrected_file = xml_file.replace("cleaned", "corrected")
#                 with open(corrected_file, "w") as f:
#                     f.write(f_string)
#                     f.close()
#             except Exception as e:
#                 still_incorrect_file = txt_file.replace("cleaned", "corrected")
#                 still_incorrect = {"file": still_incorrect_file, "exception_type": type(e), "exception_message": str(e)}
#                 still_incorrect_list += [still_incorrect]
#                 with open(still_incorrect_file, "w") as f:
#                     f.write(f_string)
#                     f.close()
        
#         i += 1

#     return still_incorrect_list
    

def correctJSON(txt_errored_files):
    still_incorrect = []
    comments_found = []
    new_syntax_errors = []
    for errored_file in txt_errored_files:
        with open(errored_file, "r") as f:
            f_string = f.read()
            # Check for and remove invalid comments in format: //, #, or /* */
            comments = re.findall("\n\s*\/\/\s*\w.+|\n\s*\/\*\s*.+\s*\*\/|\n\s*#\s*.+", f_string)
            if len(comments) > 0:
                comments_found += [{"errored_file": errored_file, "comment": comments}]
                for comment in comments:
                    f_string = f_string.replace(comment, "")
            
            # Check for double quotes surrounding field names and values (""..."" rather than "...")
            double_quotes = re.findall("""[@\w]+"":[\s\[\{]*"".+""", f_string)
            if len(double_quotes) > 0:
                f_string = f_string.replace('""', '"')
            
            # Check for missing curly brace at end of file
            open_brace = re.findall("\{", f_string)
            close_brace = re.findall("\}", f_string)
            if len(open_brace) == (len(close_brace) + 1):
                f_string = f_string + "\n}"
            elif (len(open_brace) > (len(close_brace) + 1)) or len(open_brace) < len(close_brace):
                errored_json = errored_file.replace(".txt", ".json")
                print("Please review file", errored_json, "manually and make sure that all open curly braces ({) are paired with a closing curly brace (}) and vice versa.")
                still_incorrect += [errored_file]

            f.close()

            # To validate that the JSON data has been corrected, write a new file
            # with the corrected string in a 'corrected' directory and try to load
            # the file as JSON data
            json_path = errored_file.replace(".txt", ".json")
            corrected_file = json_path.replace("cleaned", "corrected")
            with open(corrected_file, "w") as f_json:
                f_json.write(f_string)
                try:
                    data = json.load(f_json)
                except Exception as e:
                    f_error = {"file": json_path, "exception_type": type(e), "exception_message": str(e)}
                    new_syntax_errors += [f_error]
                    still_incorrect += [errored_file]
                f_json.close()

    return still_incorrect, comments_found, new_syntax_errors


# def checkDC():
#     i, maxI = 0, len(error_list)
#     still_incorrect = []
#     while i < maxI:
#         txt_file, message = txt_errored_files[i], error_list[i]
        
#         with open(txt_file, "r") as f:
#             f_string = f.read()
#             f_string = f_string.strip()  # Remove any leading and trailing whitespace

#                 # Find the name of the outermost tags and replace them with tags that include the RDF and DC namespaces
#                 last_close_tag = re.findall("<\/[a-z]+>$", f_string)
#                 try:
#                     last_close_tag = last_close_tag[0]
#                     first_open_tag_pattern = "<" + last_close_tag[2:-1] + "[^<]*>"
#                     try:
#                         first_open_tag = re.findall(first_open_tag_pattern, f_string)[0]
#                         f_string = f_string.replace(first_open_tag, dc_prefix_open_tag)
#                         f_string = f_string.replace(last_close_tag, dc_prefix_close_tag)
#                     except:
#                         new_error = {"file": txt_file, "exception_type": "Malformed XML", "exception_message": "Mismatched outermost opening and closing tags."}
#                         still_incorrect += [new_error]
#                 except:
#                     new_error = {"file": txt_file, "exception_type": "Malformed XML", "exception_message": "No closing tag found for outermost element."}
#                     still_incorrect += [new_error]

#             if "Namespace prefix rdf for about on Description" in message:
#                 # If the RDF description tag is malformed, replace it with a well-formed one
#                 rdf_desc_open_tag = re.findall('<rdf:Description rdf:about=.+>', f_string)
#                 try:
#                     f_string = f_string.replace(rdf_desc_open_tag[0], '<rdf:Description rdf:about="http://www.w3.org/TR/rdf-syntax-grammar">')
#                 except:
#                     new_error = {"file": txt_file, "exception_type": "Malformed XML", "exception_message": "No RDF description tag found."}
#                     still_incorrect += [new_error]
