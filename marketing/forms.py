from django import forms 
from . models import Signup 



class SignupForm(forms.ModelForm):
	email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type your email address'}), label='')
	class Meta:
		model = Signup
		fields = ('email',)





   