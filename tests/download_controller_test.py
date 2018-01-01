#!/usr/bin/env python3
# encoding: utf-8

import os, sys

import unittest
from nose.plugins.attrib import attr

from omad.download_controller import DownloadController

from omad.mangafox_model import MangafoxModel
from omad.batoto_model import BatotoModel

class DownloadControllerTest(unittest.TestCase):
    # if error, always first check if urls are not bad
    # testchapters should have special non-ASCII characters in their names

    # mangafox shows all manga as licensed when viewed from USA
    # needs to be korean/chinese comix to work on Travis
    mangafox_series_url = 'http://mangafox.me/manga/0_0_mhz/'
    # only recently uploaded chapters are shown to not logged in user
    batoto_series_url = 'https://bato.to/comic/_/comics/freezing-r43'

    def select_url_bad_test(self):
        dc = DownloadController()
        r = dc.setSeriesUrl("http://www.google.com")

        self.assertFalse(r)
        self.assertTrue( dc.webpage_model is None )

    @attr(site='mangafox')
    def select_url_mangafox_test(self):
        dc = DownloadController()
        r = dc.setSeriesUrl(self.mangafox_series_url)

        self.assertTrue(r)
        self.assertTrue( isinstance(dc.webpage_model, MangafoxModel) )

    @attr(site='batoto')
    def select_url_batoto_test(self):
        dc = DownloadController()
        r = dc.setSeriesUrl(self.batoto_series_url)

        self.assertTrue(r)
        self.assertTrue( isinstance(dc.webpage_model, BatotoModel) )

    def bad_series_url_test(self):
        dc = DownloadController()
        r = dc.setSeriesUrl(self.mangafox_series_url+"asdfgh")

        self.assertFalse(r)
        self.assertTrue( dc.webpage_model is None )

    def download_path_test(self):
        dpath = "./"
        dc = DownloadController()
        dc.setDownloadPath(dpath)
        r = dc.getDownloadPath()

        self.assertEqual(os.path.abspath(dpath), os.path.abspath(r))

    def download_range_test(self):
        dc = DownloadController()
        dc.setSeriesUrl(self.mangafox_series_url)
        r = dc.downloadChapterRange(0, 1)

        self.assertFalse(False in r)
