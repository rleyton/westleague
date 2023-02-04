import json


def json_write(object=None, filename: str = None):

    with open(filename, "w") as fh:
        json.dump(object, fh, indent=6)


def json_load(filename: str = None):
    with open(filename, "r") as fh:
        object = json.load(fh)
        return object
