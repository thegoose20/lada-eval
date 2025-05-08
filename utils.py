import os, re

"""
Write the Dublin Core XML records to a directory.
"""
def write_dc_xml(records_ids_list, dc_records_list, dc_directory):
    i, maxI = 0, len(records_ids_list)
    while i < maxI:
        id = str(int(records_ids_list[i]))
        record = dc_records_list[i]
        
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
            file_prefix = "dc_record_"
            file_suffix = ".xml"
            if len(id) == 1:
                file_id = "00" + id
            elif len(id) == 2:
                file_id = "0" + id
            else:
                file_id = id
            filename = file_prefix + file_id + file_suffix
            filepath = dc_directory+filename

            with open(filepath, "w") as file:
                for line in xml_data:
                    file.write(line)
                    file.write("\n")
            file.close()
            print("Wrote", filename+"!")

        i += 1
