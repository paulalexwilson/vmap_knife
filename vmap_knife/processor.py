"""
Processes the VMAP Ad Break Structure along with the Trace object
to produce a Report object.
"""

from vmap_knife import Vmap, Trace, Ad, AdBreak, Request
from typing import List
import re


class HttpCall:
    def __init__(self, requests: List[Request]):
        self.requests = requests


class AdReport:
    """
    """

    def __init__(self, ad: Ad, trace: Trace):
        self._ad = ad
        self._trace = trace
        self._process_ad_trace()

    def _process_ad_trace(self):
        self.adId = self._ad.adId
        self.sequence = self._ad.sequence
        self.is_wrapper = self._ad.is_wrapper
        self.impression = self._check_url_fired(self._ad.impression)
        self.error = self._check_error_fired(self._ad.error)
        self.tracking_calls = {}
        for trackingEvent, trackingUrl in self._ad.trackingEvents.items():
            tracedTrackingUrls = self._trace.requestForUrl(
                re.escape(trackingUrl), True)
            self.tracking_calls[trackingEvent] = HttpCall(
                tracedTrackingUrls)
        self.media_file_calls = []

    def _check_url_fired(self, url: str) -> HttpCall:
        tracedTrackingUrls = self._trace.requestForUrl(re.escape(url), True)
        return HttpCall(tracedTrackingUrls)

    def _check_error_fired(self, error: str) -> HttpCall:
        """
        Error beacons have special MACRO substitutions which make URL 
        matching trickier.
        These can be as %5BERRORCODE%5D or [ERRORCODE] it seems
        """
        error = re.escape(error)
        if '%5BERRORCODE%5D' in error:
            error_template = error.replace('%5BERRORCODE%5D', '.*')
        elif '[ERRORCODE]' in error:
            error_template = error.replace('[ERRORCODE]', '.*')
        tracedTrackingUrls = self._trace.requestForUrl(error_template, True)
        return HttpCall(tracedTrackingUrls)


class AdBreakReport:
    """
     TODO: Add slot impressions
    """

    def __init__(self, adBreakId: str, adBreakType: str, adBreakTimeOffset: str, adReports: List[AdReport]):
        self.adBreakId = adBreakId
        self.adBreakType = adBreakType
        self.adBreakTimeOffset = adBreakTimeOffset
        self.adReports = adReports


class TraceReport:
    def __init__(self, adBreakReports: List[AdBreakReport]):
        self.adBreakReports = adBreakReports


def process_trace_report(vmap: Vmap, trace: Trace) -> TraceReport:
    adBreaks = vmap.adBreaks
    adBreakReports: List[AdBreakReport] = []
    for adBreak in adBreaks:
        adBreakId = adBreak.breakId
        adBreakType = adBreak.breakType
        adBreakTimeOffset = adBreak.timeOffset
        adReports: List[AdReport] = []
        for ad in adBreak.ads:
            adReports.append(AdReport(ad, trace))
        adBreakReports.append(AdBreakReport(
            adBreakId, adBreakType, adBreakTimeOffset, adReports))
    return TraceReport(adBreakReports)
