import sys
import os
import aprslib

if len(sys.argv) == 1:
    input_filename = "sample_packets/KG5RHL-11_raw.txt"
    output_filename = "sample_packets/KG5RHL-11_parsed.txt"
elif len(sys.argv) == 2:
    input_filename = sys.argv[1]
    output_filename = "%s_parsed.txt" % (os.path.splitext(input_filename)[0])
elif len(sys.argv) == 3:
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

# these are all the possible fields contained within the APRS data. You don't have to use all of them (see desired_fields)
all_fields = ['from', 'via', 'path', 'to', 'latitude', 'longitude', 'altitude', 'posambiguity', 'course', 'speed', 'format', 'messagecapable', 'symbol', 'symboltable', 'raw', 'comment']

# define which fields will be written into the output file
desired_fields = ['latitude', 'longitude', 'altitude', 'speed', 'course', 'from', 'comment']

# define string to use in case of null data (if a certain field does not exist in a packet)
null_data_string = "NA"

# read all lines of input file
with open(input_filename, "r") as input_file:
    aprs_packets = input_file.readlines()

# create array to hold timestamps
timestamps = []

# populate timestamps with first value in every line (ended by a colon) before actual APRS packet
for packet_index in range(0, len(aprs_packets)):
    current_line = aprs_packets[packet_index].split(': ')
    timestamps.append(current_line[0])
    aprs_packets[packet_index] = current_line[1]

# open output and write header, then write parsed APRS data
with open(output_filename, "w") as output_file:
    output_file.write('timestamp,' + ','.join(desired_fields) + '\n')
    
    # for each line in the input data, parse the APRS data using aprslib and extract the desired fields
    for packet_index in range(0, len(aprs_packets)):     
        # parse data and append timestamp to front   
        current_aprs_packet = aprslib.parse(aprs_packets[packet_index])
        current_output_data = [str(timestamps[packet_index])]

        # extract and append desired fields, preserving CSV format by replacing commas with semicolons
        for field_index in range(0, len(desired_fields)):
            # get current field name
            field = desired_fields[field_index]
            
            # check if field exists in current packet
            if field in current_aprs_packet:
                # replace commas in data with semicolons to preserve CSV format
                current_output_data.append(str(current_aprs_packet[field]).replace(',', ';'))
            else:
                # if the field is not in the current APRS packet, append the null data value instead
                current_output_data.append(null_data_string)
        
        # write line to output file
        output_file.write(','.join(current_output_data) + '\n')
