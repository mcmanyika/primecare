from django import forms
from django.core.files.images import get_image_dimensions
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from joins.models import UserProfile
from django import *
from django.contrib.auth import authenticate, get_user_model, login, logout

from .models import *
User = get_user_model()


class AvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'tracker',
            'rootid',
            'gender',
            'phone',
        ]


class AcctForm(forms.ModelForm):
    class Meta:
        model = t_acct
        fields = [
            'rootid',
            'gender',
            'phone',
            'account_type',
            'status',
            'user',
        ]


class EditAcctForm(forms.ModelForm):
    class Meta:
        model = t_acct
        fields = [
            'rootid',
            'gender',
            'phone',
            'address',
            'emergency_contact',
            'account_type',
            'status',
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = t_acct
        fields = ["rootid",  "gender", "phone", "address",
                  "emergency_contact", "account_type", "status", "user"]


class UserForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'rootid',
            'gender',
            'avatar',
        ]


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
        ]

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Emails must match")

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(
                "This email has already been registered")
        return email


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'Username'}), label='')

    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'First Name'}), label='')
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'Last Name'}), label='')
    email = forms.EmailField(max_length=254, required=False,  widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'Email'}), label='')
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'Password'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'Repeat Password'}), label='')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', )
