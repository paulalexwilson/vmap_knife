#!/usr/bin/env python

"""Tests for `vmap` package."""

import unittest
import os
from vmap_knife import process_trace_report, parse_csv, parse_vmap


class TestProcessor(unittest.TestCase):
    def test_should_provide_adBreak_list(self):
        with open(_open_test_file('./vmaps/test-vmap.xml'), 'r') as f:
            trace = parse_csv(_open_test_file(
                './test_files/Bitmovin845Stripped.csv'))
            vmap = parse_vmap(f)
            traceReport = process_trace_report(vmap, trace)
            for adbreak in traceReport.adBreakReports:
                pass


def _open_test_file(path):
    return os.path.join(os.path.dirname(__file__), path)
