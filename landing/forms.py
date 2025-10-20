from django import forms
from .models import Contestant

class ContestantForm(forms.ModelForm):
    class Meta:
        model = Contestant
        fields = ['name_or_group_name', 'email', 'talent_description', 'is_group', 'group_size', 'video_submission']

from django import forms

class PartnerContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)   