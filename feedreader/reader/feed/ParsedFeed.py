__author__ = 'Dietmar'

import HTMLParser
from feedreader.reader.feed.ParsedFeedEntry import ParsedFeedEntry
from feedparser.feedparser import feedparser


class ParsedFeed():

    def __init__(self, feed):
        self.name = feed.name
        self.id = feed.id
        self.url = feed.url

        dFeedParserDict = feedparser.parse( feed.url )
        if 'bozo_exception' in dFeedParserDict.keys():
            self.error = 'something went wrong while reading this feed... mumble mumble'
            return

        # website title
        # format: string
        self.title      = dFeedParserDict.feed.title

        # website link
        # format: string
        self.link       = dFeedParserDict.feed.link

        # website subtitle
        # format: string
        self.subtitle   = dFeedParserDict.feed.subtitle

        # number of feed entries
        # format: string
        self.number     = len(dFeedParserDict.entries)

        # feed version. e.g. rss20
        # format: string
        self.version    = dFeedParserDict.version

        # headers
        # format: {content-length, content-encoding, vary, server, last-modified, connection, date, content-type, x-pingback}
        self.headers    = dFeedParserDict.headers
        self.entries    = []

        # feed entries
        for entry in dFeedParserDict.entries:
            e = ParsedFeedEntry(self, entry)
            self.entries.append(e)

        #print dFeedParserDict.entries

    def __str__(self):
        return 'id: ' + str(self.id) + ', name: ' + self.name + ', url: ' + self.url + ', number of entries: ' + str(len(self.entries))