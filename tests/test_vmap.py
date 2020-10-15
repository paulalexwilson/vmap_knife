#!/usr/bin/env python

"""Tests for `vmap` package."""

import unittest
import os
from vmap_knife import parse_vmap


class TestVmap_knife(unittest.TestCase):

    def test_should_provide_adBreak_list(self):
        with open(_open_test_file('./vmaps/test-vmap.xml'), 'r') as f:
            vmap = parse_vmap(f)
            adbreak_1 = vmap.adBreaks[0]
            assert adbreak_1.breakId == 'cue_point-628937079'
            assert adbreak_1.ads[0].adId == '17639838.140264947470848'

    def test_should_provide_tracking_events(self):
        with open(_open_test_file('./vmaps/test-vmap.xml'), 'r') as f:
            vmap = parse_vmap(f)
            ad = vmap.adBreaks[0].ads[0]
            trackingEvents = ad.trackingEvents
            assert 'complete' in trackingEvents


def _open_test_file(path):
    return os.path.join(os.path.dirname(__file__), path)
