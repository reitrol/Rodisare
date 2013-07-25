__author__ = 'Roland Reitboeck'
from django import forms

from feedreader.reader.user.form.registration.username import UserNameField
from feedreader.reader.user.form.registration.password import PasswordField
from feedreader.reader.user.form.registration.mail import MailField
from feedreader.reader.user.form.registration.firstname import FirstNameField
from feedreader.reader.user.form.registration.lastname import LastNameField


class RegistrationForm(forms.Form):
    """
    Form for user registration
    """
    #lastName = LastNameField(max_length=100, required=True, min_length=1)
    #firstName = FirstNameField(max_length=100, required=True, min_length=1)
    username = UserNameField(max_length=100, required=True, min_length=1)
    email = MailField(max_length=100, required=True)
    password = PasswordField(max_length=32, min_length=8, required=True) #, widget=forms.PasswordInput)