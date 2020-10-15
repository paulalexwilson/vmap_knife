#!/usr/bin/env python

"""Tests for `har` package."""

import unittest
import os
from click.testing import CliRunner
from vmap_knife import parse_har


class TestHar(unittest.TestCase):

    @unittest.skip("skipping")
    def test_0000_shouldProvideAdBreakList(self):
        with open(_open_test_file('./binaries/Bitmovin845Stripped.har'), 'r') as f:
            har = parse_har(f)
            assert har.invokes_url("")


def _open_test_file(path):
    return os.path.join(os.path.dirname(__file__), path)
