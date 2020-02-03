from django import forms
from django.contrib.auth.forms import UserCreationForm
from members.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'name', 'designation', 'password1', 'password2')


class ActivateForm(forms.Form):
    member = forms.ModelChoiceField(queryset=User.objects.filter(is_active=False), empty_label='Select from below')
