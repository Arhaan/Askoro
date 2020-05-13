from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
class UserRegisterForm(UserCreationForm):
    email=forms.EmailField(max_length='256')
    def __init__(self, *args, **kwargs):
        self.helper=FormHelper()
        self.helper.help_text_inline = True
        super().__init__(*args, **kwargs)
    class Meta:
        model=User
        fields = ['username', 'email', 'password1', 'password2']
