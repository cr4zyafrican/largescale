from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.views import generic 
from django.template import loader
from django.contrib.auth import logout
from django.views.generic import TemplateView
from .models import RecipeD, Friend, Ingredient
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.views.generic import View
from .forms import UserForm, RecipeForm, HomeForm, CommentForm, IngredientForm, IForm
from django.contrib.auth.models import User
from django.db.models import Q
from .functions import getRecipe

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


# Create your views here.
#takes a request and returns a http response.
def index(request):
	if not request.user.is_authenticated:
		return render(request, 'recipe/login.html')
	else:
		all_recipes = RecipeD.objects.filter(user=request.user)
		user = request.user
		query = request.GET.get("q")
		if query:
			all_recipes = all_recipes.filter(Q(Name__icontains=query)).distinct()
			return render(request, 'recipe/index.html', {'all_recipes':all_recipes, 'user':user})
		else:
			return render(request, 'recipe/index.html', {'all_recipes':all_recipes, 'user':user}) 

def RecipeCreate(request):
	form = RecipeForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		recipe = form.save(commit=False)
		recipe.user = request.user
		recipe.save()
		return render(request, 'recipe/detail.html', {'reciped':recipe})
	else:
		return render(request, 'recipe/reciped_form.html', {'form':form})

class DetailView(generic.DetailView):
	model = RecipeD
	template_name = 'recipe/detail.html'


class RecipeUpdate(UpdateView):
	model = RecipeD
	fields = ['Name', 'Cuisine', 'RecipeProcedure', 'RecipePicture']

class RecipeDelete(DeleteView):
	model = RecipeD
	success_url = reverse_lazy("recipe:index")

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'recipe/login.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                recipe = RecipeD.objects.filter(user=request.user)
                return render(request, 'recipe/index.html', {'recipe': recipe})
            else:
                return render(request, 'recipe/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'recipe/login.html', {'error_message': 'Invalid login'})
    return render(request, 'recipe/login.html')

class UserFormView(View):
	form_class= UserForm
	template_name = 'recipe/registration_form.html'
	#display a blank form
	def get(self, request):
		form= self.form_class(None)
		return render(request, self.template_name, {'form':form})
	#process form data

	def post(self, request):
		form= self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			#cleaned (normalized) data
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()
			user = authenticate(username=username, password=password)

			if user is not None:
				if  user.is_active:
					login(request,user)
					return redirect('recipe:index')
		return render(request, self.template_name, {'form':form})


def change_friends(request, operation, pk):
	friend = User.objects.get(pk=pk)
	if operation =='add':
		Friend.make_friend(request.user, friend)
	elif operation =='remove':
		Friend.lose_friend(request.user, friend)
	return redirect('recipe:home')

class ProfileView(generic.DetailView):
	User = get_user_model()
	template_name = 'recipe/user.html'
	def get_object(self):
		username = self.kwargs.get("username")
		if username is None:
			raise Http404
		return get_object_or_404(User, username__iexact=username, is_active=True)
 
def add_comment(request, pk):
 	post = get_object_or_404(RecipeD, pk=pk)
 	form = CommentForm(request.POST or None)
 	user = request.user
 	if request.method == 'POST':
 		form = CommentForm(request.POST or None)
 		if form.is_valid():
 			comment = form.save(commit=False)
 			comment.RecipeD = post
 			comment.user = request.user
 			form = CommentForm(request.POST or None)
 			comment.save()
 			return redirect('recipe:home')
 	else:
 		form = CommentForm()
 	template = 'recipe/add_comment.html'
 	context = {'form':form, 'user':user}
 	return render(request, template, context)

class search(TemplateView):
	template_name = 'recipe/search.html'
	names = getRecipe("apples")
	def post(self, request):
		form = IForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			ingredientList = form.save(commit=False)
			ingredientList.save()
			form = IForm(request.POST or None)
			return redirect('recipe:search')
		return render(request, 'recipe/index.html')
	def get(self, request):
		form = IForm()
		if(Ingredient.objects.count()==0):
			names = getRecipe("apples")
			return render(request, 'recipe/search.html', {'title':names})
		i = Ingredient.objects.all()[Ingredient.objects.count()]
		name = i.ingredientName
		names = getRecipe(i)
		return render(request, 'recipe/search.html', {'title':names})


class HomeView(TemplateView):
	template_name = 'recipe/home.html'
	def get(self, request):
		form = HomeForm()

		posts = RecipeD.objects.all().order_by('-created')
		users = User.objects.exclude(id=request.user.id)
		user = request.user
		try:
			friend = Friend.objects.get(current_user=request.user)
			friends = friend.users.all()
		except:
			friend = None
			friends = None

		args={'form': form, 'posts':posts, 'users':users, 'friends':friends,'user':user}
		return render(request, self.template_name, args)
	def post(self, request):
		form = HomeForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			post = form.save(commit=False)
			post.user= request.user
			post.save()
			form = HomeForm(request.POST or None, request.FILES or None)
			return redirect('recipe:home')
		args = {'form':form, 'post':post}
		return render(request, self.template_name, args)
 
