from django.forms import ModelForm

from bulletins.models import Bulletin

class BulletinForm(ModelForm):
    class Meta:
        model = Bulletin
        exclude = ('Author', 'Items')