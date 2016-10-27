from flask import json

def save_dataset(filename, dataset):
    with open(filename, 'w') as f:
        print 'Saving:', filename
        dataset.serialize(f, format='trig')
    print 'Saved.'
    print

def save_json(filename, data):
    with open(filename, 'w') as f:
        print 'Saving:', filename
        json.dump(data, f)
    print 'Saved.'
    print