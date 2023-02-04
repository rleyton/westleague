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


def fetch_events(dir: str = None):
    if dir is not None:
        events = glob.glob(dir + "?")
        return events
    else:
        return None


def fetch_results_filenames(dir: str = None):
    results = None
    if dir is not None:
        results = []
        for result in glob.glob(dir + "/*.team.results.csv"):
            filename = os.path.basename(result)
            (eventname, agecat, gender) = filename.split(".")[:3]

            results.append(
                {
                    "filename": dir + "/" + filename,
                    "eventname": eventname,
                    "agecat": agecat,
                    "gender": gender,
                }
            )
    return results
