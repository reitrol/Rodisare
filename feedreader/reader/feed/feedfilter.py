from feedreader.reader.feed.ParsedFeed import ParsedFeed

__author__ = 'Roland Reitboeck'


class SearchFeed(object):
    """
    Class to search feeds by keywords
    """

    def __init__(self, feeds, keywords):
        self.feeds = feeds
        self.keywords = keywords

    def getFilteredFeeds(self):
        """
        static method to get filtered feeds
        """

        feedEntries = []  # list of all feed entries for one user

        for feed in self.feeds:
            feedEntries += ParsedFeed(feed).entries  # gets feed entries of each feed

        return self.filterFeedEntries(feedEntries)

    def filterFeedEntries(self, feedEntries):
        """
        filters the feed entries
        """
        filtered = []

        for entry in feedEntries:
            entryText = entry.title.lower() + " " + entry.summary.lower()

            # if entryText contains all keys
            if all(key in entryText for key in self.keywords.lower().split(' ')):
                filtered.append(entry)

        return filtered





