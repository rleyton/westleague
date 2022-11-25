import pandas as pd
from .utils_consts import CLUB_PARSED, DATA_DIR
import glob
import os


def process_teams(df, teamdf):
    if df is not None and teamdf is not None:
        if "team" not in df:
            raise Exception("Not a placings dataframe - expecting team column")
        else:
            df["clubnumber"] = pd.to_numeric(df["team"].str[:-1])

    joined = df.join(other=teamdf, on="clubnumber")
    return joined


def load_team_submissions(event):
    if event is not None:
        submissions = {}
        for clubSubmission in glob.glob(
            DATA_DIR + "/" + CLUB_PARSED + "/*" + event + ".csv"
        ):
            filename = os.path.basename(clubSubmission)
            clubNumber = int(filename.split(".")[0])
            df = pd.read_csv(clubSubmission)
            submissions[clubNumber] = df

        return submissions
