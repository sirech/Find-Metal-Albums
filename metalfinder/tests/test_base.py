import unittest
import copy

class BaseTest(unittest.TestCase):

    def setUp(self):
        from test_data.test_config import py
        self.config = copy.deepcopy(py)
