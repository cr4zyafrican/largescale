from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class RecipeD(models.Model):
	recipelName = models.CharField(max_length=250)
	cuisine = models.CharField(max_length=250)
	recipeProcedure = models.CharField(max_length = 1000000)
	is_favorite = models.BooleanField(default=False)
	recipePiture = models.CharField(max_length=100000, default="")
	def get_absolute_url(self):
		return reverse('recipe:index')

	def __str__(self):
		return self.recipelName +"\n"+"Procedure: "+self.recipeProcedure


#many to many relationship
class Ingredient(models.Model):
	ingredientName = models.CharField(max_length=250)
	ingredientPicture = models.CharField(max_length=1000)

class ingredientList(models.Model):
	amount = models.IntegerField()
	recipe = models.ForeignKey(RecipeD, on_delete=models.CASCADE, blank=False, null=False)
	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, blank=False, null=False)

