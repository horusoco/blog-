from django import forms 
from tinymce import TinyMCE 
from . models import Post, Comment











class TinyMCEWidget(TinyMCE):
	def use_required_attribute(self, *args):
		return False 


class PostForm(forms.ModelForm):
	content = forms.CharField(
		widget=TinyMCEWidget(
		attrs={'required': False, 'cols': 30, 'rows': 10}
		)
	)


class CommentForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={
	'placeholder': 'Type your email address',
	'class':'form-control'}))
	class Meta:
		model = Comment
		fields = ('content',)

		