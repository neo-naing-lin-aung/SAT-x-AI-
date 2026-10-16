from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import PasswordChangeForm

class EditUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            }


class CustomPasswordChangeForm(PasswordChangeForm):
    pass 

