from django.urls import path # new
from . import views


urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('login_user', views.login_user, name = 'login_user'),
    path('logout_user', views.logout_user, name = 'logout_user'),

]