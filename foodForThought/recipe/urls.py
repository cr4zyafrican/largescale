from django.conf.urls import url
from . import views
app_name= 'recipe'

urlpatterns = [
    url(r'^$', views.index, name='index'), 
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)$', views.change_friends, name='change_friends'),
    url(r'^home/$', views.HomeView.as_view(), name='home'),  
    url(r'^login_user/$', views.login_user, name='login_user'),

    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    url(r'^register/$', views.UserFormView.as_view(), name='register'), 

    #/recipe/id/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),   
    #/recipe/recipeD/add/
    url(r'recipeD/add/$', views.RecipeCreate, name='recipe-add'),

    url(r'reciped/(?P<pk>[0-9]+)/update$', views.RecipeUpdate.as_view(), name='recipe-update'),

    url(r'reciped/(?P<pk>[0-9]+)/delete$', views.RecipeDelete.as_view(), name='recipe-delete'),


]
