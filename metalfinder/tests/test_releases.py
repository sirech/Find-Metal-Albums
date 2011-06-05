# -*- coding: utf-8 -*-
from test_base import BaseTest
from metalfinder.releases import Scrapper

from mock import patch, Mock

class ReleasesTest(BaseTest):

    def setUp(self):
        super(ReleasesTest,self).setUp()
        self.scrapper = Scrapper(self.config)
        self.opener = Mock()
        self.opener.open.return_value = open('test_data/2011.html')
        self.scrapper._opener = self.opener

    def _get_soup(self):
        return self.scrapper._soupify('')

    def _get_existing(self):
        self.scrapper._cfg['existing_file'] = 'test_data/existing'
        self.scrapper._existing = self.scrapper._load_existing()
        return self.scrapper._existing

    def test_load_existing_empty(self):
        self.assertEqual(self.scrapper._load_existing(), set())

    def test_load_existing(self):
        self.assertEqual(len(self._get_existing()), 173)

    def test_soupify(self):
        self.assertEqual(self._get_soup().name, u'[document]')

    def test_albums_for_month(self):
        albums = self.scrapper._albums_for_month(self._get_soup(), 'January')
        self.assertEqual(len(albums), 25)
        self.assertEqual(albums[13], (u'Sirenia', u'The Enigma of Life', 21))

    def test_albums_for_month_with_existing(self):
        self._get_existing()
        albums = self.scrapper._albums_for_month(self._get_soup(), 'March')
        self.assertEqual(len(albums), 4)
        self.assertEqual(albums[0], (u'Children of Bodom', u'Relentless Reckless Forever', 2))

    def test_albums(self):
        self._get_existing()
        albums = self.scrapper.albums

        total = 0
        for _,lst in albums:
            total += len(lst)

        self.assertEqual(total, 15)
