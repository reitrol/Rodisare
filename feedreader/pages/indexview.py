from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from feedreader.reader.database.databaseprovider import DatabaseProvider
from feedreader.reader.user.form.login.login import LoginForm
from feedreader.reader.user.session.authentication import Authentification
from feedreader.reader.user.session.sessionhandler import SessionHandler
from feedreader.reader.feed.ParsedFeed import ParsedFeed

__author__ = 'Roland'


class IndexView(object):
    """
    Class for index view
    """

    @staticmethod
    def get(request):
        """
        static method for get
        """

        # redirect active session
        if SessionHandler.isUserSessionAlive(request.session):
            loginUser = SessionHandler.getSessionUser(request.session)

            feeds = DatabaseProvider.getFeedsByUserId(loginUser.id)  # gets the feeds of the user
            frmLogin = LoginForm()

            parsedFeedEntries = []
            for feed in feeds:
                #parsedFeeds.append(ParsedFeed(feed))
                pf = ParsedFeed(feed)
                for entry in pf.entries:
                    parsedFeedEntries.append(entry)

            tmp = sorted(parsedFeedEntries, cmp=IndexView.sortFeedEntries, reverse=True)
            parsedFeedEntriesSorted = []
            for i in range(0,len(tmp)):
                parsedFeedEntriesSorted.append(tmp[i])

            return render_to_response('index.html', {'login': frmLogin, 'user': loginUser, 'feeds': feeds, 'parsedFeedEntries': parsedFeedEntriesSorted},
                                      context_instance=RequestContext(request))

        else:
            # displays new login form
            frmLogin = LoginForm()
            return render_to_response('index.html', {'login': frmLogin, 'user': 'Anonymous'},
                                      context_instance=RequestContext(request))


    @staticmethod
    def post(request):
        """
        static method for post
        """

        if 'submitLogin' in request.POST:

            form = LoginForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username'].encode('ascii', 'ignore')
                password = form.cleaned_data['password'].encode('ascii', 'ignore')

                user = Authentification.isValidUser(username, password)

                # checks if user exists
                if user is not None:
                    request.session['active_User'] = user

                    # sets the session expiration in seconds
                    request.session.set_expiry(60*60*24*7)  # sets session to 7 days

                    return HttpResponseRedirect('/feedreader/')

                # user does not exists
                else:
                    #return HttpResponseRedirect('/feedreader/')
                    frmLogin = LoginForm()
                    error = "Incorrect username or password"
                    return render_to_response('index.html', {'login': frmLogin, 'user': 'Anonymous', 'error': error},
                                          context_instance=RequestContext(request))

            # invalid form
            else:
                frmLogin = LoginForm()
                error = "You have entered invalid data. Please try again."
                return render_to_response('index.html', {'login': frmLogin, 'user': 'Anonymous', 'error': error},
                                          context_instance=RequestContext(request))

        elif 'submitSearch' in request.POST:
            searchValue = request.POST['submitSearch']
            values = searchValue.replace(' ', '+')

            return HttpResponseRedirect('/feedreader/search/?keywords=' + values)

        else:
            return HttpResponseRedirect('/feedreader/')



    @staticmethod
    def sortFeedEntries(entry1, entry2):
        t1 = entry1.published_parsed
        t2 = entry2.published_parsed
        str1 = ''
        str1 += '%(y)02d' % {'y': t1.tm_year}
        str1 += '%(y)02d' % {'y': t1.tm_mon}
        str1 += '%(y)02d' % {'y': t1.tm_mday}
        str1 += '%(y)02d' % {'y': t1.tm_hour}
        str1 += '%(y)02d' % {'y': t1.tm_min}
        str1 += '%(y)02d' % {'y': t1.tm_sec}
        str2 = ''
        str2 += '%(y)02d' % {'y': t2.tm_year}
        str2 += '%(y)02d' % {'y': t2.tm_mon}
        str2 += '%(y)02d' % {'y': t2.tm_mday}
        str2 += '%(y)02d' % {'y': t2.tm_hour}
        str2 += '%(y)02d' % {'y': t2.tm_min}
        str2 += '%(y)02d' % {'y': t2.tm_sec}
        return cmp(str1, str2)
