__author__ = 'Roland Reitboeck'
from django.contrib.auth import authenticate
import datetime
import time


class SessionHandler():
    """
    SessionHandler for easy handling with active sessions
    """

    @staticmethod
    def isUserSessionAlive(session):

        if session.get('active_User') is not None:

            expiryDate = session.get_expiry_date()
            dateNow = datetime.datetime.now()
            timeSpanSeconds = time.mktime(expiryDate.timetuple()) - time.mktime(dateNow.timetuple())

            # session refresh, if session < 15 minutes
            if timeSpanSeconds < 60*15:
                session.set_expiry(60*60*24*7)  # sets session to 7 days

            return True
        else:
            return False


    @staticmethod
    def getSessionUser(session):
        try:
            return session['active_User']
        except Exception, e:
            return None

