from django.contrib.auth.models import User
from .models import RecipeD, Comment, Ingredient
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

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['body']

class HomeForm(forms.ModelForm):
    class Meta:
        model = RecipeD
        fields = ['post', 'Name', 'Cuisine', 'RecipeProcedure', 'RecipePicture']
        
class IngredientForm(forms.ModelForm):
	class Meta:
		model = Ingredient
		fields = ['ingredientName']

class IForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['ingredientName']