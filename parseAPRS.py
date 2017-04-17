import aprslib

# define filenames of input and output files
input_filename = "sample_packets/KG5RHL-11_raw.txt"
output_filename = "sample_packets/KG5RHL-11_parsed.txt"

# these are all the possible fields contained within the APRS data. You don't have to use all of them (see desired_fields)
all_fields = ['from', 'via', 'path', 'to', 'latitude', 'longitude', 'altitude', 'posambiguity', 'course', 'speed', 'format', 'messagecapable', 'symbol', 'symboltable', 'raw', 'comment']

# define which fields will be written into the output file
desired_fields = {'latitude', 'longitude', 'altitude', 'from'}

# define string to use in case of null data (field does not exist in packet)
null_data_value = "NA"

# read all lines of input file
with open(input_filename, "r") as input_file:
    input_lines = input_file.readlines()

# create array to hold timestamps
timestamps = []

# populate timestamps
for row in range(0, len(input_lines)):
    current_line = input_lines[row].split(': ')
    timestamps.append(current_line[0])
    input_lines[row] = current_line[1]

# open output and write header, then write parsed APRS data
with open(output_filename, "w") as output_file:
    output_file.write('timestamp,' + ','.join(desired_fields) + '\n')
    
    # for each row in the input data, parse the APRS data using aprslib and extract the desired fields
    for row in range(0, len(input_lines)):     
        # parse data and append timestamp to front   
        current_line_all_fields = aprslib.parse(input_lines[row])
        current_line_desired_fields = [str(timestamps[row])]

        # extract and append desired fields, preservign CSV format
        for field in desired_fields:
            if field in current_line_all_fields:
                # replace commas in data with semicolons to preserve CSV format
                current_line_desired_fields.append(str(current_line_all_fields[field]).replace(',', ';'))
            else:
                # if the field is not in the current APRS packet, append the null data value instead
                current_line_desired_fields.append(null_data_value)
        
        # write line to output file
        output_file.write(','.join(current_line_desired_fields) + '\n')
