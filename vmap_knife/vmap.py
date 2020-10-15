"""
Provides datastructures for accessing metadata stored
within a VMAP document.
"""
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from dataclasses import dataclass
from datetime import timedelta
from typing import List, Dict
from typing import Optional

VMAP_NAMESPACE_MAP = {'vmap': 'http://www.iab.net/vmap-1.0'}


@dataclass
class Ad:
    adId: str
    is_wrapper: bool
    sequence: Optional[int]
    title: str
    vast_ad_tag: Optional[str]
    error: Optional[str]
    impression: Optional[str]
    trackingEvents: Dict
    mediaFiles: List


class AdBreak:
    def __init__(self, breakId: str, breakType: str, timeOffset: str, ads: List[Ad]):
        self._breakId = breakId
        self._breakType = breakType
        self._timeOffset = timeOffset
        self._ads = ads or []

    def push_ad(self, ad: Ad):
        self._ads.append(ad)

    @property
    def ads(self) -> List[Ad]:
        return self._ads

    @property
    def breakId(self):
        return self._breakId

    @property
    def breakType(self):
        return self._breakType

    @property
    def timeOffset(self):
        return self._timeOffset


class Vmap:
    """Represents a VMAP document"""

    def __init__(self):
        self._adBreaks = []

    def push_adBreak(self, ad: AdBreak) -> None:
        self._adBreaks.append(ad)

    @property
    def adBreaks(self) -> List[AdBreak]:
        return self._adBreaks


def parse_vmap(vmap_path) -> Vmap:
    tree = ET.parse(vmap_path)
    root = tree.getroot()
    vmap = Vmap()
    for xml_adbreak in root:
        breakId = xml_adbreak.attrib['breakId']
        breakType = xml_adbreak.attrib['breakType']
        timeOffset = xml_adbreak.attrib['timeOffset']
        ads = parseAds(xml_adbreak)
        vmap.push_adBreak(AdBreak(breakId=breakId,
                                  breakType=breakType,
                                  timeOffset=timeOffset,
                                  ads=ads))
    return vmap


def parseAds(adbreak_element: Element) -> List[Ad]:
    ad_elements = adbreak_element.findall(
        './vmap:AdSource/vmap:VASTAdData/VAST/Ad', VMAP_NAMESPACE_MAP)
    ads: List[Ad] = []
    for ad_element in ad_elements:
        adId = ad_element.attrib['id']
        if 'sequence' in ad_element.attrib:
            sequence = ad_element.attrib['sequence']
        else:
            sequence = None
        inlineElement = ad_element.find('InLine')
        wrapperElement = ad_element.find('Wrapper')
        if inlineElement is not None:
            title = inlineElement.find('AdTitle').text
            error_beacon = inlineElement.find('Error').text
            impression = inlineElement.find('Impression').text
            trackingEvents = _parseTrackingEvents(inlineElement)
            ads.append(Ad(adId=adId, is_wrapper=False, sequence=sequence, title=title,
                          error=error_beacon, vast_ad_tag=None,
                          impression=impression, trackingEvents=trackingEvents, mediaFiles=[]))
        else:
            vast_ad_tag = wrapperElement.find('VASTAdTagURI').text
            error_beacon = wrapperElement.find('Error').text
            impression = wrapperElement.find('Impression').text
            trackingEvents = _parseTrackingEvents(wrapperElement)
            ads.append(Ad(adId=adId, is_wrapper=True, sequence=sequence, title=None,
                          error=error_beacon, vast_ad_tag=vast_ad_tag,
                          impression=impression, trackingEvents=trackingEvents, mediaFiles=[]))
    return ads


def _parseTrackingEvents(element: Element) -> Dict:
    trackingEventDict = {}
    trackingEventsElement = element.find(
        './Creatives/Creative/Linear/TrackingEvents')
    trackingEventElements = trackingEventsElement.findall('Tracking')
    for trackingEvent in trackingEventElements:
        event = trackingEvent.attrib['event']
        url = trackingEvent.text
        trackingEventDict[event] = url
    return trackingEventDict
