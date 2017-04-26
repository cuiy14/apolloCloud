from django import forms

from .models import Upload

class UploadForm(forms.ModelForm):
    """the form for upload files"""
    class Meta:
        model = Upload
        fields = ['userfiles','forecastperiod','forecastmethod']
        labels = {'text': 'upload *.csv file'}
