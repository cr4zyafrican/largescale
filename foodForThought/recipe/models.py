from django.db import models
from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse
from django.conf import settings

# Create your models here.
class RecipeD(models.Model):
	user = models.ForeignKey(User, default=1)
	Name = models.CharField(max_length=250)
	post = models.CharField(max_length = 10000000, default="")
	Cuisine = models.CharField(max_length=250)
	created = models.DateTimeField(auto_now_add=True, blank=False, null=True)
	RecipeProcedure = models.CharField(max_length = 1000000)
	RecipePicture = models.FileField(default="")


	def get_absolute_url(self):
		return reverse('recipe:index')

	def __str__(self):
		return self.Name +"\n"+"Procedure: "+self.RecipeProcedure

class Comment(models.Model):
	RecipeD = models.ForeignKey(RecipeD, related_name="comments")
	user = models.ForeignKey(User, default=1)
	created = models.DateTimeField(auto_now_add=True)
	body = models.TextField()
#many to many relationship
class Ingredient(models.Model):
	ingredientName = models.CharField(max_length = 1000000)

class ingredientList(models.Model):
	amount = models.IntegerField()
	recipe = models.ForeignKey(RecipeD, on_delete=models.CASCADE, blank=False, null=False)
	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, blank=False, null=False)

class Friend(models.Model):
	users = models.ManyToManyField(User)
	current_user = models.ForeignKey(User, related_name='owner', null=False)
	@classmethod
	def make_friend(cls, current_user, new_friend):
		friend, created = cls.objects.get_or_create(
			current_user=current_user

			)
		friend.users.add(new_friend)
	@classmethod
	def lose_friend(cls, current_user, new_friend):
		friend,created = cls.objects.get_or_create(
			current_user=current_user)
		friend.users.remove(new_friend)
