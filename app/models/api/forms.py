from django.forms import ModelForm
from .models import *

class CafeForm(ModelForm):
    class Meta:
        model = Cafe
        fields = '__all__'