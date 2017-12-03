import json
import requests
from .models import RecipeD


def getRecipe():
	payload = {
		'ingredients': "apples",
	}
	api_key = os.environ['api_key']

	endpoint = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients"


	response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?fillIngredients=false&ingredients=apples%2C+oranges&limitLicense=false&number=5&ranking=1",
	  headers={
	    "X-Mashape-Key": "VW4AuGjtoEmshFNJeRjEnTKXIzNZp1NnQXtjsnkzXIXgTBsqeF",
	    "X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"
	  }
	)
  	data = response.json()
  	



