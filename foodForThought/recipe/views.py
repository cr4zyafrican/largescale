from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.views import generic 
from django.template import loader
from django.contrib.auth import logout
from django.views.generic import TemplateView
from .models import RecipeD, Friend
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm, RecipeForm, HomeForm
from django.contrib.auth.models import User
from django.db.models import Q

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
		args = {'form':form, 'post':post, 'text':text}
		return render(request, self.template_name, args)
