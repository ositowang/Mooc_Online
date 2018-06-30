__author__ = 'osito_wang'
__date__ = '2018/6/24 16:16'
import re
from django import forms

from operation.models import UserQuestion


class UserQuestionForm(forms.ModelForm):
    class Meta:
        model = UserQuestion
        fields = ["name", "mobile", "course_name"]

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        pattern = re.compile("(\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\d{3}[-\.\s]\d{4})")
        if pattern.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("The phone number is not valid", code="invalid_phone_number")

