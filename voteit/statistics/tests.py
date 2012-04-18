from unittest import TestCase


class StatisticsTests(TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_integration(self):
        self.config.include('voteit.statistics')
        