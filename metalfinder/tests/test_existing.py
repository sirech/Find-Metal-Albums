# -*- coding: utf-8 -*-
from test_base import BaseTest
from metalfinder.existing import process_band_name, Finder

from mock import patch

class ExistingTest(BaseTest):

    def setUp(self):
        super(ExistingTest,self).setUp()
        self.path_patcher = patch('os.path')
        self.listdir_patcher = patch('os.listdir')
        self.path = self.path_patcher.start()
        self.listdir = self.listdir_patcher.start()
        self.listdir.return_value = set(sorted([u'SKA-P',
                                                u'Within Temptation',
                                                u'Metallica',
                                                u'Héroes del Silencio',
                                                u'Rage against the machine',
                                                u'invalid']))
        self.path.join.side_effect = lambda path1, path2 : path2
        self.path.isdir.side_effect = lambda name : name != u'invalid'
        self.finder = Finder(self.config)

    def tearDown(self):
        super(ExistingTest,self).tearDown()
        self.path_patcher.stop()
        self.listdir_patcher.stop()

    def test_process_band_name(self):
        self.assertEqual(process_band_name(u'Within Temptation'), u'withintemptation')

    def test_process_band_name_special(self):
        self.assertEqual(process_band_name(u'SKA-P'), u'skap')

    def test_process_band_name_accent(self):
        self.assertEqual(process_band_name(u'Héroes del Silencio'), u'heroesdelsilencio')

    def test_bands(self):
        self.assertEqual(len(list(self.finder.bands)), 5)

    def test_bands_members(self):
        for band in [u'metallica', u'heroesdelsilencio', u'skap', u'withintemptation', u'rageagainstthemachine']:
            self.assertTrue(band in self.finder.bands)
