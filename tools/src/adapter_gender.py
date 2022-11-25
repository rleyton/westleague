import pandas
import numpy


def gender_process(df, genderdf):
    if df is not None and genderdf is not None:
        if "team" not in df:
            raise Exception("Not a placings dataframe - expecting team column")
        else:
            df["gender"] = df["team"].str[-1:]

    return df
