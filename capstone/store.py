import json

def save_to_file(file_format, filename, data):
    if file_format == 'json':
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)
    if file_format == 'csv':
        print('not implemented')
