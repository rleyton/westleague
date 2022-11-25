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
