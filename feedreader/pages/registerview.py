from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
from feedreader.reader.user.form.registration.registration import RegistrationForm
from feedreader.reader.user.session.authentication import Authentification

__author__ = 'Roland'


class RegisterView(object):
    """
    Class for register view
    """

    @staticmethod
    def get(request):
        """
        static method for get
        """

        # displays new registration form
        frmRegistration = RegistrationForm()
        return render_to_response('register.html', {'registration': frmRegistration},
                                  context_instance=RequestContext(request))

    @staticmethod
    def post(request):
        """
        static method for post
        """

        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username'].encode('ascii', 'ignore')
            password = form.cleaned_data['password'].encode('ascii', 'ignore')
            email = form.cleaned_data['email'].encode('ascii', 'ignore')

            if Authentification.userExists(username):
                errorMessage = "Username already exists. Please correct these fields and resubmit the form."
                error = "<div class='alert alert-error'><strong>%s</strong></div>" % errorMessage
                error = mark_safe(error)
                return render_to_response('register.html', {'registration': form, 'error': error},
                                          context_instance=RequestContext(request))

            user = User.objects.create_user(username, email, password)

            # checks if user exists
            if user is not None:
                request.session['active_User'] = user

                # sets the session expiration in seconds
                request.session.set_expiry(600)
                return HttpResponseRedirect('/feedreader/')

        else:
            errorMessage = "One or more required fields were not filled in correctly. " \
                        "Please correct these fields and resubmit the form."

            error = "<div class='alert alert-error'><strong>%s</strong></div>" % errorMessage
            error = mark_safe(error)
            return render_to_response('register.html', {'registration': form, 'error': error},
                                      context_instance=RequestContext(request))