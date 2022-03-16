from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls import static
from django.conf.urls.static import static
from.views import CustomLoginView,RegisterPage

urlpatterns=[
   path('',views.index,name='home'),
   path('profile/',views.profile,name = 'profile'),
   path('newproject/',views.new_project,name='newproject'),
   path('search/',views.search_results,name = 'search_results'),
   path('editprofile/',views.edit_profile,name='editprofile'),
   path('singleproject/',views.single_project,name='singleproject'),
   path('logout/',views.logout_request,name='logout'),
   path('login/', CustomLoginView.as_view(),name='login'),
   path('register/', RegisterPage.as_view(),name='register')


]