__author__ = 'Roland Reitboeck'
from django import forms


class PasswordField(forms.CharField):

    widget = forms.TextInput(attrs={'placeholder': 'Min. 8 Characters'})

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
        super(PasswordField, self).validate(value)