from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from .models import User

_INPUT = {"class": "form-input"}


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(_INPUT | {"autofocus": True})
        self.fields["password"].widget.attrs.update(_INPUT)


class StyledPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(_INPUT)


class AdminAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-input"
            if name in ("first_name", "last_name", "email"):
                field.required = True
