from django import forms
from .models import Contestant

class ContestantForm(forms.ModelForm):
    class Meta:
        model = Contestant
        fields = ['name', 'email', 'talent_description']