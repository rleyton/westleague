from .adapter_json import json_load
from .utils_config import TEAMS
import pandas as pd


def load_clubs():
    return pd.read_csv(TEAMS, index_col="Number")
