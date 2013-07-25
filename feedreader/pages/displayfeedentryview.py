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


class DisplayFeedEntryView(object):
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

            if 'fid' in request.GET.keys() and 'eid' in request.GET.keys():
                fid = request.GET['fid']
                eid = request.GET['eid']
                feeds = DatabaseProvider.getFeedsByUserId(loginUser.id)  # gets the feeds of the user
                feed = DatabaseProvider.getFeedByUserIdAndFeedId(loginUser.id, fid)  # gets a feed of the user
                pFeed = ParsedFeed(feed)

                entry = []
                for e in pFeed.entries:
                    if e.id == eid:
                        entry.append(e)
                        break

                return render_to_response('displayfeedentry.html', {'feeds': feeds, 'feed': pFeed, 'entry': entry[0], 'user': loginUser}, context_instance=RequestContext(request))

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

