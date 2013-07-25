__author__ = 'Roland Reitboeck'
from django import forms

from feedreader.reader.user.form.login.username import UserNameField
from feedreader.reader.user.form.login.password import PasswordField


class LoginForm(forms.Form):
    """
    Form for user login
    """
    username = UserNameField(max_length=100, initial='webmaster', required=True)
    password = PasswordField(max_length=32, initial='pythonHSA', required=True) #, widget=forms.PasswordInput)



