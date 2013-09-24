from unittest import TestCase

from pyramid import testing
from betahaus.pyracont.factories import createContent


class StatisticsViewTests(TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _fixture(self):
        from voteit.core.testing_helpers import register_catalog
        from voteit.core.testing_helpers import bootstrap_and_fixture
        from voteit.core.security import ROLE_VIEWER
        self.config.scan('voteit.core.models')
        self.config.testing_securitypolicy(userid='jane')
        register_catalog(self.config)
        root = bootstrap_and_fixture(self.config)
        root['m'] = meeting = createContent('Meeting')
        root['users']['jane'] = createContent('User')
        root['users']['tarzan'] = createContent('User')
        meeting.set_groups('jane', [ROLE_VIEWER], event = True)
        meeting.set_groups('tarzan', [ROLE_VIEWER], event = True)
        meeting['d'] = createContent('DiscussionPost', creators = ['jane'])
        meeting['d2'] = createContent('DiscussionPost', creators = ['jane'])
        meeting['poll'] = createContent('Poll')
        meeting['poll']['v'] = createContent('Vote', creators = ['jane'])
        meeting['p'] = createContent('Proposal', creators = ['jane'])
        meeting['p2'] = createContent('Proposal', creators = ['tarzan'])
        return root

    @property
    def _cut(self):
        from voteit.statistics.views import StatisticsView
        return StatisticsView

    def test_get_user_stats_reg(self):
        root = self._fixture()
        request = testing.DummyRequest()
        obj = self._cut(root['m'], request)
        self.assertEqual(obj.get_user_stats(['jane'], 'DiscussionPost'), {'jane': 2})
        self.assertEqual(obj.get_user_stats(['jane'], 'Proposal'), {'jane': 1})
        self.assertEqual(obj.get_user_stats(['tarzan'], 'Proposal'), {'tarzan': 1})
        self.assertEqual(obj.get_user_stats(['tarzan', 'jane'], 'Proposal'), {'jane': 1, 'tarzan': 1})

    def test_get_user_stats_votes(self):
        root = self._fixture()
        request = testing.DummyRequest()
        obj = self._cut(root['m'], request)
        self.assertEqual(obj.get_user_stats(['jane'], 'Vote'), {'jane': 1})
        self.assertEqual(obj.get_user_stats(['tarzan'], 'Vote'), {})

    def test_statistics_view(self):
        root = self._fixture()
        request = testing.DummyRequest()
        obj = self._cut(root['m'], request)
        res = obj.statisticts_view()
        self.assertEqual(res['results'], [{'display_name': u'Proposal',
                                           'stats': {u'jane': 1, u'tarzan': 1},
                                           'ctype': 'Proposal'},
                                          {'display_name': u'Discussion Post',
                                           'stats': {u'jane': 2},
                                           'ctype': 'DiscussionPost'},
                                          {'display_name': u'Vote',
                                           'stats': {u'jane': 1},
                                           'ctype': 'Vote'}])


    def test_statistics_menu_link_integration(self):
        root = self._fixture()
        request = testing.DummyRequest()
        self.config.include('voteit.statistics')
        obj = self._cut(root['m'], request)
        res = obj.api.render_single_view_component(root['m'], request, 'meeting', 'statistics')
        self.assertEqual(res, u'<li><a href="http://example.com/m/statistics">Statistics</a></li>')


class StatisticsTests(TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_integration(self):
        try:
            self.config.include('voteit.statistics')
        except Exception, e: # pragma : no cover
            self.fail(e)
