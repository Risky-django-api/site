from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=50,
        help_text=('Letters, digits and @/./+/-/_ only.'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(max_length=50, help_text='Inform a valid email address.',
                             widget=(forms.TextInput(attrs={'class': 'form-control'})))
    password1 = forms.CharField(label = 'Password', widget=(forms.PasswordInput(attrs={'class': 'form-control'})))
    password2 = forms.CharField(label = 'Repeat password',widget=(forms.PasswordInput(attrs={'class': 'form-control'})))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

class CustomLoginForm(AuthenticationForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update(
      {'class': 'form-control'}
    )
    self.fields['password'].widget.attrs.update(
      {'class': 'form-control'}
    )