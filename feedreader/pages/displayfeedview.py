from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from feedreader.reader.database.databaseprovider import DatabaseProvider
from feedreader.reader.feed.form.newfeed.addfeed import AddFeedForm
from feedreader.reader.user.form.login.login import LoginForm
from feedreader.reader.user.form.management.manage import UserManageForm
from feedreader.reader.user.session.sessionhandler import SessionHandler
from feedreader.reader.feed.ParsedFeed import ParsedFeed

__author__ = 'Dietmar'


class DisplayFeedView(object):
    """
    Class for displayfeed view
    """

    @staticmethod
    def get(request):
        """
        static method for get
        """

        # redirect active session
        if SessionHandler.isUserSessionAlive(request.session):
            loginUser = SessionHandler.getSessionUser(request.session)

            if 'fid' in request.GET.keys():
                feedId = request.GET['fid']
                feed = DatabaseProvider.getFeedByUserIdAndFeedId(loginUser.id, feedId)  # gets the specific feed of the user
                parsedFeed = ParsedFeed(feed)

                feeds = DatabaseProvider.getFeedsByUserId(loginUser.id)  # gets all feeds of a user

                return render_to_response('displayfeed.html', {'feed': parsedFeed, 'feeds': feeds, 'user': loginUser}, context_instance=RequestContext(request))


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


        return HttpResponseRedirect('/feedreader/manage')

