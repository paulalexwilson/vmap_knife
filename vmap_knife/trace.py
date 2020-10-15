"""
Models a collection of requests as a single Trace.
"""

from typing import TypedDict, Optional, List
from dataclasses import dataclass
from pandas import DataFrame
import pandas as pd


class Request:
    def __init__(self, row):
        self._row = row
        self.url = row['URL']
        self.method = row['Method']
        self.response_code = row['Response Code']
        self.status = row['Status']
        self.request_start = row['Request Start Time']
        self.request_end = row['Request End Time']
        self.duration_ms = row['Duration (ms)']

    def __str__(self):
        return str(self._row)

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'URL': self.url,
            'Method': self.method,
            'Response Code': self.response_code,
            'Status': self.status,
            'Request Start Time': self.request_start,
            'Request End Time': self.request_end,
            'Duration (ms)': self.duration_ms
        }


class Trace:
    """
    Represents a complete trace which can be queried.
    """

    def __init__(self, requests_frame: DataFrame = None, requests: List[Request] = None):
        if requests_frame is not None:
            self._requests_frame = requests_frame
            self._requests_frame.set_index('URL')
        elif requests is not None:
            self._requests_frame = pd.DataFrame.from_records(
                r.to_dict() for r in requests)
        else:
            raise Exception(
                "Provide either requests_frame or requests as constructor arguments to Trace")

    def requestForUrl(self, url: str, is_regex: bool = False) -> List[Request]:
        """
        Provides the Request object associated with the given URL.
        Since a Trace could contain multiple requests for the same
        URL a List of Request objects is returned. If no requests
        match the URL an empty list. Matching can be done via a Python
        regex is the boolean `is_regex` is set to `true`.
        """
        requestedUrls: List[Request] = []
        if not is_regex:
            matches = self._requests_frame.loc[self._requests_frame['URL'] == url]
            for _, row in matches.iterrows():
                requestedUrls.append(Request(row))
        else:
            matches = self._requests_frame.URL.str.contains(url)
            selected = self._requests_frame[matches]
            for _, row in selected.iterrows():
                requestedUrls.append(Request(row))
        return requestedUrls

    def __str__(self):
        return str(self._requests_frame)
