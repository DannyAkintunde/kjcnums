from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from . import models
from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email'}))

class RegistrationForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username','first_name','last_name','password1','password2','email']



class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class NumForm(forms.ModelForm):
    """Form definition for Num."""
    num = forms.CharField(min_length=11,max_length=11,required=True)
    class Meta:
        """Meta definition for Numform."""
        model = models.Nums
        fields = ('num',)

class OtherlinkForm(forms.ModelForm):
    """Form definition for Otherllink."""

    class Meta:
        """Meta definition for Otherlinkform."""

        model = models.Otherlink
        fields = ('link','display_text')

class SociallinkForm(forms.ModelForm):
    """Form definition for Sociallink."""
    class Meta:
        """Meta definition for Sociallinkform."""

        model = models.Sociallink
        fields = ('link','platform','text')

class NinForm(forms.ModelForm):
    """Form definition for Nin."""
    nin = forms.CharField(max_length=11,min_length=11)
    class Meta:
        """Meta definition for Ninform."""

        model = models.Nin
        fields = ('nin',)

class PrivacyForm(forms.ModelForm):
    """Form definition for Privacy."""

    class Meta:
        """Meta definition for Privacyform."""

        model = models.Ristriction
        fields = ('type','users')





class BasicInfoForm(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model = models.Userdata
        fields = ['gender', 'category']
        widgets = {
            'gender':forms.Select(choices=[('m','Male'),('f','Female')])
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'id': 'fileInput'})

# class ContactInfoForm(forms.ModelForm):
#     """Form definition for ContactInfo."""

#     class Meta:
#         """Meta definition for ContactInfoform."""

#         model = models.Userdata
#         fields = ('nums','sociallinks','otherlinks')

class RecoveryForm (forms.Form):
    nin = forms.CharField(max_length=11,min_length=11,required=True,help_text='Input your nin')