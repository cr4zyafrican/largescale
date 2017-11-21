from django.contrib.auth.models import User
from .models import RecipeD
from django import forms

class RecipeForm(forms.ModelForm):
	class Meta:
		model = RecipeD
		fields = ['Name', 'Cuisine', 'RecipeProcedure', 'RecipePicture']

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ['username','email', 'password']

class HomeForm(forms.ModelForm):
    class Meta:
        model = RecipeD
        fields = ['post', 'Name', 'Cuisine', 'RecipeProcedure', 'RecipePicture']