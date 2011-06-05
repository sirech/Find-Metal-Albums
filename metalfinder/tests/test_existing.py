# -*- coding: utf-8 -*-
from test_base import BaseTest
from metalfinder.existing import process_band_name, Finder

class ExistingTest(BaseTest):

    def setUp(self):
        super(ExistingTest,self).setUp()

    def test_process_band_name(self):
        self.assertEqual(process_band_name(u'Within Temptation'), u'withintemptation')

    def test_process_band_name_special(self):
        self.assertEqual(process_band_name(u'SKA-P'), u'skap')

    def test_process_band_name_accent(self):
        self.assertEqual(process_band_name(u'Héroes del Silencio'), u'heroesdelsilencio')

