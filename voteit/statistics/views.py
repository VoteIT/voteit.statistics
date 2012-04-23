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
        ctypes = [DiscussionPost.content_type, Proposal.content_type, Vote.content_type]
        display_names = {'DiscussionPost': DiscussionPost.display_name,
                         'Proposal': Proposal.display_name,
                         'Vote': Vote.display_name}
        results = []
        for ctype in ctypes:
            results.append(dict(stats = self.get_user_stats(userids, ctype),
                                ctype = ctype,
                                display_name = display_names[ctype]))
        self.response['userids'] = userids
        self.response['results'] = results
        return self.response

    def get_user_stats(self, userids, content_type):
        path = resource_path(self.api.meeting)
        results = {}
        for userid in userids:
            num = self.api.search_catalog(path = path,
                                          content_type = content_type,
                                          creators = userid)[0]
            if num:
                results[userid] = num
        return results


@view_action('meeting', 'statistics', title = _(u"Statistics"), link = "@@statistics")
def statistics_menu_link(context, request, va, **kw):
    """ Show a link to the statistics page in the  meeting menu """
    api = kw['api']
    url = "%s%s" % (api.meeting_url, va.kwargs['link'])
    return """<li><a href="%s">%s</a></li>""" % (url, api.translate(va.title))
