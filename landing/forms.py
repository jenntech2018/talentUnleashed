from django import forms
from .models import Contestant

class ContestantForm(forms.ModelForm):
    class Meta:
        model = Contestant
        fields = ['name_or_group_name', 'email', 'talent_description', 'is_group', 'group_size', 'video_submission']

from django import forms

# forms.py
from django import forms
from .models import PartnerInquiry

class PartnerContactForm(forms.ModelForm):
    class Meta:
        model = PartnerInquiry
        fields = ['name', 'email', 'message']