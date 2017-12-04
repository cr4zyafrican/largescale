import json
import requests
from .models import RecipeD


def getRecipe(i):
	params = {
		'fillIngredients': False,
		'ingredients': i,
		'limitLicense': False,
		'number': 5,
		'ranking': 1
	}

	endpoint = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients"


	headers={
	    "X-Mashape-Key": "VW4AuGjtoEmshFNJeRjEnTKXIzNZp1NnQXtjsnkzXIXgTBsqeF",
    	"X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"
	}

	response = requests.get(endpoint, params=params, headers=headers).json()[0],
	
	info = response[0]['title'] + "\n"+response[0]['image']
	return info
  	



