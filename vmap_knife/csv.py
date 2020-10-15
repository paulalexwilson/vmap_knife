"""

"""
from vmap_knife import Trace, Request
from typing import IO, Any
import pandas


def parse_csv(csv_file: str) -> Trace:
    df = pandas.read_csv(csv_file)
    return Trace(df)
