from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from feedreader.reader.database.databaseprovider import DatabaseProvider
from feedreader.reader.feed.form.newfeed.addfeed import AddFeedForm
from feedreader.reader.user.form.login.login import LoginForm
from feedreader.reader.user.form.management.manage import UserManageForm
from feedreader.reader.user.session.sessionhandler import SessionHandler
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

__author__ = 'Roland'


class ManageView(object):
    """
    Class for manage view
    """

    @staticmethod
    def get(request):
        """
        static method for get
        """

        activeFeeds = ''
        activeUser = ''

        if 'pagetab' in request.GET.keys():
                pageTab = request.GET['pagetab']

                if(pageTab == 'user'):
                    activeFeeds = ''
                    activeUser = 'active'
                else:
                    activeFeeds = 'active'
                    activeUser = ''

         # redirect active session
        if SessionHandler.isUserSessionAlive(request.session):
            loginUser = SessionHandler.getSessionUser(request.session)
            formAddFeed = AddFeedForm()
            formManageUser = UserManageForm()

            feeds = DatabaseProvider.getFeedsByUserId(loginUser.id)  # gets the feeds of the user

            return render_to_response('manage.html', {'frmAddFeed': formAddFeed, 'user': loginUser, 'feeds': feeds,
                                      'manage': formManageUser, 'mail': loginUser.email, 'activeFeeds': activeFeeds,
                                      'activeUser': activeUser},
                                      context_instance=RequestContext(request))

        return HttpResponseRedirect('/feedreader/')

    @staticmethod
    def post(request):
        """
        static method for post
        """
        if 'submitNewFeed' in request.POST:

            form = AddFeedForm(request.POST)

            if form.is_valid():
                name = form.cleaned_data['name'].encode('ascii', 'ignore')
                url = form.cleaned_data['url'].encode('ascii', 'ignore')

                validate = URLValidator()
                try:
                    validate(url)
                except ValidationError, e:
                    loginUser = SessionHandler.getSessionUser(request.session)
                    formAddFeed = AddFeedForm()
                    formManageUser = UserManageForm()
                    error = "The feed URL you provided seems to be incorrect!"
                    feeds = DatabaseProvider.getFeedsByUserId(loginUser.id)  # gets the feeds of the user
                    return render_to_response('manage.html', {'frmAddFeed': formAddFeed, 'user': loginUser, 'feeds': feeds,
                                                              'manage': formManageUser, 'mail': loginUser.email, 'errorurl': error},
                                                                context_instance=RequestContext(request))

                loginUser = SessionHandler.getSessionUser(request.session)
                DatabaseProvider.addNewFeed(loginUser.id, name, url)  # adds new newfeed for user

                formAddFeed = AddFeedForm()
                formManageUser = UserManageForm()
                success = "Feed successfully added!"
                feeds = DatabaseProvider.getFeedsByUserId(loginUser.id)  # gets the feeds of the user
                return render_to_response('manage.html', {'frmAddFeed': formAddFeed, 'user': loginUser, 'feeds': feeds,
                                                          'manage': formManageUser, 'mail': loginUser.email, 'success': success},
                                          context_instance=RequestContext(request))

            # invalid form
            else:
                loginUser = SessionHandler.getSessionUser(request.session)
                formAddFeed = AddFeedForm()
                formManageUser = UserManageForm()
                error = "Form is invalid"
                feeds = DatabaseProvider.getFeedsByUserId(loginUser.id)  # gets the feeds of the user
                return render_to_response('manage.html', {'frmAddFeed': formAddFeed, 'user': loginUser, 'feeds': feeds,
                                                          'manage': formManageUser, 'mail': loginUser.email, 'errorurl': error},
                                          context_instance=RequestContext(request))

        elif 'submitDeleteFeed' in request.POST:

            deleteID = request.POST.get('submitDeleteFeed')
            loginUser = SessionHandler.getSessionUser(request.session)
            DatabaseProvider.deleteFeed(loginUser.id, deleteID)

            formAddFeed = AddFeedForm()
            formManageUser = UserManageForm()
            success = "Feed successfully deleted!"
            feeds = DatabaseProvider.getFeedsByUserId(loginUser.id)  # gets the feeds of the user
            return render_to_response('manage.html', {'frmAddFeed': formAddFeed, 'user': loginUser, 'feeds': feeds,
                                                      'manage': formManageUser, 'mail': loginUser.email, 'success': success},
                                      context_instance=RequestContext(request))

        elif 'submitChangePw' in request.POST:
            form = UserManageForm(request.POST)

            if form.is_valid():
                password = form.cleaned_data['password'].encode('ascii', 'ignore')

                user = request.session['active_User']  # get user id from session
                user.set_password(password)
                user.save()

                loginUser = SessionHandler.getSessionUser(request.session)
                formAddFeed = AddFeedForm()
                formManageUser = UserManageForm()
                success = "Password successfully changed!"
                feeds = DatabaseProvider.getFeedsByUserId(loginUser.id)  # gets the feeds of the user
                return render_to_response('manage.html', {'frmAddFeed': formAddFeed, 'user': loginUser, 'feeds': feeds,
                                                          'manage': formManageUser, 'mail': loginUser.email, 'success': success},
                                          context_instance=RequestContext(request))

            # invalid form
            else:
                loginUser = SessionHandler.getSessionUser(request.session)
                formAddFeed = AddFeedForm()
                formManageUser = UserManageForm()
                error = "Invalid password (Min. 8 Characters)!"
                feeds = DatabaseProvider.getFeedsByUserId(loginUser.id)  # gets the feeds of the user
                return render_to_response('manage.html', {'frmAddFeed': formAddFeed, 'user': loginUser, 'feeds': feeds,
                                          'manage': formManageUser, 'mail': loginUser.email, 'errorpw': error},
                                          context_instance=RequestContext(request))

        elif 'submitSearch' in request.POST:
            searchValue = request.POST['submitSearch']
            values = searchValue.replace(' ', '+')

            return HttpResponseRedirect('/feedreader/search/?keywords=' + values)

        return HttpResponseRedirect('/feedreader/manage')

