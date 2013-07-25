from feedreader.reader.feed.feedfilter import SearchFeed

__author__ = 'Roland Reitboeck'

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from feedreader.reader.database.databaseprovider import DatabaseProvider
from feedreader.reader.feed.form.newfeed.addfeed import AddFeedForm
from feedreader.reader.user.form.management.manage import UserManageForm
from feedreader.reader.user.session.sessionhandler import SessionHandler
from feedreader.reader.feed.ParsedFeed import ParsedFeed


class SearchFeedView(object):
    """
    Class for search view
    """

    @staticmethod
    def get(request):
        """
        static method for get
        """

        # redirect active session
        if SessionHandler.isUserSessionAlive(request.session):
            loginUser = SessionHandler.getSessionUser(request.session)

            if 'keywords' in request.GET.keys():
                keywords = request.GET['keywords']  # gets keywords from URL as string
                feeds = DatabaseProvider.getFeedsByUserId(loginUser.id)  # gets feed list of the user

                filter = SearchFeed(feeds, keywords)  # get feed information

                parsedFeeds = filter.getFilteredFeeds()
                count = len(parsedFeeds)

                feeds = DatabaseProvider.getFeedsByUserId(loginUser.id)  # gets all feeds of a user

                return render_to_response('search.html', {'parsedFeeds': parsedFeeds, 'user': loginUser,
                                                          'keywords': keywords, 'count': count, 'feeds': feeds},
                                          context_instance=RequestContext(request))

        return HttpResponseRedirect('/feedreader/')

    @staticmethod
    def post(request):
        """
        static method for post
        """

        if 'submitSearch' in request.POST:
            searchValue = request.POST['submitSearch']
            values = searchValue.replace(' ', '+')

            return HttpResponseRedirect('/feedreader/search/?keywords=' + values)


        return HttpResponseRedirect('/feedreader/search')

