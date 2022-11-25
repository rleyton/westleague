import pandas as pd
import numpy as np
import os
import glob
from .utils_consts import (
    SheetColumns,
    SheetType,
    DataStart,
    NAMES_GENDER_AGECAT,
    NAMES_GENDER,
    NAMES,
)


def fetch_clubs_from_dir(dir: str = None):
    clubs = None
    if dir is not None:
        clubs = []
        for event in glob.glob(dir + "/*.xlsx"):
            filename = os.path.basename(event)
            club = filename.split(".")[0]
            clubs.append((club, filename))
    return clubs


def extract_range(sheet, range):
    if sheet is not None and range is not None:
        columnsWide = SheetType[range]
        columnStart = SheetColumns[range]

        # TODO: better rule?
        dataSlice = sheet.loc[DataStart - 1 :]

        dataRange = (
            dataSlice[dataSlice.columns[columnStart - 1 : columnStart + columnsWide]]
            .dropna(how="all")
            .reset_index()
        )

        # check if it's all NaN
        if dataRange.iloc[:, 0].isnull().values.sum() >= len(dataRange):
            return None
        else:
            returnRange = pd.DataFrame()

            returnRange["names"] = dataRange[dataRange.columns[1]]

            if columnsWide >= NAMES_GENDER:
                returnRange["gender"] = dataRange[dataRange.columns[2]]

            if columnsWide >= NAMES_GENDER_AGECAT:
                returnRange["agecat"] = dataRange[dataRange.columns[3]]

            # reindex so it's zero indexed, don't care about previous index
            return returnRange.reset_index(drop="index")
