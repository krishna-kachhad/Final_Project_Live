from django import forms
from .models import *

class signupForm(forms.ModelForm):
    class Meta:
        model=signupdata
        fields='__all__'

class notesForm(forms.ModelForm):
    class Meta:
        model=mynotes
        fields='__all__'

class contactusForm(forms.ModelForm):
    class Meta:
        model=contactus
        fields='__all__'