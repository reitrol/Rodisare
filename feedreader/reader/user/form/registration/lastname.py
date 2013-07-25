__author__ = 'Roland Reitboeck'
from django import forms


class LastNameField(forms.CharField):

    widget = forms.TextInput(attrs={'placeholder': 'E.g. Reitboeck'})

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
        super(LastNameField, self).validate(value)