from django import forms

from .models import Upload

class UploadForm(forms.ModelForm):
    """the form for upload files"""
    class Meta:
        model = Upload
        fields = ['userfiles','uploadName','firstDay','forecastperiod','forecastmethod']
        labels = {'text': 'upload *.csv file'}

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)

# class UploadForm(forms.Form):
#     """ the form for uploading files"""
#     FORECASTPERIOD = (
#         ('s', 'short term'),
#         ('m', 'medium term'),
#         ('l', 'long term'),
#     )
#     FORECASTMETHOD = (
#         ('ann', 'neural network'),
#         ('svm', 'support vector machine'),
#         ('mps', 'multiple proportion smoothing method')
#     )
#     uploadName = forms.CharField(max_length=100)
#     file = forms.FileField(upload_to=user_directory_path)
#     forecastperiod = forms.CharField("Forecasting period", max_length=1, \
#                                       choices=FORECASTPERIOD, blank=False,
#                                       default='m')
#     forecastmethod = forms.CharField("Forecasting method", max_length=3, \
#                                       choices=FORECASTMETHOD, blank=False,
#                                       default='ann')


