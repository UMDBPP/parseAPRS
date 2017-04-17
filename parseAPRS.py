import aprslib

input_filename = "sample_packets/KG5RHL-11_raw.txt"
output_filename = "sample_packets/KG5RHL-11_parsed.txt"

header = ['DateTime', 'Latitude', 'Longitude', 'Altitude_m', 'Callsign']

with open(input_filename, "r") as input_file:
    lines = input_file.readlines()

timestamps = []

for row in range(0, len(lines)):
    line = lines[row].split(': ')
    timestamps.append(line[0])
    lines[row] = line[1]

with open(output_filename, "w") as output_file:
    output_file.write(','.join(header) + '\n')
    for row in range(0, len(lines)):        
        aprs = aprslib.parse(lines[row])
        line_data = [str(timestamps[row])]

        if 'latitude' in aprs:
            line_data.append(str(aprs['latitude']))

        if 'longitude' in aprs:
            line_data.append(str(aprs['longitude']))

        if 'altitude' in aprs:
            line_data.append(str(aprs['altitude']))
        else:
            line_data.append(str(0))

        if 'from' in aprs:
            line_data.append(str(aprs['from']))
        
        output_file.write(','.join(line_data) + '\n')
