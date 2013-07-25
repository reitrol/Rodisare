__author__ = 'Roland Reitboeck'
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class Authentification(object):
    """
    Authentification class for simple auth. with Djang admin
    """

    @staticmethod
    def isValidUser(user, password):
        """
        Checks, if user and password are correct
        """
        user = authenticate(username=user, password=password)

        if user is not None:
            if user.is_active:
                return user

        return None

    @staticmethod
    def userExists(username):
        """
        Checks for registration if users already exists
        """
        if User.objects.filter(username=username).count() > 0:
            return True
        else:
            return False

