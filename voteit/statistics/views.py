from pyramid.view import view_config
from pyramid.traversal import resource_path
from betahaus.viewcomponent.decorators import view_action
from voteit.core.models.interfaces import IMeeting
from voteit.core.views.base_view import BaseView
from voteit.core.security import VIEW
from voteit.core.security import find_authorized_userids
from voteit.core.models.discussion_post import DiscussionPost
from voteit.core.models.proposal import Proposal
from voteit.core.models.vote import Vote

from voteit.statistics import StatisticsMF as _


class StatisticsView(BaseView):

    @view_config(name = 'statistics', context = IMeeting, permission = VIEW,
                 renderer = 'statistics.pt')
    def statisticts_view(self):
        """ Show statistics for all users that have view permission in this meeting.
            This might be a CPU expensive view, so be carefull.
        """
        userids = find_authorized_userids(self.api.meeting, [VIEW])
        ctypes = self.request.registry.settings.get('statistics.ctypes',
                                                    'Proposal\nDiscussionPost\nVote')
        ctypes = ctypes.strip().splitlines()
        results = []
        for ctype in ctypes:
            factory = self.api.get_content_factory(ctype)
            results.append(dict(stats = self.get_user_stats(userids, ctype),
                                ctype = ctype,
                                display_name = getattr(factory._callable, 'display_name', ctype)))
        self.response['userids'] = userids
        self.response['results'] = results
        return self.response

    def get_user_stats(self, userids, content_type):
        """ This method is now tweaked which might look funny. The reason for this is that it
            was written when votes were part of the catalog. Nowdays they aren't. Hence the split.
        """
        path = resource_path(self.api.meeting)
        results = {}
        if content_type == u'Vote':
            for docid in self.api.search_catalog(path = path, content_type = u'Poll')[1]:
                poll = self.api.resolve_catalog_docid(docid)
                for vote in poll.get_content(content_type = u'Vote'):
                    creator = vote.creators[0]
                    if creator not in userids:
                        continue
                    current = results.setdefault(creator, 0)
                    results[creator] = current + 1
            return results
        #Default
        for userid in userids:
            num = self.api.search_catalog(path = path,
                                          content_type = content_type,
                                          creators = userid)[0]
            if num:
                results[userid] = num
        return results


@view_action('meeting', 'statistics', title = _(u"Statistics"), link = "statistics")
def statistics_menu_link(context, request, va, **kw):
    """ Show a link to the statistics page in the  meeting menu """
    api = kw['api']
    url = "%s%s" % (api.meeting_url, va.kwargs['link'])
    return """<li><a href="%s">%s</a></li>""" % (url, api.translate(va.title))
