from web import models
from django import forms

from web import models
from web.forms.bootstrap import BootStrapForm


class PreferenceForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Preference
        fields = [
            'student_id',
            'major',
            'dorm_area',
            'preferred_building',
            'preferred_subject',
            'preferred_topic',
            'additional_preferences',
        ]

