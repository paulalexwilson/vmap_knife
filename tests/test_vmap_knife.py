#!/usr/bin/env python

"""Tests for `vmap_knife` package."""


import unittest
import os
from click.testing import CliRunner

from vmap_knife import vmap_knife
from vmap_knife import cli


def _open_test_file(path):
    return os.path.join(os.path.dirname(__file__), path)


csv_path = _open_test_file('test_files/Bitmovin845Stripped.csv')
vmap_path = _open_test_file('vmaps/test-vmap.xml')


class TestVmap_knife(unittest.TestCase):
    """Tests for `vmap_knife` package."""

    def test_000_report_generation(self):
        runner = CliRunner()
        result = runner.invoke(
            cli.main, args=[
                '--csvfile', csv_path,
                '--vmapfile', vmap_path,
                '--outputfile', 'report2.html'], catch_exceptions=False)
