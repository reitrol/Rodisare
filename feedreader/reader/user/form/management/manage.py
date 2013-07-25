__author__ = 'Roland Reitboeck'
from django import forms

from feedreader.reader.user.form.management.password import PasswordField


class UserManageForm(forms.Form):
    """
    Form for user login
    """
    password = PasswordField(max_length=32, required=True, min_length=8) #, widget=forms.PasswordInput)



