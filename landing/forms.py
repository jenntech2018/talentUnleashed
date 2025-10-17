from django import forms
from .models import Contestant

class ContestantForm(forms.ModelForm):
    class Meta:
        model = Contestant
        fields = ['name_or_group_name', 'email', 'talent_description', 'is_group', 'group_size']
