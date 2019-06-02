import csv
import re
import petl

IN_FILE = './offices.csv'
OUT_FILE = './offices_clean.csv'
LOC_FILE = './Office_Locations.csv'
SERVICES_FILE = './Office_Services.csv'

regional_code = {"NSW": "02", "VIC": "03", "QLD": "07", "SA": "09"}

international_code = "(+61)"

with open(IN_FILE, 'r') as infile, open(OUT_FILE, "w") as outfile:
    csv_reader = csv.reader(infile)
    writer = csv.writer(outfile)
    headers = next(csv_reader, None)  #skipping header row
    writer.writerow(headers)
    for row in csv_reader:
        number_column = row[5]
        state_column = row[3]
        clean_num = re.sub("\D", "", row[5])[-8:]
        formatted_num = international_code + " " + regional_code[
            state_column] + " " + clean_num
        row[5] = formatted_num
        writer.writerow(row)

services = petl.fromcsv(SERVICES_FILE)
offices = petl.fromcsv(OUT_FILE)
offices = offices.rename({"Contact Name": "Office", "Phone Number": "Phone"})
offices = petl.cutout(offices,"State","Postcode")

locations = petl.fromcsv(LOC_FILE)
locations = locations.rename({"officeID": "OfficeID"})
office_service = petl.join(services, offices, key='OfficeID')

office_service_locations = petl.join(
    office_service, locations, key='OfficeID')

office_service_locations = petl.convert(office_service_locations,'OfficeServiceID',int)
office_service_locations = petl.sort(office_service_locations,'OfficeServiceID')
petl.tocsv(office_service_locations, 'office_service_locations.csv')