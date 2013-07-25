__author__ = 'Roland Reitboeck'
from django import forms


class MailField(forms.EmailField):

    widget = forms.TextInput(attrs={'placeholder': 'E.g. reitrol@gmail.com'})

    def to_python(self, value):
        """
        Normalize to string
        """
        return value

    def validate(self, value):
        """
        Check if value consists only of valid emails.
        """
        # Use the parent's handling of required fields, etc.
        super(MailField, self).validate(value)