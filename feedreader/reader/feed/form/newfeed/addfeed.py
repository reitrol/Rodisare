__author__ = 'Roland Reitboeck'
from django import forms

from feedreader.reader.feed.form.newfeed.name import FeedNameField
from feedreader.reader.feed.form.newfeed.url import FeedUrl


class AddFeedForm(forms.Form):
    """
    Form for user login
    """
    name = FeedNameField(max_length=20, required=True)
    url = FeedUrl(max_length=500, required=True)



