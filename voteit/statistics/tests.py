from unittest import TestCase

from pyramid import testing


class StatisticsTests(TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_integration(self):
        self.config.include('voteit.statistics')
        