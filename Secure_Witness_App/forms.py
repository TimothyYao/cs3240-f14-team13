from django import forms
from models import Bulletin



#unused for now . . .
class BulletinForm(forms.ModelForm):
    class Meta:
        model = Bulletin





class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
