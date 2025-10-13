from django import forms
from .models import Contestant

class ContestantForm(forms.ModelForm):
    class Meta:
        model = Contestant
        fields = ['name/group', 'email', 'talent_description']