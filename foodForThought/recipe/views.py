from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.views import generic 
from django.template import loader
from .models import RecipeD
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.
#takes a request and returns a http response.
def index(request):
	all_recipes = RecipeD.objects.all()
	context = {
		'all_recipes':all_recipes,
	}
	template = loader.get_template('recipe/index.html')
	return render(request, 'recipe/index.html', context)

class DetailView(generic.DetailView):
	model = RecipeD
	template_name = 'recipe/detail.html'
class RecipeCreate(CreateView):
	model = RecipeD
	fields = ['recipelName', 'cuisine', 'recipeProcedure', 'recipePiture']

class RecipeUpdate(UpdateView):
	model = RecipeD
	fields = ['recipelName', 'cuisine', 'recipeProcedure', 'recipePiture']

class RecipeDelete(DeleteView):
	model = RecipeD
	success_url = reverse_lazy("recipe:index")