__author__ = 'Roland'


from feedreader.models import Feed


class DatabaseProvider(object):
    """
    Class for Database interactions
    """

    @staticmethod
    def getFeedsByUserId(pUserId):
        feeds = Feed.objects.filter(userId=int(pUserId))
        return feeds

    @staticmethod
    def getFeedByUserIdAndFeedId(pUserId, pFeedId):
        feed = Feed.objects.filter(userId=int(pUserId), id=int(pFeedId))
        return feed[0]

    @staticmethod
    def addNewFeed(uId, pFeedName, pFeedUrl):
        newFeed = Feed(userId=uId, name=pFeedName, url=pFeedUrl)
        newFeed.save()

    @staticmethod
    def deleteFeed(uId, feedId):
        Feed.objects.filter(id=int(feedId), userId=int(uId)).delete()