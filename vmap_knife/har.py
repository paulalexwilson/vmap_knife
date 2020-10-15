"""
Convienient access into a parsed HAR File.

Provides class-based representation of a HAR with convenience
methods for interrogating recorded traffic.
"""
from haralyzer import HarParser, HarPage
import json
from typing import TypedDict, NamedTuple


class Har:
    def __init__(self, har_data):
        self.har_data: HarRequestMap = {}

    def invokes_url(self, url) -> bool:
        return url in self.har_data


class HarRequest(NamedTuple):
    """Models a single request found within a HAR"""
    url: str


class HarRequestMap(TypedDict):
    """Maps a URL to a HarRequest for efficient lookup"""
    url: str
    request: HarRequest


def parse_har(har_file) -> Har:
    har_parser = HarParser(json.loads(har_file.read()))
    return _pre_parse(har_parser)


def _pre_parse(har_parser) -> Har:
    """Performs a pre-parsing step to populate an in-memory dict"""
    _request_map = HarRequestMap()
    for page in har_parser.pages:
        _request_map[page.url] = HarRequest(url=page.url)
#            for entry in page.entries:
#                response_body = entry['response']['content'].get('text', '')
# TODO: Place file size limit on HAR file
    return Har(_request_map)
