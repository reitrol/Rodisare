__author__ = 'Roland Reitboeck'
from django import forms


class FirstNameField(forms.CharField):

    widget = forms.TextInput(attrs={'placeholder': 'E.g. Roland'})

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
        super(FirstNameField, self).validate(value)