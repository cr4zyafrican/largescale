from django.conf.urls import url
from . import views
app_name= 'recipe'

urlpatterns = [
    url(r'^$', views.index, name='index'), 

    #/recipe/id/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),   
    #/recipe/recipeD/add/
    url(r'recipeD/add/$', views.RecipeCreate.as_view(), name='recipe-add'),

    url(r'reciped/(?P<pk>[0-9]+)/update$', views.RecipeUpdate.as_view(), name='recipe-update'),

    url(r'reciped/(?P<pk>[0-9]+)/delete$', views.RecipeDelete.as_view(), name='recipe-delete'),

]
