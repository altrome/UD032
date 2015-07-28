"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
- check if the field "productionStartYear" contains a year
- check if the year is in range 1886-2014
- convert the value of the field to be just a year (not full datetime)
- the rest of the fields and values should stay the same
- if the value of the field is a valid year in range, as described above,
  write that line to the output_good file
- if the value of the field is not a valid year, 
  write that line to the output_bad file
- discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
- you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the 
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import csv
import pprint
import time

INPUT_FILE = 'autos.csv'
OUTPUT_GOOD = 'autos-valid.csv'
OUTPUT_BAD = 'FIXME-autos.csv'

def process_file(input_file, output_good, output_bad):

    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames

        #COMPLETE THIS FUNCTION
        good_data = []
        bad_data = []
        URI = "dbpedia.org"
        firstYear = 1886
        lastYear = 2014
        for line in reader:
            if sameURI(URI, line["URI"]):
                if containsYear(line[ "productionStartYear"]):
                    productionStartYear = time.strptime(line[ "productionStartYear"], "%Y-%d-%mT%H:%M:%S+02:00").tm_year
                    if inRange(productionStartYear, firstYear, lastYear):
                        line[ "productionStartYear"] = productionStartYear
                        good_data.append(line)
                    else:
                        bad_data.append(line)
                else:
                    bad_data.append(line)

        writeFile(output_good, good_data, header)
        writeFile(output_bad, bad_data, header)

def containsYear(date):
    date_parts= date.split('-')
    return date_parts[0].isdigit()

def inRange(year, start, end):
    return (year >= start and year <= end)

def writeFile(filename, data, header):
    with open(filename, "w") as g:
        writer = csv.DictWriter(g, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def sameURI(domain, URI):
    uri_parts = URI.split('/')
    try: 
        domainURI = uri_parts[2]
    except IndexError:
        domainURI = None 
    return domainURI == domain

    # This is just an example on how you can use csv.DictWriter
    # Remember that you have to output 2 files
    # with open(output_good, "w") as g:
    #     writer = csv.DictWriter(g, delimiter=",", fieldnames= header)
    #     writer.writeheader()
    #     for row in YOURDATA:
    #         writer.writerow(row)

def process_file_without_functions(input_file, output_good, output_bad):

    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames

        #COMPLETE THIS FUNCTION
        good_data = []
        bad_data = []
        URI = "dbpedia.org"
        firstYear = 1886
        lastYear = 2014
        for line in reader:
            if URI in line["URI"]:
                date_parts= line[ "productionStartYear"].split('-')
                if date_parts[0].isdigit():
                    productionStartYear = int(date_parts[0])
                    if productionStartYear >= firstYear and productionStartYear <= lastYear:
                        line[ "productionStartYear"] = productionStartYear
                        good_data.append(line)
                    else:
                        bad_data.append(line)
                else:
                    bad_data.append(line)

        with open(output_good, "w") as g:
            writer = csv.DictWriter(g, delimiter=",", fieldnames= header)
            writer.writeheader()
            for row in good_data:
                writer.writerow(row)
        
        with open(output_bad, "w") as g:
            writer = csv.DictWriter(g, delimiter=",", fieldnames= header)
            writer.writeheader()
            for row in bad_data:
                writer.writerow(row)

def test():

    #process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)
    process_file_without_functions(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)


if __name__ == "__main__":
    test()

