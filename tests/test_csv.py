#!/usr/bin/env python

"""Tests for `csv` package."""

import unittest
import os
from vmap_knife import parse_csv, Trace
import re


class TestCsv(unittest.TestCase):

    def test_0000_shouldProvideAdBreakList(self):
        trace = parse_csv(_open_test_file(
            './test_files/Bitmovin845Stripped.csv'))
        requests = trace.requestForUrl(
            'https://jssdks.mparticle.com/v2/JS/4737f480f10a9542afc838d38d1b1d86/Events')

        assert len(requests) > 0

    def test_shouldAllowRegexSearch(self):
        trace = parse_csv(_open_test_file(
            './test_files/Bitmovin845Stripped.csv'))
        requests = trace.requestForUrl(
            re.escape("https://5e529.v.fwmrm.net/ad/l/1?s=d027&n=386345%3B386345&t=1602503513126642570&f=262144&r=386345&adid=47376614&reid=37278405&arid=0&auid=&cn=thirdQuartile&et=i&_cc=&tpos=0&init=1&iw=&uxnw=&uxss=&uxct=&metr=121"), True)

        assert len(requests) > 0


def _open_test_file(path):
    return os.path.join(os.path.dirname(__file__), path)
