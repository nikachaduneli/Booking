from django.urls import path, include
from . import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', user_views.UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/loout.html'), name='logout'),
    path('register/', user_views.user_register, name='register'),
]
