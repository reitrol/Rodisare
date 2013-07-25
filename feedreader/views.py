import HTMLParser
from django.shortcuts import render_to_response, render
from django.core.context_processors import csrf
from django.template import RequestContext

from django.contrib.auth import logout
from feedreader.pages.searchview import SearchFeedView

from feedreader.reader.feed.ParsedFeed import ParsedFeed

from feedreader.pages.manageview import ManageView
from feedreader.pages.registerview import RegisterView
from feedreader.pages.indexview import IndexView
from feedreader.pages.displayfeedview import DisplayFeedView
from feedreader.pages.displayfeedinfoview import DisplayFeedInfoView
from feedreader.pages.displayfeedentryview import DisplayFeedEntryView

def index(request):
    """
    Request for app index page
    """
    c = {}
    c.update(csrf(request))  # Cross Site Request Forgery protection

    if request.method == 'GET':
        return IndexView.get(request)
    elif request.method == 'POST':
        return IndexView.post(request)


def register(request):
    """
    Request for app registration page
    """
    c = {}
    c.update(csrf(request))  # Cross Site Request Forgery protection

    if request.method == 'GET':
        return RegisterView.get(request)
    elif request.method == 'POST':
        return RegisterView.post(request)


def logoutUser(request):
    """
    Request for logout page
    """
    logout(request)
    return render_to_response('logout.html', context_instance=RequestContext(request))


def manage(request):
    """
    Request for manage page to organize feeds
    """
    c = {}
    c.update(csrf(request))  # Cross Site Request Forgery protection

    if request.method == 'GET':
        return ManageView.get(request)
    elif request.method == 'POST':
        return ManageView.post(request)

def displayfeed(request):
    """
    Request for displayfeed page to display feeds or single feed entries
    """
    c = {}
    c.update(csrf(request))  # Cross Site Request Forgery protection

    if request.method == 'GET':
        return DisplayFeedView.get(request)
    elif request.method == 'POST':
        return DisplayFeedView.post(request)

def displayfeedinfo(request):
    """
    Request for displayfeed info page to display feed information
    """
    c = {}
    c.update(csrf(request))  # Cross Site Request Forgery protection

    if request.method == 'GET':
        return DisplayFeedInfoView.get(request)
    elif request.method == 'POST':
        return DisplayFeedInfoView.post(request)


def displayfeedentry(request):
    """
    Request for a feed a single feed entry
    """
    c = {}
    c.update(csrf(request))  # Cross Site Request Forgery protection

    if request.method == 'GET':
        return DisplayFeedEntryView.get(request)
    elif request.method == 'POST':
        return DisplayFeedEntryView.post(request)


def search(request):
    """
    Request for search page to display specific feeds
    """
    c = {}
    c.update(csrf(request))  # Cross Site Request Forgery protection

    if request.method == 'GET':
        return SearchFeedView.get(request)
    elif request.method == 'POST':
        return SearchFeedView.post(request)