import json

def save_to_file(file_format, filename, data):
    if file_format == 'json':
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)
    if file_format == 'csv':
        print('not implemented')

def load_from_file(file_format, filename):
    if file_format == 'json':
        dataset = None
        with open(filename, 'r') as infile:
            dataset = json.loads(infile.read())
        return dataset
    if file_format == 'csv':
        print('not implemented')
