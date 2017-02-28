from django.forms import ModelForm
from .models import *

class CafeForm(ModelForm):
    class Meta:
        model = Cafe
        fields = '__all__'

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = '__all__'

class DeleteCafeForm(ModelForm):
	class Meta:
		model = Cafe
        fields = []

class DeleteCommentForm(ModelForm):
	class Meta:
		model = Comment
        fields = []

