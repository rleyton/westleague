import glob
import os


def fetch_events_from_dir(dir: str = None):
    events = None
    if dir is not None:
        events = []
        for event in glob.glob(dir + "/*.meta.csv"):
            filename = os.path.basename(event)
            eventname = filename.split(".")[0]
            events.append(eventname)
    return events


def fetch_volunteers_from_dir(dir: str = None):
    if dir is not None:
        volunteers = glob.glob(dir + "/volunteers.csv")

        if len(volunteers) > 0:
            return volunteers[0]
    else:
        return None
